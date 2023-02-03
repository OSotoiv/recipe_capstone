from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, EmailField, PasswordField, FieldList, TextAreaField, RadioField, SelectField
from wtforms.validators import InputRequired, ValidationError, DataRequired, Length, Email, Regexp


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    def allowed_file(form, field):
        file = field.data
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        # file is a file and has a file name. strings will not have file name
        if not file or type(file) == str:
            return True
        allow = '.' in file.filename and \
                file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        if allow == False:
            raise ValidationError('File type not allowed...')

    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = FileField('Profile Image', validators=[allowed_file])
    header_image_url = FileField('Background Image', validators=[allowed_file])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UserUpdateForm(UserAddForm):
    """form for updating user"""
    bio = TextAreaField('Bio: Share a little about your interiest')

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
