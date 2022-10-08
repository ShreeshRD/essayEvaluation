from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
# from essaychecker import evaluate
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aes.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Prompts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100))
    description = db.Column(db.String(200))
    min_marks = db.Column(db.Integer)
    max_marks = db.Column(db.Integer)
    source_essay = db.Column(db.String(100))

# class Source(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     essay = db.Column(db.String(2000))

@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        prs = Prompts.query.all()
        return render_template('home.html', prompts = prs)
    else:
        return render_template('index.html', message="Hello!")

@app.route('/prompt/<int:sid>')
def prompt(sid):
    src = Prompts.query.get(sid)
    html = None
    if src.source_essay == "YES":
        with open('p'+str(sid)+'.htm','r') as file:
            html = file.read()
    return render_template('prompt.html', no = str(sid), source = src, content = html)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            hashed_password = bcrypt.generate_password_hash(request.form['password'])
            db.session.add(User(username=request.form['username'], password=hashed_password))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        session["uname"] = u
        data = User.query.filter_by(username=u).first()
        if data is not None and bcrypt.check_password_hash(data.password, p):
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

@app.route('/takeInput/',methods=['POST'])
def takeInput():
    t = request.form['input_text']
    name = session["uname"]
    # d_file = open("%s.txt" %name,"w")
    # d_file.write(t)
    # d_file.close()
    score = "evaluate(t)"
    return render_template('results.html', res = score)

if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
    db.create_all()
    app.run(debug=True)