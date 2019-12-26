FROM node:10
WORKDIR /usr/src/
COPY web-app/package*.json ./
RUN npm install