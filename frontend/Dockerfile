FROM node:12-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
RUN npm install -g @angular/cli
COPY . .
