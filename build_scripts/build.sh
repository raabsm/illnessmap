#!/bin/bash
source mongoconfig.sh

REVIEWSFILE="$1"
RESTAURANTSFILE="$2"

mongoimport --host $host --port $port --db FoodIllness --collection Restaurants --drop --file $RESTAURANTSFILE
mongoimport --host $host --port $port --db FoodIllness --collection Reviews --drop --file $REVIEWSFILE

mongo $host:$port initdb.js

#TODO -- setup environment

python add_sentences.py FoodIllness AllSickReviews Reviews

python update_locs.py FoodIllness Restaurants

