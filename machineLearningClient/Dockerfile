FROM python:3.8
RUN pip install --upgrade pip
WORKDIR /app2
COPY requirements.txt /app2/
RUN pip install -r requirements.txt
COPY . /app2
CMD ["python", "./ml_client.py"]


