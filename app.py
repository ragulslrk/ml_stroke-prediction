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

@app.route('/form')
def  home():
    return render_template('form.html')

#predict
@app.route('/predict',methods=['POST'])
def predict():
    if request.method=="POST":
       ans=mp.predict([[1,67.0,0,1,0,93.71,31.200000,1]])
       res= ans[0]
       return res
        
if __name__ =="__main__":  
    
    app.run()