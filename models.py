from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Cookbook(db.Model):
    """Mapping user likes to warbles."""

    __tablename__ = 'cookbooks'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey('recipes.spoonacular_id')
    )


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/img/default-pic.png",
    )

    header_image_url = db.Column(
        db.Text,
        default=""
    )

    bio = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    recipes = db.relationship(
        'Recipe',
        secondary="cookbooks"
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def update(self, form):
        self.username = form.username.data,
        self.email = form.email.data,
        self.image_url = form.image_url.data,

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user. Hashes password and adds user to system"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Recipe(db.Model):
    """recipe model"""
    __tablename__ = 'recipes'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    spoonacular_id = db.Column(db.Integer(), nullable=True, unique=True)
    title = db.Column(db.String(), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
