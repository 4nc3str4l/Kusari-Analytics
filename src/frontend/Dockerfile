FROM node:15.12.0-alpine3.13

RUN mkdir -p /opt/app/src/dist
RUN apk add coreutils

ADD package.json /opt/app/package.json
ADD webpack.config.js /opt/app/webpack.config.js
ADD start.sh /opt/app/start.sh

WORKDIR /opt/app
ENTRYPOINT ["stdbuf", "-o0", "/opt/app/start.sh"]
