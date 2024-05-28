FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /iterio_project

COPY docker_functionality/entrypoint.sh docker_functionality/entrypoint.sh
COPY docker_functionality/wait-for-it.sh docker_functionality/wait-for-it.sh
COPY docker_functionality/requirements.txt docker_functionality/requirements.txt

RUN pip install --no-cache-dir -r docker_functionality/requirements.txt

COPY . .
