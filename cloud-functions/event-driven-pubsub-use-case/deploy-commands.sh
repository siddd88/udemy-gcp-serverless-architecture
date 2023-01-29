
# Deploy cloud function with pub-sub trigger
gcloud functions deploy wishlist_session --runtime python38 \
--trigger-topic ds-sessions-topic --entry-point trigger_wishlist_event --memory=1GB

# Publish message to the above topic 
gcloud pubsub topics publish ds-sessions-topic \
--message='{"notification":[{"session_id": "a189231nvi37413kjasd"},{"product_id":10},{"wishlist_status":1}]}'

gcloud pubsub topics publish ds-sessions-topic \
--message='{"notification":[{"session_id": "a189231nvi37413kjasd"},{"product_id":10},{"wishlist_status":0}]}'

gcloud pubsub topics publish ds-sessions-topic \
--message='{"notification":[{"session_id": "ab3321iuewmn2911"},{"product_id":3},{"wishlist_status":1}]}'

gcloud pubsub topics publish ds-sessions-topic \
--message='{"notification":[{"session_id": "mnfkp2389asdiu2321n"},{"product_id":12},{"wishlist_status":1}]}'


gcloud pubsub topics publish ds-sessions-topic \
--message='{"notification":[{"session_id": "a189231nvi37413kjasd"},{"product_id":777},{"wishlist_status":1}]}'

gcloud pubsub topics publish ds-sessions-topic \
--message='{"notification":[{"session_id": "a189231nvi37413kjasd"},{"product_id":120},{"wishlist_status":1}]}'

gcloud pubsub topics publish ds-sessions-topic \
--message='{"notification":[{"session_id": "a189231nvi37413kjasd"},{"product_id":77},{"wishlist_status":1}]}'
