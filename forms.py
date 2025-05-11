from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    nickname = StringField('Ник', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(6, 128)])
    password2 = PasswordField('Повтор пароля', validators=[
        DataRequired(), EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('Ник уже занят.')

class LoginForm(FlaskForm):
    nickname = StringField('Ник', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired(), Length(6, 128)])
    new_password2 = PasswordField('Повтор нового пароля', validators=[
        DataRequired(), EqualTo('new_password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Сменить пароль')
