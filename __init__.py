from flask import Flask, url_for, redirect, request, render_template;
import MySQLdb;
import redis;
from pymongo import MongoClient

app = Flask(__name__)

# This is a client for REDIS NOSQL database
r = redis.StrictRedis('localhost',6379,0,charset="UTF-8",decode_responses=True);

# This is a client for MONGO DB
client = MongoClient('localhost',27017)
db = client.tododb

# This is a main route to main site Svilar davor portfolio
@app.route('/')
def portfolio():
    return render_template('index.html')

# This is a change of color under the boostrap theme
@app.route('/index1')
def index1():
    return render_template('index1.html')

# This is a route to holistic site towards holistic.html
@app.route('/holistic')
def holistic():
    return render_template('holistic.html')

# This is a route to two funduros site towards login.html
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'TWO' or request.form['password'] != 'FUNDUROS':
            error = 'Site is under construction, come again later !!!'
        else:
            return redirect(url_for('funduros'))
    return render_template('login.html', error=error)

@app.route('/funduros')
def funduros():
    return render_template("twofunduros.html")

@app.route('/page1')
def page1():
    return render_template("page1.html")

@app.route('/page2')
def page2():
    return render_template("page2.html")

@app.route('/page3')
def page3():
    return render_template("page3.html")

# This is a route to quiz site towards create question redis answer

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':

        return render_template('CreateQuestion.html');
    elif request.method == 'POST':

        title = request.form['title'];
        question = request.form['question'];
        answer = request.form['answer'];
        r.set(title +':question', question)
        r.set(title +':answer', answer)
        return render_template('CreatedQuestion.html', question = question,title = title, answer = answer);
    else:
        return "<h2>Invalid request</h2>";

@app.route('/question/<title>', methods=['GET', 'POST'])
def question(title):
    if request.method == 'GET':
        question = r.get(title+':question')
        return render_template('AnswerQuestion.html', question = question,title = title);
    elif request.method == 'POST':
        submittedAnswer = request.form['submittedAnswer'];
        answer = r.get(title+':answer')
        if submittedAnswer == answer:
            return render_template('Correct.html');
        else:
            return render_template('Incorrect.html', submittedAnswer = submittedAnswer, answer = answer);
    else:
        return '<h2>Invalid request</h2>';

# This is a route to quiz site WHOS YOUR DADDY
@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/wrong")
def wrong():
    return render_template("wrong.html")

@app.route("/right")
def right():
    return render_template("right.html")
# This is a route a WEB QZUIZ using SQL

@app.route('/starter')
def starter():
    return render_template('starter.html');

class Client(object):
    def __init__(self):
        self.connection = MySQLdb.connect("localhost","root","sv1l4r","quizdb");
        self.cursor = self.connection.cursor();
        return;
    def saveQuestion(self, title, question, answer):
        sql = "INSERT INTO questions VALUES ("+"'"+(title)+"',"+"'"+(question)+"',"+"'"+(answer)+"',"+"1"+")";
        self.cursor.execute(sql);
        self.connection.commit();
        self.connection.close();
        return;
    def getQuestion(self, title):
        sql = "SELECT Description FROM questions WHERE QuestionName = '"+(title)+"'";
        self.cursor.execute(sql);
        results = self.cursor.fetchone();
        question = results;
        self.connection.close()
        for letter in results:
            exit = ""
            if letter != ("'"):
                exit = exit + letter
            else:
                pass
        return exit;
    def getAnswer(self, title):
        try:
            sql = "SELECT CorrectAnswer FROM questions WHERE QuestionName = '"+(title)+"'";
            self.cursor.execute(sql);
            results = self.cursor.fetchone();
            correctAnswer = results;
            self.connection.close();
            for letter in results:
                exit = ""
                if letter != ("'"):
                    exit = exit + letter
            else:
                pass
            return exit;
        except MySQLdb.Error as err:
            return err;

# server/create
@app.route('/create1', methods=['GET', 'POST'])
def create1():
    if request.method == 'GET':
        return render_template('CreateQuestion1.html');
    elif request.method == 'POST':
        title = request.form['title'];
        question = request.form['question'];
        answer = request.form['answer'];

        client = Client();
        client.saveQuestion(title, question, answer);

        return render_template('CreatedQuestion1.html', question = question,title = title);
    else:
        return "<h2>Invalid request</h2>";

# server/question/<title>
@app.route('/question1/<title>', methods=['GET', 'POST'])
def question1(title):
    if request.method == 'GET':
        client = Client();
        question = client.getQuestion(title);
        return render_template('AnswerQuestion1.html', question = question);
    elif request.method == 'POST':
        submittedAnswer = request.form['submittedAnswer'];

        client = Client();
        answer = client.getAnswer(title)

        if submittedAnswer == answer:
            return render_template('Correct1.html');
        else:
            return render_template('Incorrect1.html', submittedAnswer = submittedAnswer, answer = answer);
    else:
        return '<h2>Invalid request</h2>';

# This is a part of web Mongo db site
@app.route('/todo')
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]
    return render_template('todo.html', items=items)

@app.route('/new', methods=['POST'])
def new():
    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)
    return redirect(url_for('todo'))



if __name__ == '__main__':
    app.run()
