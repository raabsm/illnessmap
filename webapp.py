import tornado.ioloop
import tornado.web
import api_keys
import json
from mongodb_connection import MongoConnection
from bson.json_util import dumps
import time
import schedule

global data, db


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('geo_map.html', API_KEY=api_keys.Google_Maps_API_KEY)


class RestaurantHandler(tornado.web.RequestHandler):
    def post(self):
        business_id = self.get_argument('business_id')
        start_time = self.get_argument('start_time')
        end_time = self.get_argument('end_time')
        review_bottom_threshold = self.get_argument('review_bottom_threshold')
        review_top_threshold = self.get_argument('review_top_threshold')
        self.render('restaurant.html',
                    start_time=start_time,
                    end_time=end_time,
                    review_bottom_threshold=review_bottom_threshold,
                    review_top_threshold=review_top_threshold,
                    business_id=business_id)


class GetRestuarantInfo(tornado.web.RequestHandler):
    def get(self):
        id = self.get_query_argument('business_id')
        info = get_rest_info(id)
        self.write(info)


class GetReviews(tornado.web.RequestHandler):
    def get(self):
        self.write(data)
        schedule.run_pending()


def get_newest_reviews():
    print("Querying DB...")
    global data
    collection = db.return_collection(api_keys.DB_INFO['collections']['condensed_reviews'])
    data = collection.find({})
    data = dumps(data)
    print("Data updated")


schedule.every().day.do(get_newest_reviews)


def init_mongo():
    global db
    db = MongoConnection(api_keys.DB_INFO['db'], api_keys.DB_INFO['uri'])


def get_rest_info(id):
    collection = db.return_collection(api_keys.DB_INFO['collections']['all_reviews'])
    rest_info = collection.find_one({'_id': id})
    return rest_info


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/restaurant_info", RestaurantHandler),
        (r"/get_reviews", GetReviews),
        (r"/get_restaurant_info", GetRestuarantInfo),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "/home/smr2218/datafiles/"}),
        (r"/images/(.*)", tornado.web.StaticFileHandler, {"path": "/home/smr2218/datafiles/images"}),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": "/home/smr2218/research/css/"}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": "/home/smr2218/research/js/"}),
    ])


if __name__ == "__main__":
    init_mongo()
    get_newest_reviews()
    app = make_app()
    app.listen(9898)
    print('running')
    tornado.ioloop.IOLoop.current().start()