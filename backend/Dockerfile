# syntax=docker/dockerfile:1
FROM python:3 AS backend-base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/server

FROM backend-base AS backend-install
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM backend-install AS backend-dev
COPY . .


