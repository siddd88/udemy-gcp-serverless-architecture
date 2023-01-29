import json
from google.cloud import aiplatform

PROJECT_ID = '{your-project-id}'
REGION = 'us-east1'
PIPELINE_ROOT = 'gs://vertex-ai-udemy/cc-fraud-kfpl'

def trigger_pipeline():
   pipeline_spec_uri = "gs://vertex-ai-udemy/adclick-model-kubeflow-pipeline/cc-fraud-pipeline.json"
   aiplatform.init(
       project=PROJECT_ID,
       location=REGION,
   )

   job = aiplatform.PipelineJob(
       display_name=f'cc-model-pipeline',
       template_path=pipeline_spec_uri,
       pipeline_root=PIPELINE_ROOT,
       enable_caching=False
   )
   job.submit()

trigger_pipeline()

# To run this using app engine or cloud functions , include the below modules in requirements.txt 
# google-api-python-client>=1.7.8,<2
# google-cloud-aiplatform