# Deploy the App 
gcloud app deploy 

# Browse the deployed app 
gcloud app browse

# Check the versions and instance running for the app 
gcloud app versions list
gcloud app instances list 

# Get the URL for the app for a specific version
gcloud app browse --version {version_id}

# Split the traffic between different versions of the app .Defaults to split by IP addresses 
gcloud app services set-traffic --splits=20221128t143115=.5,v2=.5

# Split the traffic between different versions of the app by random and not by IP Addresses 
gcloud app services set-traffic splits=20221128t143115=.5,v2=.5 --split-by=random




