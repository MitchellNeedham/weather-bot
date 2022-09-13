FROM node:lts AS frontend-base
WORKDIR /usr/src/client

FROM frontend-base AS frontend-install
COPY package.json .
RUN npm install

FROM frontend-install AS frontend-dev
COPY . .