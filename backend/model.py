from sklearn.ensemble import GradientBoostingClassifier
import pickle
import pandas as pd

file = open("backend/grav.pickle", 'rb')
model = pickle.load(file)
file.close()

file = open("backend/datapreprocessing.pickle", 'rb')
func = pickle.load(file)
file.close()

input_variables = pd.DataFrame([[37,20.2,2,0,0,"Normal Sinus Rhythm",11.5,10,0.9]],columns=['age', 'bmi', 'asa','preop_htn','preop_dm','preop_ecg','preop_hb','preop_aptt','preop_cr'])
df=func(input_variables)
ypred=model.predict(df)
print(ypred)


