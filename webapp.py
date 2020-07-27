import tornado.ioloop
import tornado.web
import os
from pymongo import MongoClient
from bson.json_util import dumps

global data, db


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('geo_map.html', API_KEY=os.environ['GOOGLE_MAPS_API_KEY'])


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
        print(type(info))
        print(info)
        self.write(info)


class GetReviews(tornado.web.RequestHandler):
    def get(self):
        self.write(data)


class UpdateReviews(tornado.web.RequestHandler):
    def get(self):
        get_newest_reviews()


def get_newest_reviews():
    print("Querying DB...")
    global data
    collection = db[os.environ['COLLECTION_NEWEST_REVIEWS']]
    data = collection.find({})
    data = dumps(data)
    print("Data updated")


def init_mongo():
    global db
    db = MongoClient(os.environ['URI'])[os.environ['DB']]


def get_rest_info(id):
    collection = db[os.environ['COLLECTION_ALL_REVIEWS']]
    rest_info = collection.find_one({'_id': id})
    return rest_info


def make_app():
    pwd = os.environ['PWD']
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/restaurant_info", RestaurantHandler),
        (r"/get_reviews", GetReviews),
        (r"/get_restaurant_info", GetRestuarantInfo),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": pwd + "/datafiles/"}),
        (r"/images/(.*)", tornado.web.StaticFileHandler, {"path": pwd + "/datafiles/images"}),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": pwd + "/css/"}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": pwd + "/js/"})
    ])


if __name__ == "__main__":
    init_mongo()
    get_newest_reviews()
    app = make_app()
    app.listen(9898)
    print('running')
    tornado.ioloop.IOLoop.current().start()
