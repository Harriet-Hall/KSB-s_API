FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN --mount=type=secret,id=USERNAME \
  --mount=type=secret,id=DATABASE \
  --mount=type=secret,id=HOST \
  --mount=type=secret,id=PORT \
  --mount=type=secret,id=PASSWORD \
  --mount=type=secret,id=TEST_DATABASE \
  --mount=type=secret,id=TEST_HOST \
  --mount=type=secret,id=TEST_USER \
  --mount=type=secret,id=TEST_PASSWORD \
  --mount=type=secret,id=TEST_PORT \
  --mount=type=secret,id=POSTGRES_USER \
  --mount=type=secret,id=POSTGRES_PASSWORD \
  --mount=type=secret,id=POSTGRES_DATABASE \
  echo "./private-install-script --username $(cat /run/secrets/USERNAME) --database $(cat /run/secrets/DATABASE) --host $(cat /run/secrets/HOST) --port $(cat /run/secrets/PORT) --password $(cat /run/secrets/PASSWORD) --test-database $(cat /run/secrets/TEST_DATABASE) --test-host $(cat /run/secrets/TEST_HOST) --test-user $(cat /run/secrets/TEST_USER) --test-password $(cat /run/secrets/TEST_PASSWORD) --test-port $(cat /run/secrets/TEST_PORT) --postgres-user $(cat /run/secrets/POSTGRES_USER) --postgres-password $(cat /run/secrets/POSTGRES_PASSWORD) --postgres-database $(cat /run/secrets/POSTGRES_DATABASE)"



RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/

EXPOSE 5000

ENV FLASK_APP=app.app
ENV FLASK_RUN_HOST=0.0.0.0


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
