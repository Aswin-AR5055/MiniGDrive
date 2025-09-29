FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 6000

CMD ["gunicorn", "-w", "2", "--threads", "2", "--preload", "-b", "0.0.0.0:6000", "routes:app"]

