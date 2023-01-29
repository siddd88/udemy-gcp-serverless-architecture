import flask,json
from flask import request,jsonify
from google.cloud import bigquery
import logging

app = flask.Flask(__name__)

logging.getLogger().setLevel(logging.INFO)
bigquery_client = bigquery.Client()

# @app.route("/")
@app.route("/",methods=["GET","POST"])

def main():
    # post_id= request.args.get('post_id', default = '1', type = int)
    if request.method=='POST' :

        logging.info("----POST REQUEST Initiated-----")
        input_data = request.get_json()
        # return jsonify(input_data)
        post_id = input_data['post_id']

        sql = """
            SELECT
            answer_count,comment_count
            FROM `bigquery-public-data.stackoverflow.stackoverflow_posts`
            where id={0}
        """.format(int(post_id))

        query_job = bigquery_client.query(sql)
        for row in query_job:
            a = row[0]
            b = row[1]
        
        post_response = dict()
        post_response['answer_count'] = str(a)
        post_response['comment_count'] = str(b)

        logging.info("----Response Triggered-----")
        return jsonify(post_response)
    else : 
        return "Invalid Response"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)