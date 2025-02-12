FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY sentiment_analyzer.py sentiment_analyzer.py
COPY app.py app.py

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]