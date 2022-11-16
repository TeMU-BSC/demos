FROM node:16
WORKDIR /app
COPY package.json ./
RUN npm install -g npm@9.1.1
RUN yarn global add @angular/cli
RUN yarn install
COPY . .
