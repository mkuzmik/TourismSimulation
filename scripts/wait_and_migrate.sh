#/bin/bash

while ! nc -z tourism_database 5432;
do
  echo sleeping;
  sleep 1;
done;
echo Connected!;
sleep 5;
echo 'Migrating'

yoyo apply --config ../yoyo.ini