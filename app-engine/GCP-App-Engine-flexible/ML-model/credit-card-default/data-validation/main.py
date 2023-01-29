from flask import Flask,request,jsonify
from google.cloud import bigquery
app = Flask(__name__)
import logging

logging.getLogger().setLevel(logging.INFO)
client = bigquery.Client()

@app.route("/")

def main():
    ds_attribute_count = validate_dataset_attributes()
    ds_output_variable_stats = validate_output_variable()
    output_dict = {}
    output_dict['total_attrbutes'] = ds_attribute_count
    output_dict['is_output_valid'] = ds_output_variable_stats
    return jsonify(output_dict)

def validate_output_variable():
    qry = """
            SELECT 
                case when count(1)>1 then 0 else 1 end  is_output_valid
            FROM `bigquery-public-data.ml_datasets.ulb_fraud_detection` 
            where Class not in (0,1)
            """
    query_job = client.query(qry)
    result = query_job.result()
    for row in result : 
        return row.is_output_valid

def validate_dataset_attributes():
    qry = """
            SELECT 
                count(distinct column_name) as col_count
            FROM  
                bigquery-public-data.ml_datasets.INFORMATION_SCHEMA.COLUMNS
            WHERE table_name = "ulb_fraud_detection";
           """
    query_job = client.query(qry)
    result = query_job.result()
    for row in result : 
        return row.col_count

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)