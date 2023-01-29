import requests
post_request = {
                    "daily_time_spent":500,
                    "age":23,
                    "area_income":45000,
                    "daily_internet_usage":45,
                    "male":1
                }
prediction_endpoint = 'https://classification-model-prediction-dot-gcp-serverless-project.uc.r.appspot.com'

r = requests.post(prediction_endpoint, json=post_request)

print(r.status_code,r.text)