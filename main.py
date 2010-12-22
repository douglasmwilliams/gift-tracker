#!/usr/bin/env python

import logging
import wsgiref.handlers
from google.appengine.ext import webapp

from giftqueue.handlers import AdminHandler, DashboardHandler, AddToQueueHandler, GiftOpenHandler

def main():
    logging.getLogger().setLevel(logging.DEBUG)

    app = webapp.WSGIApplication(
        [
            (r'/dashboard', DashboardHandler),
            (r'/admin', AdminHandler),
            (r'/open', GiftOpenHandler),
            (r'/add', AddToQueueHandler),
        ], 
        debug=True
    )

    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()
