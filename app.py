from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from scripts.essaychecker import evaluate
from flask_bcrypt import Bcrypt
from PIL import Image
import pytesseract
import scripts.globalPlag.global_plag as gplag
import scripts.localPlag.local_plag as lplag
import time
import csv
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
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_user = db.Column(db.String(100))
    t_pass = db.Column(db.String(100))
    def __init__(self, t_user, t_pass):
        self.t_user = t_user
        self.t_pass = t_pass
class Prompts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100))
    description = db.Column(db.String(200))
    min_marks = db.Column(db.Integer)
    max_marks = db.Column(db.Integer)
    source_essay = db.Column(db.String(100))

@app.route('/', methods=['GET'])
def index():
    if session.get('isTeacher'):
        return render_template('teacher_portal.html', res= '')
    elif session.get('logged_in'):
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
@app.route('/teacher_login/', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'GET':
        return render_template('teacher.html')
    else:
        u = request.form['username']
        p = request.form['password']
        session["uname"] = u
        data = Teacher.query.filter_by(t_user=u, t_pass=p).first()
        if data is not None:
            session['logged_in'] = True
            session['isTeacher'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")

@app.route('/teacher/<int:sid>', methods=['POST', 'GET'])
def teach_res(sid):
    filename = "uploads/"+str(sid)+"/report.csv"
    res = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            res.append(row)
    return render_template('teacher_portal.html', res = res)

@app.route('/teacher/<int:sid>/<string:sname>', methods=['POST', 'GET'])
def show_essay(sid,sname):
    essay = open("uploads/"+str(sid)+"/%s.txt" %sname,"r")
    t = essay.read()
    essay.close()
    return render_template('show_essay.html', content = t, name = sname)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    session['isTeacher'] = False
    return redirect(url_for('index'))

@app.route('/results/',methods=['POST'])
def takeInput():
    t = request.form['input_text']
    session["essay"] = t
    name = session["uname"]
    no = str(session['prompt_no'])
    d_file = open("uploads/"+no+"/%s.txt" %name,"w+")
    d_file.write(t)
    d_file.close()
    score = evaluate(t)
    path = '.\\uploads\\'
    l_results, flag1 = lplag.check_plagiarism(path+no)
    lscore = ''
    for ele in l_results:
        if name in ele:
            out = str(ele).replace('.txt', '')
            lscore += out.replace(name, '') + '<br/>'
    score = max(score)
    if(flag1 == 1):
        score = "0 - Please enter a valid answer."
        lscore = "N/A"
    session["score"] = score
    session["lscore"] = lscore

    #writing into results
    if(lscore == ''):
        res = [name, score, 'N/A']
    else:
        res = [name, score, lscore]
    filename = "uploads/"+no+"/report.csv"
    with open(filename, 'a') as csvfile: 
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(res)
    return render_template('results.html', res = score, loc = lscore)

@app.route('/global', methods=['POST'])
def background_process_test():
    t = session["essay"]
    if len(t.split()) > 5:
        tic = time.time()
        time.sleep(10)
        gscore = gplag.get_global_score(t)#'text --> 77% match with link: <a style="text-decoration: underline;" class="display-5">link<a/>"'# gplag.get_global_score(t)
        tic = time.time() - tic
    else:
        gscore = 0
        time.sleep(5)
        tic = 0
    return render_template('global.html', glob = gscore, time = tic)

if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)