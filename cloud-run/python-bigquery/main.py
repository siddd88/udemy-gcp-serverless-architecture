from flask import Flask
import json
import os
from flask import request
from google.cloud import bigquery
app = Flask(__name__)

bigquery_client = bigquery.Client()

@app.route("/")

def main():
    post_id= request.args.get('post_id', default = '1', type = int)
    sql = """
        SELECT
        answer_count,comment_count
        FROM `bigquery-public-data.stackoverflow.stackoverflow_posts`
        where id={0}
    """.format(int(post_id))
    
    dataframe = ( bigquery_client.query(sql)
    .result()
    .to_dataframe(create_bqstorage_client=True,)
    )
    return {"data": json.loads(dataframe.to_json(orient='records'))}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5052)))