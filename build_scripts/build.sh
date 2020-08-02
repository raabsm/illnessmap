#!/bin/bash

REVIEWSFILE="$1"
RESTAURANTSFILE="$2"

mongoimport --host $HOST --port $PORT --db $DB --collection Restaurants --drop --file $RESTAURANTSFILE
mongoimport --host $HOST --port $PORT --db $DB --collection Reviews --drop --file $REVIEWSFILE

mongo $HOST:$PORT --eval "var dbName = '$DB'" initdb.js


python3 -u script.py

