FROM python:3.7
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
ENV HOST 0.0.0.0
ENTRYPOINT ["python", "app/main_flask.py"]
