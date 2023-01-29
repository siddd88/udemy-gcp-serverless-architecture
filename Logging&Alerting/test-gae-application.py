import requests,time,random

arr = [4854632,21100518,34876283,22596360,25962612]

while True : 

    app_endpoint = 'https://python-bq-application-dot-gcp-serverless-project-374110.uc.r.appspot.com/?post_id='+str(random.choice(arr))

    r = requests.get(app_endpoint)

    print(r.status_code,r.text)
    time.sleep(5)
    