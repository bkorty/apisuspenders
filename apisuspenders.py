import logging

from tornado import ioloop


logger = logging.getLogger('Suspenders')


class Suspenders(object):

    def __init__(self, app, ioloop, **settings):
        self.app = app
        self.ioloop = ioloop

    def process_retries(self):
        try:
            logger.info("process_retries")
        finally:
            self.ioloop.call_later(1, self.process_retries)


def install(app, **kwargs):
    iol = ioloop.IOLoop.instance()
    setattr(app, 'suspenders', Suspenders(app, iol))
    iol.call_later(1, app.suspenders.process_retries)