FROM python:3.13


ENV PYTHONUNBUFFERED=1
ENV DOCKER_BUILDKIT=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /home/dev/app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
