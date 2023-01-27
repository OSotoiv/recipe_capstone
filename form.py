from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, FieldList, TextAreaField, RadioField, SelectField
from wtforms.validators import InputRequired, Optional, NumberRange, ValidationError, DataRequired, Email, Length


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UserUpdateForm(UserAddForm):
    """form for updating user"""

# class SearchByIngredients(Form):
#     ingredient = StringField('Ingredient')


class SearchByIngredientsForm(FlaskForm):
    ingredients = FieldList(StringField(label='Ingredient'),
                            min_entries=5, max_entries=5)


cuisines = [(''), ('African'), ('American'), ('British'), ('Cajun'), ('Caribbean'), ('Chinese'), ('Eastern European'),
            ('European'), ('French'), ('German'), ('Greek'),
            ('Indian'), ('Irish'), ('Italian'), ('Japanese'),
            ('Jewish'), ('Korean'), ('Latin American'), ('Mediterranean'),
            ('Mexican'), ('Middle Eastern'), ('Nordic'), ('Southern'),
            ('Spanish'), ('Thai'), ('Vietnamese')]

diets = [(''), ('Gluten Free'), ('Ketogenic'), ('Vegetarian'), ('Lacto-Vegetarian'), ('Ovo-Vegetarian'),
         ('Vegan'), ('Pescetarian'), ('Paleo'), ('Primal'), ('Low FODMAP'), ('Whole30')]

meal_types = [(''), ('main course'), ('side dish'), ('dessert'), ('appetizer'), ('salad'), ('bread'),
              ('breakfast'), ('soup'), ('beverage'), ('sauce'), ('marinade'), ('fingerfood'), ('snack'), ('drink')]


class ComplexForm(FlaskForm):
    ingredients = FieldList(StringField(label='Ingredient'),
                            min_entries=5, max_entries=5)
    cuisine = SelectField('Cuisine Type', choices=cuisines)
    diet = SelectField('Diet Types', choices=diets)
    meal_type = SelectField('Meal Type', choices=meal_types)
