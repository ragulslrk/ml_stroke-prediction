import re
from flask import  *
import json
import datetime
from flask_pymongo import PyMongo
import pickle

#flask and pymongo intialization
app=Flask(__name__,template_folder='template',static_url_path='/static')
app.config['SECRET_KEY']='form project'
#for mongodb connection 
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/stroke_preds")
db = mongodb_client.db
    

#ml  model loading
f= open('stroke_model','rb') 
mp=pickle.load(f)


@app.route('/')
def  home():
    return render_template('index.html')

@app.route('/form')
def  form():
    return render_template('form.html')



#predict
@app.route('/predict',methods=['POST'])
def predict():
    if request.method=="POST":
        print(request.form)
        gender=int(request.form['gender'])
        age=int(request.form['age'])
        Hypertension=int(request.form['Hypertension'])
        marry=int(request.form['martial'])
        work=int(request.form['Working'])
        glucose=float(request.form['glucose'])
        bmi=float(request.form['bmi'])
        smoking=int(request.form['smoking_status'])
        # ans=mp.predict([[1,67.0,0,1,0,93.71,31.200000,1]])
        ans=mp.predict([[gender,age,Hypertension, marry,work,glucose,bmi,smoking]])
        print(ans[0])
        return  redirect(url_for('result',res=ans[0],name=request.form['name']))
        
#result
@app.route("/result/<int:res>/<name>")
def result(name,res):
    print(name,res)
    if res==0:
        msg='Stroke predicted negative'
    else:
         msg='Stroke predicted Positive'

    return render_template('result.html',names=name,msgs=msg)
        
if __name__ =="__main__":  
    
    app.run()