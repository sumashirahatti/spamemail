import cPickle as c
import cPickle as c
import os
from sklearn import *
from collections import Counter
from flask import Flask, request, render_template
from werkzeug import secure_filename
un="sakilbhai"
ps="sakil123"
status=""
UPLOAD_FOLDER = '/home/sakil/Desktop/project1/sakil/emails'

def load(classifier_file):
    with open(classifier_file) as fp:
        classifier=c.load(fp)
    return classifier
def make_dict():
    directory = "emails/"
    root = os.listdir(directory)
    emails = [directory + email for email in root]
    words = []

    count = len(emails)
    for email in emails:
        y = open(email)
        z = y.read()
        words += z.split(" ")
        print count
        count -= 1

    for j in range(len(words)):
        if not words[j].isalpha():
            words[j] = ""

    dictionary = Counter(words)
    del dictionary[""]
    return dictionary.most_common(3000)





app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
@app.route('/')
def my_form():
    return render_template('hello.html')
@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['mail']
    classifier = load("model.mdl")
    dict = make_dict()
    
    features = []
    user = text.split()
        
    for word in dict:
        features.append(user.count(word[0]))
    res = classifier.predict([features])
    
    a=["Not Spam", "Spam!"][res[0]]
    return render_template('hello.html',result=a)

@app.route('/login')
def loginpage():
     return render_template('home.html')
@app.route('/loginauth',methods=['POST'])
def ifsuccess():
    uname=request.form['uname']
    passw=request.form['psw']
    if un==uname and passw==ps:
        lisst=(os.listdir('/home/sakil/Desktop/project1/sakil/emails')) 
        return render_template('filelist.html',resul=lisst)
        
     
        

    else:
        return "LOGIN FAILED PLEASE CHECK YOUR USERNAME AND PASSWORD!! PLEASE GO BACK AND TRY AGAIN"

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
      lisst=(os.listdir('/home/sakil/Desktop/project1/sakil/emails')) 
      return render_template('filelist.html',status="success",resul=lisst)





    
if __name__ == '__main__':
   app.run(debug = True)


