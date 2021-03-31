FROM python:3.9.2-alpine3.13

ADD wait-for /opt/wait-for
RUN mkdir -p /opt/app/src
ADD requirements.txt /opt/app/requirements.txt
RUN pip3 install -r /opt/app/requirements.txt
WORKDIR /opt/app/src

ENTRYPOINT ["/opt/wait-for", "rabbit:5672", "--", "python3", "-u", "/opt/app/src/main.py"]
