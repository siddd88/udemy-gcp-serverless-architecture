import requests,time,random

arr = [4854632,21100518,34876283,22596360,25962612]

while True : 

    app_endpoint = 'https://python-bigquery-api-3y7amv5w2a-uc.a.run.app?post_id='+str(random.choice(arr))

    r = requests.get(app_endpoint)

    print(r.status_code,r.text)
    time.sleep(1)
    