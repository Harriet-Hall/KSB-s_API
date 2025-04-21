FROM python:3.9-slim AS builder

WORKDIR /app
ENV TZ="Europe/London"

COPY . .
RUN pip cache purge
RUN pip3 install -r requirements.txt
RUN date

ENV PYTHONPATH=/app
ENV FLASK_APP=app.app.py 
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

FROM python:3.9-slim AS production 

WORKDIR /app
ENV TZ="Europe/London"
COPY --from=builder app/requirements.txt app/requirements.txt
RUN pip3 install --no-cache-dir -r app/requirements.txt
RUN date

COPY --from=builder /app/app /app/app 

ENV ENVIRONMENT=production
ENV PYTHONPATH=/app
ENV FLASK_APP=app.app.py
EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]