from os import getenv
from dotenv import load_dotenv


from flask import Flask, render_template, flash, url_for, redirect
from flask_login import current_user, login_required, LoginManager, login_user

from sqlalchemy import select


from db import Session, Travel, User
from forms import LoginForm, RegisterForm


from datetime import date


load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    with Session.begin() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if user:
            user = User(email=user.email)
            return user


@app.get("/")
def index():

    return render_template("index.html")


@app.get('/register')
def register():
    form = RegisterForm()
    return render_template('form_template.html', form=form)

@app.post('/register')
def register_post():
    form = RegisterForm()
    with Session.begin() as session:
        user = session.scalar(select(User).where(User.email == form.email.data))
        if user:
            flash("User exists!")
            return redirect(url_for('register'))
        pwd = form.password.data
        user = User(
            nickname=form.email.data.split('@')[0],
            email=form.email.data,
            password=pwd,
        )
        session.add(user)
        return redirect(url_for('login'))
    return render_template('form_template.html', form=form)

@app.get('/login')
def login():
    form = LoginForm()
    return render_template('form_template.html', form=form)

@app.post('/login')
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        with Session.begin() as session:
            user = session.query(User).where(User.nickname == form.nickname.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for("index"))
                flash("Wrong password")
            else:
                flash("Wrong nickname")
    return render_template('form_template.html', form=form)




if __name__ == "__main__":
    app.run(debug=True)