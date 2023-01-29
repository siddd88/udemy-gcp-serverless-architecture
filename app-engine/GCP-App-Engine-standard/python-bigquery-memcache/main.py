from flask import Flask, render_template, request
from google.appengine.api import memcache,wrap_wsgi_app
from google.appengine.ext import ndb
from google.cloud import bigquery
import json 

bigquery_client = bigquery.Client()
app = Flask(__name__)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app)
HOUR = 3600

class BqResult(ndb.Model):
    post_response   = ndb.JsonProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

def cache_results(answer_count,comment_count):    
    post_response = '{"answer_count":'+str(answer_count)+',"comment_count":'+str(comment_count)+'}'
    BqResult(post_response='{}'.format(post_response)).put()

def fetch_cached_results(limit):
    return BqResult.query().order(-BqResult.timestamp).fetch(limit)

def fetch_bq_result(post_id):
    sql = """
        SELECT
            answer_count,
            comment_count
        FROM `bigquery-public-data.stackoverflow.stackoverflow_posts`
        where id={0}
    """.format(int(post_id))

    query_job = bigquery_client.query(sql)
    answer_count = '0'
    comment_count = '0'

    for row in query_job : 
        answer_count = row[0]
        comment_count = row[1]

    return answer_count,comment_count

@app.route('/')
def root():
    post_id= request.args.get('post_id', default = 1, type = int)
    post_id = str(post_id)

    bq_result = memcache.get(post_id)

    if not bq_result :
        answer_count,comment_count =  fetch_bq_result(post_id)
        cache_results(answer_count,comment_count)
        memcache.set(post_id, bq_result, HOUR)
        bq_result = list(fetch_cached_results(1))

    return render_template('index.html', bq_result=bq_result)