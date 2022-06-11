from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from admin import admin_page

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Viskonti'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(admin_page, url_prefix='/admin')
db = SQLAlchemy(app)

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    info = db.Column(db.String(60), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f'{self.id})Title: {self.title} || Info: {self.info} || Rating: {self.rating}'


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(60), nullable=False)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        account_info = Account.query.all()
        for each in account_info:
            acc_username = each.username
            acc_password = each.password
            if request.form['username'] not in acc_username:
                flash('Invalid username')
            elif request.form['password'] not in acc_password:
                flash('Invalid password')
            else:
                session['username'] = username
                flash('You were logged in')
                return redirect(url_for('user'))
    session.pop('username', None)
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        r_username = request.form['r_username']
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        if mail == '' or password == '' or r_username == '' or lastname == '' or firstname == '':
            flash('შეავსეთ ყველა ველი')
        elif len(password) < 8:
            flash('პაროლი უნდა შედგებოდეს მინიმუმ  8 სიმბოლოსგან')
        else:
            b2 = Account(username=r_username, password=password)
            db.session.add(b2)
            db.session.commit()
            session['mail'] = mail
            return redirect(url_for('user'))

    session.pop('mail', None)
    return render_template('registration.html')


@app.route('/user')
def user():
    subjects = ['Python', 'Calculus', 'DB']
    return render_template('user.html', subjects=subjects)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('mail', None)
    flash('You were logged out')
    return redirect(url_for('home'))


@app.route('/anime', methods=['GET', 'POST'])
def anime():
    if request.method == 'POST':
        t = request.form['title']
        i = request.form['info']
        r = request.form['rating']
        if t == '' or i == '' or r == '':
            flash('შეიტანეთ ყველა ველი')
        elif not isfloat(r):
            flash('შეიტანეთ რიცხვი რეიტინგის ველში')
        else:
            b1 = Anime(title=t, info=i, rating=float(r))
            db.session.add(b1)
            db.session.commit()
            flash('მონაცემები დამატებულია')

    return render_template('animes.html')


@app.route('/list', methods=['GET', 'POST'])
def anime_list():
    content = Anime.query.all()
    return render_template('anime_list.html', content=content)


if __name__ == "__main__":
    app.run(debug=True)
