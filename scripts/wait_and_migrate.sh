#/bin/bash

while ! nc -z tourism_database 5432;
do
  echo sleeping;
  sleep 1;
done;
echo Connected!;

yoyo apply --config ../yoyo.ini