#!/bin/bash

mongoimport --host $HOST --port $PORT --db $DB --collection Restaurants --file $RESTAURANTSFILE
mongoimport --host $HOST --port $PORT --db $DB --collection Reviews --file $REVIEWSFILE

mongo $HOST:$PORT --eval "var dbName = '$DB'" initdb.js


python3 -u script.py

