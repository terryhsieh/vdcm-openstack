#!/bin/bash

# Settings
. settings

apt-get install -y --force-yes glance python-mysqldb mysql-client curl python-httplib2

# Glance Setup
mysql -h $MYSQL_HOST -u root -p$MYSQL_ROOT_PASS -e 'DROP DATABASE IF EXISTS glance;'
mysql -h $MYSQL_HOST -u root -p$MYSQL_ROOT_PASS -e 'CREATE DATABASE glance;'

echo "GRANT ALL ON glance.* TO 'glance'@'%' IDENTIFIED BY '$MYSQL_GLANCE_PASS'; FLUSH PRIVILEGES;" | mysql -h $MYSQL_HOST -u root -p$MYSQL_ROOT_PASS

sed -e "s,%SERVICE_TOKEN%,$SERVICE_TOKEN,g" glance-registry.conf.tmpl > glance-registry.conf
sed -e "s,%MYSQL_HOST%,$MYSQL_HOST,g" -i glance-registry.conf
sed -e "s,%MYSQL_GLANCE_PASS%,$MYSQL_GLANCE_PASS,g" -i glance-registry.conf
sed -e "s,%SERVICE_TOKEN%,$SERVICE_TOKEN,g" glance-api.conf.tmpl > glance-api.conf

service glance-api stop
service glance-registry stop

sleep 2

cp glance-registry.conf glance-api.conf /etc/glance/

chown glance:glance /etc/glance/glance-registry.conf
chown glance:glance /etc/glance/glance-api.conf

glance-manage db_sync

service glance-api start
sleep 2
service glance-registry start
sleep 2

./glance-upload-ttylinux.sh
#./glance-upload-oneiric.sh
#./glance-upload-loader.sh
#./glance-upload-lucid-loader.sh


