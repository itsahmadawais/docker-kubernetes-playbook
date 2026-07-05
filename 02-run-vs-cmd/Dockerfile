FROM python:3.14

RUN apt-get update
RUN apt-get install -y curl

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]