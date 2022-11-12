from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from scripts.essaychecker import evaluate
from flask_bcrypt import Bcrypt
from PIL import Image
import pytesseract
import scripts.globalPlag.global_plag as gplag
import scripts.localPlag.local_plag as lplag

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

@app.route('/takeImg', methods=['POST', 'GET']) #EASTER EGG, DO NOT TOUCH
def takeImg(no):
    return """<h1 style="font-size:72px; padding:250px;">Thanks for reading our code!!!</h1>"""

@app.route('/prompt/<int:sid>', methods=['POST', 'GET'])
def prompt(sid):
    txt = ''
    session['prompt_no'] = sid
    if request.files:
        image = request.files["image"]
        im = Image.open(image)
        text = pytesseract.image_to_string(im)
        txt = text.replace('\n',' ')
    src = Prompts.query.get(sid)
    html = None
    if src.source_essay == "YES":
        with open('templates/src_essays/p'+str(sid)+'.htm','r') as file:
            html = file.read()
    return render_template('prompt.html', no = str(sid), source = src, content = html, ocr = txt)

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

@app.route('/results/',methods=['POST'])
def takeInput():
    t = request.form['input_text']
    name = session["uname"]
    no = str(session['prompt_no'])
    d_file = open("uploads/"+no+"/%s.txt" %name,"w+")
    d_file.write(t)
    d_file.close()
    score = evaluate(t)
    # if len(t.split()) > 5:
    #     gscore = gplag.get_global_score(t)
    # else:
    gscore = """In a small saucepan, add finely chopped dark chocolate and a splash of cocoa powder. Stir occasionally until melted. ('https://www.maderatribune.com/single-post/chocolate-goes-international', 48.50712500726658)

While waiting for that to melt, mix together cornstarch with a small splash of whole milk. Once chocolate is melted, add the rest of your milk slowly while constantly whisking. ('https://flavouronline.co.za/how-to-make-the-best-hot-chocolate-of-all-time/', 91.70205237216021)

Continue to heat until all of it is nice and hot. Then whisk in the cornstarch slurry. ('https://wellversed.in/blogs/articles/is-corn-starch-gluten-free', 50.09794328681196)

Continue to heat until thickened. Pour into a mug, topped with whipped cream and dust with cocoa powder. ('https://www.telegraphindia.com/culture/food/recipes-mother-s-day-specials/cid/1771655', 47.836487323494005)"""
    path = '.\\uploads\\'
    lscore = str(lplag.check_plagiarism(path+no))
    return render_template('results.html', res = score, loc = lscore, glob = gscore)

if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)