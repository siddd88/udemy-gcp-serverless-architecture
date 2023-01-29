# Define the Variables 
export GOOGLE_CLOUD_PROJECT={your-project-id}
export REGION=us-central1
export BUCKET=pyspark-jobs-ph

# Enable the APIs
gcloud services enable bigquery.googleapis.com
gcloud services enable dataproc.googleapis.com

# Create Subnet 
gcloud compute networks subnets update default \
  --region=${REGION} \
  --enable-private-ip-google-access

gcloud compute networks subnets describe default \
  --region=${REGION} \
  --format="get(privateIpGoogleAccess)"

# Define a PH Cluster Name   
PHS_CLUSTER_NAME=pyspark-phs

# Create a bucket with the above variable : BUCKET
gsutil mb -l ${REGION} gs://${BUCKET}

# Create a dataproc PHS Cluster 
gcloud dataproc clusters create ${PHS_CLUSTER_NAME} \
    --region=${REGION} \
    --single-node \
    --enable-component-gateway \
    --properties=spark:spark.history.fs.logDirectory=gs://${BUCKET}/phs/spark-job-history
    --properties=spark:spark.dynamicAllocation.maxExecutors=10

# Submit the pyspark batch job to dataproc serverless 
gcloud dataproc batches submit pyspark top_stackoverflow_tags.py \
  --batch=top-stackoverflow-tags \
  --region=${REGION} \
  --deps-bucket=gs://serverless-spark-udemy \
  --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar \
--history-server-cluster=projects/${GOOGLE_CLOUD_PROJECT}/regions/${REGION}/clusters/${PHS_CLUSTER_NAME} \
  -- ${BUCKET}

# Submit the pyspark batch job to dataproc serverless with autoscaling parameters 
gcloud dataproc batches submit pyspark top_stackoverflow_tags.py \
  --batch=top-stackoverflow-tags \
  --region=${REGION} \
  --deps-bucket=gs://serverless-spark-udemy \
  --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar \
--history-server-cluster=projects/${GOOGLE_CLOUD_PROJECT}/regions/${REGION}/clusters/${PHS_CLUSTER_NAME} \
--properties=spark.dynamicAllocation.initialExecutors=3 \
  -- ${BUCKET}
