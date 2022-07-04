import re
from flask import  *
import json
import datetime
from flask_pymongo import PyMongo
import pickle
from chefboost import Chefboost as ch
#flask and pymongo intialization
app=Flask(__name__,template_folder='template',static_url_path='/static')
#app.config['SECRET_KEY']='form project'
#for mongodb connection 
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/stroke_preds")
db = mongodb_client.db
    

#ml  model loading
f= open('stroke_model','rb') 
mp=pickle.load(f)


model_id3 = ch.load_model("cricket_models.pkl")

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


#route for id3 model
@app.route('/id3_model')
def id3():
   return  render_template('id3_form.html')

@app.route('/predict_id3',methods=['POST'])
def predict_id3():
    if request.method=="POST":
          
        
         
        predict_id3=ch.predict(model_id3,param=[request.form['outlook'],request.form['temp'],request.form['humidity'],request.form['wind'] ])
        print(request.form)
        print(predict_id3)
        if predict_id3=="No":
            pre=0
        else:
            pre=1           
         
        return  redirect(url_for('result_id3',res=pre))

@app.route("/result_id3/<int:res>")
def result_id3(res):
    print(res)
    if res==0:
        msg="You Can't Play"
    else:
         msg='You Can Play'

    return render_template('result_id3.html',msgs=msg)
        
#@app.route('/download')
#def downloadFile ():
    
    #path = "./healthcare-dataset-stroke-data.csv"
    #return send_file(path, as_attachment=True)
if __name__ =="__main__":  

    
    app.run()