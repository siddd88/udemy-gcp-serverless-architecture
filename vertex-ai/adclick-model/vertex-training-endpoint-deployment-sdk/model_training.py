import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from google.cloud import storage
from joblib import dump
from sklearn.pipeline import make_pipeline

storage_client = storage.Client()
bucket = storage_client.bucket("your-bucket-name")

df = pd.read_csv('gs://your-bucket-name/adclick-model-input/advertising.csv')
max_iter= 1000
solver= 'lbfgs'

X = df[['Daily Time Spent on Site', 'Age', 'Area Income','Daily Internet Usage', 'Male']]
y = df['Clicked on Ad']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

logmodel = LogisticRegression(solver=solver,max_iter=max_iter)

pipeline = make_pipeline(logmodel)

pipeline.fit(X_train, y_train)

dump(pipeline, 'model_artifacts/model.joblib')

model_artifact = bucket.blob('adclick-model-artifact/model.joblib')

model_artifact.upload_from_filename('model_artifacts/model.joblib')

#pipeline.predict([[23.95,53,1182,20,0]])