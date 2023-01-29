
# Deploy cloud function with pub-sub trigger
gcloud functions deploy cloud-func-pubsub --runtime python38 \
--trigger-topic cf-test-topic --entry-point process_pubsub_events --memory=1GB

# Publish message to the above topic 
gcloud pubsub topics publish cf-test-topic --message="Hello Cloud Function"