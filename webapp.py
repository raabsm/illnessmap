import tornado.ioloop
import tornado.web
import api_keys
import json
from mongodb_connection import MongoConnection
from bson.objectid import ObjectId
from bson.json_util import dumps


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
        self.render('restaurant.html', start_time=start_time,
                                        end_time=end_time,
                                        review_bottom_threshold=review_bottom_threshold,
                                        review_top_threshold=review_top_threshold,
                                        business_id=business_id)


class GetRestuarantInfo(tornado.web.RequestHandler):
    def get(self):
        id = self.get_query_argument('business_id')
        info = get_rest_info(id)
        self.write(info)


def make_app():
    return tornado.web.Application([
                    (r"/", MainHandler),
                    (r"/restaurant_info", RestaurantHandler),
                    (r"/get_restaurant_info", GetRestuarantInfo),
                    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "/home/smr2218/datafiles/"}),
                    (r"/images/(.*)", tornado.web.StaticFileHandler, {"path": "/home/smr2218/datafiles/images"}),
                    (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": "/home/smr2218/research/css/"})
                        ])


def init_mongo():
    global db
    db = MongoConnection('FoodIllness', api_keys.MongoDBURI)


def get_rest_info(id):
    collection = db.return_collection('MergedRestaurantReviews')
    rest_info = collection.find_one({'_id': id})
    return rest_info


if __name__ == "__main__":
    init_mongo()
    app = make_app()
    app.listen(9898)
    tornado.ioloop.IOLoop.current().start()
