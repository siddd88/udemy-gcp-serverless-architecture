# APIs to be enabled 
- cloud function 
- cloud build 
- eventarc
- cloud run admin api 
- artifact registry 

PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects list --filter="project_id:$PROJECT_ID" --format='value(project_number)')
SERVICE_ACCOUNT=$(gsutil kms serviceaccount -p $PROJECT_NUMBER)

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:$SERVICE_ACCOUNT \
  --role roles/pubsub.publisher

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:$SERVICE_ACCOUNT \
  --role roles/run.admin


gcloud functions deploy python-load-bq \
--gen2 \
--runtime=python310 \
--region=us-central1 \
--source=. \
--entry-point=upload_file \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=cloud-func-trigger"
# --max-instances


gcloud functions deploy python-load-bq \
--runtime=python310 \
--region=us-central1 \
--source=. \
--entry-point=upload_file \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=cloud-func-trigger"

gsutil cp us-states.csv gs://cloud-func-trigger/us-states.csv

gcloud beta functions logs read python-load-bq --gen2 --limit=100