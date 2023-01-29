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

def cache_results(trip_miles,trip_seconds):    
    post_response = '{"trip_miles":'+str(trip_miles)+',"trip_seconds":'+str(trip_seconds)+'}'
    BqResult(post_response='{}'.format(post_response)).put()

def fetch_cached_results(limit):
    return BqResult.query().order(-BqResult.timestamp).fetch(limit)

def fetch_bq_result(unique_id):
    sql = """
        SELECT
            trip_miles,
            trip_seconds
        FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
        where unique_key={0}
    """.format(unique_id)

    query_job = bigquery_client.query(sql)
    trip_miles = '0'
    trip_seconds = '0'

    for row in query_job : 
        trip_miles = row[0]
        trip_seconds = row[1]

    return trip_miles,trip_seconds

@app.route('/')
def root():
    unique_id= request.args.get('unique_id', default = "ff0b96c0cada768361b1c9341e11905254644afb", type = str)
    unique_id = str(unique_id)

    bq_result = memcache.get(unique_id)

    if not bq_result :
        trip_miles,trip_seconds =  fetch_bq_result(unique_id)
        cache_results(trip_miles,trip_seconds)
        memcache.set(unique_id, bq_result, HOUR)
        bq_result = list(fetch_cached_results(1))

    return render_template('index.html', bq_result=bq_result)