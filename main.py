#!/usr/bin/env python

from datetime import datetime
import logging
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Gift(db.Model):
    gift_from = db.StringProperty(required=True)
    gift_to = db.StringProperty(required=True)
    queued_on = db.DateTimeProperty( auto_now_add=True)
    opened_on = db.DateTimeProperty()

    def __repr__(self):
        return "<Gift to: %s from: %s>" % (self.gift_to, self.gift_from)
     
 
class MyHandler(webapp.RequestHandler):
    def get(self):
        queued_gifts = db.GqlQuery('SELECT * FROM Gift WHERE opened_on = NULL ORDER BY queued_on')
        gifts = list(queued_gifts)

        if not gifts:
            gifts = [""]

        values = { 
            'opening_now' : gifts[0],
            'queued_gifts' : gifts[1:],
        }
        self.response.out.write(template.render('main.html', values))

    def post(self):

        gift = Gift(
            gift_from=self.request.get('gift_from'),
            gift_to=self.request.get('gift_to')
        )
        gift.put()
        self.redirect('/')

class GiftOpenHandler(webapp.RequestHandler):
    def post(self):

        for gift_id in self.request.get_all('on_deck'):
            gift = Gift.get_by_id(int(gift_id))
            logging.debug(gift)
            gift.opened_on = datetime.now() 
            gift.put()
        self.redirect('/')


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    app = webapp.WSGIApplication([(r'/', MyHandler), (r'/open', GiftOpenHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()
