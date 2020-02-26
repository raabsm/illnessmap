import tornado.ioloop
import tornado.web
import api_keys
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('geo_map.html', API_KEY=api_keys.Google_Maps_API_KEY)


def make_app():
    return tornado.web.Application([
                    (r"/", MainHandler),
                    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "/home/smr2218/datafiles/"}),
                        ])


if __name__ == "__main__":
    app = make_app()
    app.listen(9898)
    tornado.ioloop.IOLoop.current().start()
