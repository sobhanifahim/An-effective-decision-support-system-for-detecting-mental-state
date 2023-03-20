import pandas as pd
import numpy as np
import pickle
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder


df=pd.read_csv('dataset-eeg.csv')
df.drop('Patient_ID',axis=1,inplace=True)
df.drop('Gender',axis=1,inplace=True)
X = df.drop('MindState', axis=1)
Y=df['MindState']
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=77)


rf= RandomForestClassifier (n_estimators=10, max_features="auto", random_state=77)
rf.fit(X_train,y_train)
pickle.dump(rf,open('model.pkl','wb'))

