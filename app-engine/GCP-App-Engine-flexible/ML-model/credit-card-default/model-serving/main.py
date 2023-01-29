
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle
from flask import Flask,request,jsonify
import gcsfs,json
from google.cloud import bigquery
import pandas_gbq
import logging,time
app = Flask(__name__)

logging.getLogger().setLevel(logging.INFO)

@app.route("/",methods=["GET","POST"])

def main():
    if request.method=='POST' :
        input_data = request.get_json()
        if input_data['is_output_valid'] ==1 and input_data['total_attrbutes'] ==31 : 
            logging.info("----Input dataset validated-----")
            df = fetch_input_dataset()
            if train_model(df) : 
                return "Model Trained successfully "
            else : 
                return "Model Training Failed"
        else : 
            return "Input Dataset is not valid"
    else : 
        return "Method not allowed"

def fetch_input_dataset():    
    logging.info("----Fetching Input Data-----")
    query_string = """
            select * from 
            (
                (
                 SELECT * FROM `bigquery-public-data.ml_datasets.ulb_fraud_detection` where class =1 
                )
                union all 
                (
                    select * FROM `bigquery-public-data.ml_datasets.ulb_fraud_detection` where class=0 limit 3000 
                )
            )
        """
    df = pandas_gbq.read_gbq(query_string)
    return df

def train_model(df):
    
    fs = gcsfs.GCSFileSystem()
    training_start_msg = "---Training started at {}---".format(round(time.time()))
    logging.info(training_start_msg)

    X = df[df.columns.difference(['Class'])]
    y = df['Class'].astype('int')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    rfc_model = RandomForestClassifier()
    rfc_model.fit(X_train,y_train)
    
    predictions = rfc_model.predict(X_test)
    classification_report_dict = classification_report(y_test,predictions,output_dict=True)

    training_end_msg = "---Training Ended at {}---".format(round(time.time()))
    logging.info(training_end_msg)

    cls_report_msg = "Classification Report : {}".format(classification_report_dict)
    logging.info(cls_report_msg)

    try : 
        with fs.open('gs://bucket-name/fraud_detection_model.pkl', 'wb') as handle:
                pickle.dump(rfc_model,handle)
        return 1
    except Exception as e:
        return 0

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)