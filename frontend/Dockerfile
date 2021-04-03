FROM node:14-alpine

COPY . /app
WORKDIR /app

#REVIEW look at avoiding this update
RUN npm install -g npm@latest

RUN npm install

RUN npm run build

EXPOSE 5000

ENV HOST=0.0.0.0

CMD [ "npm", "start" ]
