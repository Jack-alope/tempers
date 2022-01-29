FROM node:16-alpine

COPY . /app
WORKDIR /app

RUN npm ci

RUN npm run build

EXPOSE 8080

ENV HOST=0.0.0.0

CMD [ "npm", "start" ]
