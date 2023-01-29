# FROM gcr.io/deeplearning-platform-release/sklearn-cpu.0-23
FROM python:3.10-slim
WORKDIR /
COPY . .

# COPY model_training.py /app/model_training.py
# COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
ENTRYPOINT ["python3","model_training.py"]