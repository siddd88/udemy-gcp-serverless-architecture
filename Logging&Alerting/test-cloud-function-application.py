from google.cloud import storage
import os ,time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/path-to-json-credentials-file/creds.json"

storage_client = storage.Client()

bucket = storage_client.get_bucket("cloud-func-trigger")

while True:
    blob = bucket.blob('us-states.csv')
    blob.upload_from_filename('us-states.csv')
    time.sleep(50)