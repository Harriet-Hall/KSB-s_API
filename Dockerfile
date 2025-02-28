FROM python:3.9-slim

WORKDIR /

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
