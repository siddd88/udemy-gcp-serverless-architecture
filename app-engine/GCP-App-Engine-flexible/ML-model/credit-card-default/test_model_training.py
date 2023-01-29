import requests
post_request = {
    "is_output_valid": 1,
    "total_attrbutes": 31    
}
prediction_endpoint = 'https://your-endpoint-url/'

r = requests.post(prediction_endpoint, json=post_request)

print(r.status_code,r.text)