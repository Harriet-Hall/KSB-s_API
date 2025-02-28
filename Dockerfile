FROM python:3.9-slim


WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000

ENV PYTHONPATH=/app
ENV FLASK_APP=app.app.py 

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]


