import tornado.ioloop
import tornado.web
import api_keys

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('map.html', API_KEY=api_keys.Google_Maps_API_KEY)


def make_app():
    return tornado.web.Application([
                    (r"/", MainHandler),
                        ])


if __name__ == "__main__":
    app = make_app()
    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()
