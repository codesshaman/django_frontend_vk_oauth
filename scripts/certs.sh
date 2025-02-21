#!/bin/bash

HOST="$(grep 'ALLOWED_HOST' .env | cut -d '=' -f2 | tr -d '[:space:]')"

[ ! -d certs ] && mkdir certs && chmod u+rwx certs

cd certs

openssl req -x509 -newkey rsa:2048 \
    -keyout key.pem -out cert.pem \
    -days 365 -nodes \
    -subj "/CN=${HOST}"

ls -lah && cd ..
