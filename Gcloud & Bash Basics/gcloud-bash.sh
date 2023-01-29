#Authenticate your GCP Account 
gcloud auth login 

#Set Default project-id 
gcloud config set project {PROJECT_ID}

# Test your config settings 
gcloud config list

# List of all the projects in your GCP Account 
gcloud projects list

# Get Current project 
gcloud config get-value project

# Save the result of the above cmd in a variable  
export PROJECT_ID=$(gcloud config get-value project)

#Create a new variable called BUCKET_NAME 
export BUCKET_NAME="${PROJECT_ID}-test-bucket"

# Create a New GCP Storage Bucket 
gsutil mb -p ${PROJECT_ID} gs://${BUCKET_NAME}
