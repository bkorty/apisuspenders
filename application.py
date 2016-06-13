from tornado import web

import sprockets.http

import apisuspenders

def make_default_app(**settings):
    app = web.Application([], **settings)
    apisuspenders.install(app)

    return app


if __name__ == '__main__':
    sprockets.http.run(make_default_app,
                       settings={"debug": True})