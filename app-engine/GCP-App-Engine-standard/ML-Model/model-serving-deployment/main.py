import pickle
import numpy as np 
from flask import Flask,request
import gcsfs

app = Flask(__name__)
@app.route("/",methods=["GET","POST"])

def main():

    input_path = "your-bucket-name/ad_model.pkl"
    model = load_model(input_path)
    if request.method=='POST' :
        input_data = request.get_json()
        daily_time_spent = input_data['daily_time_spent']
        age = input_data['age']
        area_income = input_data['area_income']
        daily_internet_usage = input_data['daily_internet_usage']
        male = input_data['male']
        input_arr = np.array([[daily_time_spent,age,area_income,daily_internet_usage,male]])

        predictions = model.predict(input_arr)
        return str(predictions)
    else : 
        return "Method not allowed"

def load_model(input_path):

    fs = gcsfs.GCSFileSystem()
    with fs.open(input_path, 'rb') as file:
        model = pickle.load(file)
        return model

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)