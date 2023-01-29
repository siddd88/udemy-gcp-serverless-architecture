from google.cloud import aiplatform
import os
from google.cloud.aiplatform.prediction import LocalModel
from src_dir.predictor import AdClickPredictor


REGION = "us-east1"
MODEL_ARTIFACT_DIR = "adclick-model-artifact" 
REPOSITORY = "vertexai-repo" # Change this to your artifact reg name 
IMAGE = "sklearn-image"
MODEL_DISPLAY_NAME = "adclick-model"

PROJECT_ID = "{your-project-id}"
BUCKET_NAME = "gs://{your-bucket-name}"

aiplatform.init(project=PROJECT_ID, location=REGION)

local_model = LocalModel.build_cpr_model(
    "src_dir",
    f"{REGION}-docker.pkg.dev/{PROJECT_ID}/{REPOSITORY}/{IMAGE}",
    predictor=AdClickPredictor,
    requirements_path=os.path.join("src_dir", "requirements.txt"),
)

# import json

# sample = {"instances": [
#   ['63.95','23','52182','40',1]
# ]}

# with open('instances.json', 'w') as fp:
#     json.dump(sample, fp)


with local_model.deploy_to_local_endpoint(
    artifact_uri = 'model_artifacts/',
) as local_endpoint:
    predict_response = local_endpoint.predict(
        request_file='instances.json',
        headers={"Content-Type": "application/json"},
    )
    health_check_response = local_endpoint.run_health_check()

local_model.push_image()

model = aiplatform.Model.upload(local_model = local_model,
                                display_name=MODEL_DISPLAY_NAME,
                                artifact_uri=f"{BUCKET_NAME}/{MODEL_ARTIFACT_DIR}",)

endpoint = model.deploy(machine_type="n1-standard-2",)

endpoint.predict(instances=[[63.95,44,52182,52182,1]])

# Optional 
endpoint = model.deploy(
     deployed_model_display_name='endpoint-name',
     traffic_split={"0": 100},
     machine_type="n1-standard-4",
     accelerator_count=0,
     min_replica_count=1,
     max_replica_count=1,
   )

# Batch Prediction code start
from typing import Dict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

ENDPOINT_ID="{your-endpoint-id}"
PROJECT_ID="{your-project-id}"

def predict_data(
    project: str,
    endpoint_id: str,
    instance_dict: Dict,
    location: str = "us-east1",
    api_endpoint: str = "us-east1-aiplatform.googleapis.com"):
    client_options = {"api_endpoint": api_endpoint}

    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    instance = json_format.ParseDict(instance_dict, Value())
    instances = [instance]
    
    endpoint = client.endpoint_path(project=project, location=location, endpoint=endpoint_id)

    response = client.predict(endpoint=endpoint, instances=instances)
    
    predictions = response.predictions
    
    print(predictions)


json_input = ['63.95','23','52182','40',1]
predict_data(PROJECT_ID,ENDPOINT_ID,json_input)


# Batch Prediction code ends

