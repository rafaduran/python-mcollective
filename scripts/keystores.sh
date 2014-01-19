#!/usr/bin/env bash
set -eu

SSLDIR=$(sudo puppet master --configprint ssldir)
PASSWORD=marionette

sudo puppet cert generate activemq.example.com

cd /opt
cp $SSLDIR/certs/ca.pem .
cp $SSLDIR/certs/activemq.example.com.pem activemq_cert.pem
cp $SSLDIR/private_keys/activemq.example.com.pem activemq_private.pem

sudo keytool -import -alias "My CA" -file ca.pem -keystore truststore.jks \
    -storepass $PASSWORD -noprompt

sudo cat activemq_private.pem activemq_cert.pem > temp.pem
sudo openssl pkcs12 -export -in temp.pem -out activemq.p12 \
    -name activemq.example.com -password pass:$PASSWORD

sudo keytool -importkeystore  -destkeystore keystore.jks \
    -srckeystore activemq.p12 -srcstoretype PKCS12 -alias activemq.example.com \
    -srcstorepass $PASSWORD -deststorepass $PASSWORD

cd -
