import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from google.cloud import storage
from joblib import dump

storage_client = storage.Client()
bucket = storage_client.bucket("{your-bucket-name}")

df = pd.read_csv('gs://{your-bucket-name}/adclick-model-input/advertising.csv')

X = df[df.columns.difference(['Class'])]
y = df['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
rfc_model = RandomForestClassifier(n_estimators=600)
rfc_model.fit(X_train,y_train)

dump(rfc_model, 'model.joblib')
rfc_model = bucket.blob('model_output/model/model.joblib')
rfc_model.upload_from_filename('model.joblib')