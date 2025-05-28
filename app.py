import os
import secrets

from flask import Flask, render_template, redirect, url_for, flash, session
from models import db, User
from forms import RegistrationForm, LoginForm, ChangePasswordForm

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(24))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_user():
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            return dict(nickname=user.nickname)
        return dict(nickname=None)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(nickname=form.nickname.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрированы!', 'success')
            return redirect(url_for('login'))

        elif User.query.filter_by(nickname=form.nickname.data).first():
            flash('Пользователь с таким ником уже существует. Пожалуйста, выберите другое имя.', 'danger')

        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(nickname=form.nickname.data).first()
            if user and user.check_password(form.password.data):
                session['user_id'] = user.id
                flash('Вход выполнен!', 'success')
                return redirect(url_for('game'))
            flash('Неверный ник или пароль.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/game')
    def game():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        # список уровней с названиями
        levels = [
            {'num': 1, 'title': '8 минут до катастрофы'},
            {'num': 2, 'title': 'Глубина отчаяния'},
            {'num': 3, 'title': 'Учения на границе мира'}
        ]
        return render_template('game.html', levels=levels)

    @app.route('/game/<int:level>')
    def game_level(level):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        # найдём в том же списке название выбранного уровня
        level_info = next((l for l in [
            {'num': 1, 'title': '8 минут до катастрофы'},
            {'num': 2, 'title': 'Глубина отчаяния'},
            {'num': 3, 'title': 'Учения на границе мира'}
        ] if l['num'] == level), None)

        if not level_info:
            return redirect(url_for('game'))

        return render_template('game.html',
                               level=level_info['num'],
                               level_title=level_info['title'])

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash('Вы вышли из системы.', 'info')
        return redirect(url_for('index'))

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        form = ChangePasswordForm()
        if form.validate_on_submit():
            if not user.check_password(form.old_password.data):
                flash('Старый пароль введён неверно.', 'danger')
            else:
                user.set_password(form.new_password.data)
                db.session.commit()
                flash('Пароль успешно изменён!', 'success')
                return redirect(url_for('profile'))
        return render_template('profile.html', form=form, progress='', nickname=user.nickname)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
