import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
# from google.cloud import storage
from flask import Flask,request
import gcsfs
import logging,time,json

app = Flask(__name__)

logging.getLogger().setLevel(logging.INFO)

@app.route("/")
def main():
    input_path = 'gs://your-bucket-name/advertising.csv'
    max_iter= request.args.get('max_iter', default = 1000, type = int)
    solver= request.args.get('solver', default ='lbfgs', type = str) # lbfgs,liblinear

    preprocessing_msg= "---Pre-processing started at {}---".format(round(time.time()))
    logging.info(preprocessing_msg)
    
    X_train,y_train = data_preprocess(input_path)

    training_started_msg = "---Training started at {}---".format(round(time.time()))
    logging.info(training_started_msg)

    logmodel = LogisticRegression(solver=solver,max_iter=max_iter)
    logmodel.fit(X_train,y_train)

    fs = gcsfs.GCSFileSystem()
    with fs.open('gs://your-bucket-name/ad_model.pkl', 'wb') as handle:
        pickle.dump(logmodel,handle)

    training_end_msg = "---Training Ended at {}---".format(round(time.time()))
    logging.info(training_end_msg)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

def data_preprocess(input_path):
    df = pd.read_csv(input_path)
    X = df[['Daily Time Spent on Site', 'Age', 'Area Income','Daily Internet Usage', 'Male']]
    y = df['Clicked on Ad']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    return X_train,y_train

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)
