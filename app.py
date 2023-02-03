import os
from flask import Flask, request, render_template, redirect, flash, session, jsonify, g
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Cookbook, Recipe
from form import SearchByIngredientsForm, UserAddForm, LoginForm, UserUpdateForm, ComplexForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func
from env_keys.env_secrets import APP_CONFIG_KEY
from search_by import search_api_complex, search_api_by_ingredients, search_api_for_instructions, search_api_random_recipe
from helpers import save_user_images, update_user_images


CURR_USER_KEY = "curr_user"
UPLOAD_FOLDER = 'static/profile_imgs'


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipes_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = APP_CONFIG_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

debug = DebugToolbarExtension(app)
connect_db(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id
    session['username'] = user.username


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        del session['username']


@app.route('/register', methods=["GET", "POST"])
def register():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        form = save_user_images(form)
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data.filename if form.image_url.data else User.image_url.default.arg,
                header_image_url=form.header_image_url.data.filename if form.header_image_url.data else User.header_image_url.default.arg
            )
            db.session.commit()

        except IntegrityError:
            os.remove(f'{UPLOAD_FOLDER}/{form.image_url.data.filename}')
            os.remove(f'{UPLOAD_FOLDER}/{form.header_image_url.data.filename}')
            flash("Username already taken", 'danger')
            return render_template('users/register.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash('Goodbye!', 'success')
    return redirect('/login')
########################### USER ROUTES ##########################


@app.route('/users/<int:user_id>')
def g_user_show(user_id):
    if not g.user:
        flash("You need to sign in first.", "danger")
        return redirect("/register")
    user = User.query.get_or_404(user_id)
    recipes = user.recipes
    return render_template('/users/show.html', user=user, recipes=recipes)


@app.route('/users/profile', methods=["GET", "POST"])
def user_profile():
    """Update profile for current user."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    user = User.query.get_or_404(g.user.id)
    form = UserUpdateForm(obj=user)
    if form.validate_on_submit():
        if User.authenticate(g.user.username, form.password.data):
            form = update_user_images(form, user)
            try:
                # bug: 01
                user.update(form)
                db.session.commit()
                do_login(user)
                flash('UPDATED!', 'success')
                return redirect(f"/users/{g.user.id}")
            except:
                db.session.rollback()
                form.username.errors.append('Username/Email already exist')
                return render_template('users/edit.html', form=form, user=user)

        else:
            form.password.errors.append('Incorrect Password')
    return render_template('users/edit.html', form=form, user=user)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()
    os.remove(f'{UPLOAD_FOLDER}/{g.user.image_url}')
    os.remove(f'{UPLOAD_FOLDER}/{g.user.header_image_url}')
    flash('Sorry to see you go...', 'success')
    return redirect("/register")


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users/index.html', users=users)


########################### SEARCH ROUTES##########################


@app.route('/search/ingredients', methods=['GET', 'POST'])
def search_ingredients():
    form = SearchByIngredientsForm()
    if form.validate_on_submit():
        '''get inputs val that is not NULL'''
        data = [x for x in form.ingredients.data if x]
        resp = search_api_by_ingredients(data)
        return render_template('recipes/show_search_by_res.html', recipes=resp, ingredients=data, complex=False)
    return render_template('search/form_by_ingredients.html', form=form)


@app.route('/search/random')
def get_random_recipe():
    resp = search_api_random_recipe()
    return render_template('recipes/show_by_random.html', recipes=resp.get('recipes'))


@app.route('/search/<int:recipe_id>/instructions', methods=['GET'])
def start_cooking(recipe_id):
    instructions = search_api_for_instructions(recipe_id)
    user_cookbook = [id for id, x in db.session.query(Cookbook.recipe_id, Cookbook.id).filter(
        Cookbook.user_id == g.user.id).all()]
    return render_template('recipes/start_cooking.html', recipe=instructions, user_cookbook=user_cookbook)


@app.route('/search/top_five')
def top_five():
    top = [id for id, count in db.session.query(Cookbook.recipe_id, db.func.count(Cookbook.recipe_id)).group_by(
        Cookbook.recipe_id).order_by(db.func.count(Cookbook.recipe_id).desc()).limit(5).all()]
    recipes = Recipe.query.filter(Recipe.spoonacular_id.in_(top)).all()
    return render_template('recipes/show_top_five.html', recipes=recipes)


@app.route('/search/complex', methods=['GET', 'POST'])
def complex_search():
    form = ComplexForm()
    if form.validate_on_submit():
        cuisine = form.cuisine.data
        ingredients = [x for x in form.ingredients.data if x]
        diet = form.diet.data
        meal_type = form.meal_type.data
        resp = search_api_complex(cuisine, ingredients, diet, meal_type)
        return render_template('recipes/show_search_by_res.html',
                               recipes=resp.get('results'),
                               complex=True,
                               cuisine=cuisine,
                               ingredients=ingredients,
                               diet=diet,
                               meal_type=meal_type)
    return render_template('search/complex_form.html', form=form)


@app.route('/save_recipe/<int:recipe_id>/<recipe_title>', methods=['POST'])
def save_to_cookbook(recipe_id, recipe_title):
    if not g.user:
        return jsonify({'response': 'not logged in'})
    user = User.query.get(g.user.id)
    users_cookbook = [x[0] for x in db.session.query(Cookbook.recipe_id).filter(
        Cookbook.user_id == user.id).all()]
    data = request.json
    if recipe_id in users_cookbook:
        cookbook = Cookbook.query.filter_by(
            recipe_id=recipe_id, user_id=user.id).first()
        db.session.delete(cookbook)
        db.session.commit()
        return jsonify({'response': 'unsaved'})
    recipe = Recipe.query.filter(Recipe.spoonacular_id == recipe_id).first()
    if recipe:
        # if the recipe is already saved just add to users cookbook
        cookbook = Cookbook(user_id=user.id, recipe_id=recipe.spoonacular_id)
        db.session.add(cookbook)
        db.session.commit()
    else:
        # else save recipe to db first then add to cookbook
        saved_recipe = Recipe(spoonacular_id=recipe_id, title=recipe_title, image_url=data.get(
            'image'), ingredients=data.get('ingredients'))
        user.recipes.append(saved_recipe)
        db.session.commit()
    return jsonify({'response': 'saved'})


@app.route('/')
def homepage():
    """Show homepage"""
    if g.user:
        return render_template('home.html')
    else:
        return render_template('home-anon.html')


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
