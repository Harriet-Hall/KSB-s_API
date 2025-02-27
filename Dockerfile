FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

# RUN --mount=type=secret,id=USERNAME \
#   --mount=type=secret,id=DATABASE \
#   --mount=type=secret,id=HOST \
#   --mount=type=secret,id=PORT \
#   --mount=type=secret,id=PASSWORD \
#   --mount=type=secret,id=POSTGRES_DATABASE \
#   --mount=type=secret,id=POSTGRES_HOST \
#   --mount=type=secret,id=POSTGRES_USER \
#   --mount=type=secret,id=POSTGRES_PASSWORD \
#   --mount=type=secret,id=POSTGRES_PORT \
#   echo "./private-install-script --username $(cat /run/secrets/USERNAME) --database $(cat /run/secrets/DATABASE) --host $(cat /run/secrets/HOST) --port $(cat /run/secrets/PORT) --password $(cat /run/secrets/PASSWORD) --test-database $(cat /run/secrets/POSTGRES_DATABASE) --test-host $(cat /run/secrets/POSTGRES_HOST) --test-user $(cat /run/secrets/POSTGRES_USER) --test-password $(cat /run/secrets/POSTGRES_PASSWORD) --test-port $(cat /run/secrets/POSTGRES_PORT)"



RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/

EXPOSE 5000

ENV FLASK_APP=app.app
ENV FLASK_RUN_HOST=0.0.0.0


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
