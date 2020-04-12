import tornado.ioloop
import tornado.web
import api_keys
import json

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
        print(business_id, start_time, end_time, review_bottom_threshold, review_top_threshold)
        self.render('restaurant.html', start_time=start_time,
                                        end_time=end_time,
                                        review_bottom_threshold=review_bottom_threshold,
                                        review_top_threshold=review_top_threshold,
                                        business_id=business_id)

class test(tornado.web.RequestHandler):
    def get(self):
        self.render('map.html', API_KEY=api_keys.Google_Maps_API_KEY)


def make_app():
    return tornado.web.Application([
                    (r"/", MainHandler),
                    (r"/restaurant_info", RestaurantHandler),
                    (r"/test", test),
                    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "/home/smr2218/datafiles/"}),
                        ])


if __name__ == "__main__":
    app = make_app()
    app.listen(9898)
    tornado.ioloop.IOLoop.current().start()
