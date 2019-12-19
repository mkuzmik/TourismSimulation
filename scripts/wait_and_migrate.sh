#/bin/bash

while ! nc -z localhost 5432;
do
  echo sleeping;
  sleep 1;
done;
echo Connected!;
sleep 5;
echo 'Migrating'

yoyo apply --config ../yoyo.ini --database postgresql://root:admin@127.0.0.1:5432/tourism ../migrations -v
echo "dupa"