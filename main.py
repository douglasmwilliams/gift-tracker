#!/usr/bin/env python

from datetime import datetime
import logging
import wsgiref.handlers


from giftqueue.handlers import *

def main():
    app = webapp.WSGIApplication(
      [
        (r'/admin', AdminHandler),
        (r'/open', GiftOpenHandler),
        (r'/add', AddToQueueHandler),
        (r'/dashboard', DashboardHandler),
      ], 
      debug=True
    )
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()
