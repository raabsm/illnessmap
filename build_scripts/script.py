import sys
import os
import schedule
import time
from update_locs import add_location_data
from pymongo import MongoClient
import requests


def connect_and_update_db():
    db_name = os.environ['DB']
    collection_restaurants = os.environ['COLLECTION_RESTAURANTS_JOIN_EXTRA_FIELD']
    collection_lat_long = os.environ['COLLECTION_RESTAURANTS_EXTRA_FIELD']

    try:
        db = MongoClient(os.environ['URI'])[db_name]

        try:
            collection_restaurants = db[collection_restaurants]
            collection_lat_long = db[collection_lat_long]
            add_location_data(collection_restaurants, collection_lat_long)

            print("Ran add location")
        except Exception as e:
            print("error when getting Restaurant collections", e)
    except Exception as e:
        print('Error while connecting to DB: ', e)


def update_webapp_data():
    try:
        requests.get('http://webapp:9898/update_reviews')
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("didn't work yet")



if __name__ == '__main__':
    schedule.every().day.do(connect_and_update_db)
    schedule.every().day.do(update_webapp_data)
    connect_and_update_db()
    while True:
        schedule.run_pending()
        time.sleep(1)
