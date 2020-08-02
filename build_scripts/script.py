import sys
import os
import schedule
import time
from add_sentences import add_sentences_to_reviews
from update_locs import add_location_data
from pymongo import MongoClient


def connect_and_update_db():
    db_name = os.environ['DB']
    collection_restaurants = 'Restaurants'
    collection_reviews = "Reviews"
    collection_all_reviews = os.environ['COLLECTION_ALL_REVIEWS']

    try:
        db = MongoClient(os.environ['URI'])[db_name]

        try:
            collection_reviews = db[collection_reviews]
            collection_all_reviews = db[collection_all_reviews]
            add_sentences_to_reviews(collection_all_reviews, collection_reviews)

            print("Ran add sentences")

        except Exception as e:
            print("error when getting Review collections", e)

        try:
            collection_restaurants = db[collection_restaurants]
            add_location_data(collection_restaurants)

            print("Ran add location")
        except Exception as e:
            print("error when getting Restaurant collections", e)
    except Exception as e:
        print('Error while connecting to DB: ', e)



if __name__ == '__main__':
    schedule.every().day.do(connect_and_update_db)
    connect_and_update_db()
    while True:
        schedule.run_pending()
        time.sleep(1)
