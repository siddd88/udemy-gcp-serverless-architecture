# Create a New Service Account in GCP before executing the below gcloud commands    
!gcloud projects add-iam-policy-binding gcp-serverless-project \
    --member=serviceAccount:{your service account name} \
    --role=roles/aiplatform.customCodeServiceAgent

!gcloud projects add-iam-policy-binding gcp-serverless-project \
    --member=serviceAccount: {your service account name} \
    --role=roles/aiplatform.admin

!gcloud projects add-iam-policy-binding gcp-serverless-project \
    --member=serviceAccount:{your service account name} \
    --role=roles/storage.objectAdmin

# Step-1 - Build the image 
docker build -t ad-model .

# Step-2 - Tag the image locally
docker tag ad-model gcr.io/gcp-serverless-project/ad-model

# Step-3 - Push the image to Google Cloud Registry 
docker push gcr.io/gcp-serverless-project/ad-model

# Step-4 - Run the image to Google Cloud Registry 
docker run gcr.io/gcp-serverless-project/ad-model