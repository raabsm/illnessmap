import tornado.ioloop
import tornado.web
import os
from pymongo import MongoClient
from bson.json_util import dumps

global data, db

reviews_with_sentence_errors = {}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('html/geo_map.html', API_KEY=os.environ['GOOGLE_MAPS_API_KEY'])


class RestaurantHandler(tornado.web.RequestHandler):
    def post(self):
        business_id = self.get_argument('business_id')
        start_time = self.get_argument('start_time')
        end_time = self.get_argument('end_time')
        review_bottom_threshold = self.get_argument('review_bottom_threshold')
        review_top_threshold = self.get_argument('review_top_threshold')
        self.render('html/restaurant.html',
                    start_time=start_time,
                    end_time=end_time,
                    review_bottom_threshold=review_bottom_threshold,
                    review_top_threshold=review_top_threshold,
                    business_id=business_id)


class GetRestuarantInfo(tornado.web.RequestHandler):
    def get(self):
        id = self.get_query_argument('business_id')
        info = get_rest_info(id)
        # json_string = dumps(info, ensure_ascii=False).encode('utf8')
        # print(info)
        self.write(info)


class GetReviews(tornado.web.RequestHandler):
    def get(self):
        self.write(data)


class UpdateReviews(tornado.web.RequestHandler):
    def get(self):
        get_newest_reviews()
        self.write("Completed")


class ReviewSentenceError(tornado.web.RequestHandler):
    def post(self):
        review_id = self.get_argument('review_id')
        to_insert = {
            'review_id': review_id,
            'sentences_split_length': self.get_argument('sentences_split_length'),
            'sentence_scores_length': self.get_argument('sentence_scores_length')
        }
        global reviews_with_sentence_errors
        if review_id not in reviews_with_sentence_errors:
            reviews_with_sentence_errors[review_id] = to_insert


class GetReviewsWithSentenceErrors(tornado.web.RequestHandler):
    def get(self):
        self.write(dumps(reviews_with_sentence_errors))


def get_newest_reviews():
    print("Querying DB...")
    try:
        init_mongo()
        collection = db[os.environ['COLLECTION_NEWEST_MERGED_REVIEWS']]
        temp = collection.find({})
    except Exception as e:
        print("could not reload data:", e)
        temp = []

    global data
    data = dumps(temp)
    print("Data updated")


def init_mongo():
    global db
    db = MongoClient(os.environ['URI'])[os.environ['DB']]


def get_rest_info(id):
    # collection = db[os.environ['COLLECTION_ALL_MERGED_REVIEWS']]
    collection = db['Restaurants']
    rest_info = collection.aggregate([
        {
            '$match': {
                '_id': id
            },
        },
        {
            '$lookup': {
                'from': 'AllSickReviews',
                'localField': '_id',
                'foreignField': 'business_id',
                'as': 'reviews'
            }
        }
    ])
    return list(rest_info)[0]


def make_app():
    pwd = os.getcwd()
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/log_sentence_error", ReviewSentenceError),
        (r"/get_sentence_errors", GetReviewsWithSentenceErrors),
        (r"/restaurant_info", RestaurantHandler),
        (r"/get_reviews", GetReviews),
        (r"/get_restaurant_info", GetRestuarantInfo),
        (r"/update_data", UpdateReviews),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": pwd + "/datafiles/"}),
        (r"/images/(.*)", tornado.web.StaticFileHandler, {"path": pwd + "/datafiles/images"}),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": pwd + "/css/"}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": pwd + "/js/"})
    ])


if __name__ == "__main__":
    get_newest_reviews()
    app = make_app()
    app.listen(int(os.environ['WEBAPP_PORT']))
    print('running')
    tornado.ioloop.IOLoop.current().start()