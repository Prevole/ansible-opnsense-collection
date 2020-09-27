FROM linuxserver/openssh-server:latest

RUN apk add --no-cache --virtual .build-deps py3-pip g++ gcc libxml2-dev libxslt-dev python3-dev && \
    apk add --no-cache python3 libxml2 libxslt && \
    pip install --no-cache-dir lxml && \
    apk del .build-deps
