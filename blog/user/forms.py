from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length , Email, EqualTo, ValidationError
from flask_login import current_user
from blog.models import Users


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20, message="username length!") ])
    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators= [DataRequired()])
    confirm_pass = PasswordField("confirm password", validators=[DataRequired(), EqualTo("password", message="the passwords do not match!") ])
    submit = SubmitField("SIGN UP")

    def validate_username(self, username):
        user = Users.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError("The username is not available. Choose a diffrent one")

    def validate_email(self, email):
        email = Users.query.filter_by(email= email.data).first()
        if email:
            raise ValidationError("The email is taken. Choose another one.")


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RestRequestForm(FlaskForm):
    email =  email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')


    def validate_email(self, email):
            user = Users.query.filter_by(email=email.data).first()
            if not user:
                raise ValidationError('There is no registered user with this email.')


class RestPasswordForm(FlaskForm):
    password = PasswordField("Password", validators= [DataRequired()])
    confirm_pass = PasswordField("confirm password", validators=[DataRequired(),\
                    EqualTo("password", message="the passwords do not match!") ])
    submit = SubmitField("Rest Password")

