from flask import Flask,render_template,request
import random
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.utils import redirect

app =Flask(__name__)

######################### SQL ALCHEMY CONFIGARATION #############################
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+ os.path.join(basedir,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
 
db = SQLAlchemy(app)
Migrate(app,db)


###################################  MODEL CREATION  #############################

class URLS(db.Model):
	__tablename__='urls'
	id = db.Column(db.Integer,primary_key=True)
	original_url = db.Column(db.Text)
	shorten_url = db.Column(db.Text)

	def __init__(self,original_url,shorten_url):
		self.original_url = original_url
		self.shorten_url = shorten_url

	def __repr__(self):
    		return "Original URL :- {} ::: Shortened URL :- 127.0.0.1:5000/sh/{}".format(self.original_url, self.shorten_url)





##############################  ROUTES CREATION ######################################

data = {}
dummylist= ['a','b',"c", "d", "e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0","_",'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

@app.route('/')
def fun_1():
	return render_template("home.html")
@app.route('/', methods=['POST'])
def home_post():
    original_url = request.form.get('in_1')
    
    if original_url != None:
        if original_url !="":
            short_url = random.choice(dummylist) + random.choice(dummylist) +random.choice(dummylist) + random.choice(dummylist)
            k = URLS.query.filter_by(original_url = original_url)
            for i in k:
                if i.original_url ==original_url:
                    short_url= i.shorten_url
                    return render_template('home.html', data=short_url)
        
            new_row = URLS(original_url, short_url)
            db.session.add(new_row)
            db.session.commit()
            return render_template('home.html', data=short_url)
    return render_template('home.html')
@app.route('/history')
def fun_history():
    	url_list = URLS.query.all()
    	return render_template("history.html",data = url_list)
@app.route('/sh/<short>')
def fun(short):
    url_list1 = URLS.query.filter_by(shorten_url = short)
    for i in url_list1:
        if (i.shorten_url) == short:
            return redirect(i.original_url)
        else:
            return "incorrect URL"

    
################################# RUN APP ##############################
if __name__ =='__main__':
	app.run(debug = True)

