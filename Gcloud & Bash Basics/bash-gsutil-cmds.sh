# List all the content in your current directory 
ls -l 

# Get your current directory path
pwd

#Create a new file called "files_to_upload.txt"
touch files_to_upload.txt

# Write some data into it 
echo "this is the 1st line" > files_to_upload.txt

# Write new data into it 
echo "this is the 2nd line" > files_to_upload.txt

# Append data into the file 
echo "this is the 3rd line" >> files_to_upload.txt

echo "this is the 3rd line" >> files_to_upload2.txt

# Upload the file using cp command 
gsutil cp files_to_upload.txt gs://${BUCKET_NAME}

# Upload multiple files using cp command 
gsutil cp *.txt gs://${BUCKET_NAME}

# Download multiple files from GCS Bucket 
gsutil cp -R gs://${BUCKET_NAME} .

# Download multiple files from GCS Bucket using multi-threading 
gsutil -m cp -R gs://${BUCKET_NAME} .