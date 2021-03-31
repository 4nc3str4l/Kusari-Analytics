FROM golang:1.16.2-buster

RUN mkdir -p /opt/app/src
ENV GOBIN /go/bin

RUN go env -w GO111MODULE=auto
RUN go get -u github.com/gorilla/websocket

WORKDIR /opt/app/src

ENTRYPOINT ["go", "run", "."]
