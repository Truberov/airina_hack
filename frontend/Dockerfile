######################################### Frontend #########################################
FROM node:18-alpine as build-stage

WORKDIR /frontend

COPY package.json package-lock.json ./

RUN npm install

COPY ./ ./

RUN npm run build
