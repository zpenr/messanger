from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
class RegistrationForm(FlaskForm):
    name = StringField("Логин")
    password = PasswordField('Пароль')
    submit = SubmitField('Войти')
