# First Approach

# Step-1 - Build the image 
docker build -t test-app .

# Step-2 - Test the image locally 
docker run -p 8081:8081 test-app

# Step-3 - Tag the image locally 
docker tag demo-app-cloudrun gcr.io/{your-project-id}/test-app

# Step-4 - Push the image to Google Cloud Registry 
docker push gcr.io/{your-project-id}}/test-app

# Deply to Cloud Run 
gcloud run deploy python-bigquery-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --max-instances 4 \
  --min-instances 2 