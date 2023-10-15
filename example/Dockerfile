FROM node:20.2.0-alpine3.17 As development
WORKDIR /work-dir
ENV NODE_ENV development
COPY --chown=node:node . .
RUN npm install
RUN apk add git
EXPOSE 3000
CMD ["node", "index.js"]