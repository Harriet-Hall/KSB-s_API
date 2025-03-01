FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV FLASK_APP=app.app.py 


FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /app/requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY --from=builder /app/app.py /app.py

EXPOSE 5000

ENV PYTHONPATH=/app
ENV FLASK_APP=app.app.py

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]