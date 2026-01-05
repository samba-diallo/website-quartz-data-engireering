FROM node:21.7.3@sha256:4b232062fa976e3a966c49e9b6279efa56c8d207a67270868f51b3d155c4e33d

WORKDIR /home/node/app

COPY package.json .
COPY app.js .

EXPOSE 8080

USER node

CMD ["npm", "start"]
