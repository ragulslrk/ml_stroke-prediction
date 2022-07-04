
from chefboost import Chefboost as ch
model_id3 = ch.load_model("cricket_models.pkl")   
pre=ch.predict(model_id3, param = ['Rain', 'Mild', 'High', 'Weak'])
print('this is id3:',pre)