# First Approach

# Step-1 - Build the image 
docker build -t pybigquery .

# Step-2 - Test the image locally 
docker run -p 8081:8081 pybigquery

# Step-3 - Tag the image locally 
docker tag pybigquery gcr.io/{your-project-id}/pybigquery
ø
# Step-4 - Push the image to Google Clouød Registry 
docker push gcr.io/{your-project-id}/pybigquery

# Deploy from GCR Image 

gcloud run deploy pybigquery \
--image gcr.io/{your-project-id}/pybigquery --region us-central1 \
--allow-unauthenticated \
  --max-instances 2 \
  --min-instances 1 

# Deploy to Cloud Run  
gcloud run deploy python-bigquery-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --max-instances 2 \
  --min-instances 1 


  # Assign the roles 
  gcloud projects add-iam-policy-binding {your-project-id} \
  --member=serviceAccount:{your-project-number}@cloudbuild.gserviceaccount.com --role=roles/iam.serviceAccountUser

  gcloud projects add-iam-policy-binding {your-project-id} \
  --member=serviceAccount:{your-project-number}@cloudbuild.gserviceaccount.com --role=roles/run.admin