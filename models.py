from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Situation(db.Model):
    __tablename__ = 'situations'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=True)

    # явным образом указываем, что это отношение по колонке Choice.situation_id
    choices = db.relationship(
        'Choice',
        back_populates='situation',
        cascade='all, delete-orphan',
        foreign_keys='Choice.situation_id'  # <--- здесь
    )


class Choice(db.Model):
    __tablename__ = 'choices'
    id = db.Column(db.Integer, primary_key=True)
    situation_id = db.Column(db.Integer, db.ForeignKey('situations.id'), nullable=False)
    text = db.Column(db.String(100), nullable=False)

    # разрешаем NULL — значит «закончить уровень»
    next_situation_id = db.Column(
        db.Integer,
        db.ForeignKey('situations.id'),
        nullable=True
    )

    situation = db.relationship(
        'Situation',
        back_populates='choices',
        foreign_keys=[situation_id]
    )
    next_situation = db.relationship(
        'Situation',
        foreign_keys=[next_situation_id]
    )
