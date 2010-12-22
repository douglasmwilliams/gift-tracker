from datetime import datetime
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from giftqueue.models import Gift

class DashboardHandler(webapp.RequestHandler):
    def get(self):
        queued_gifts = db.GqlQuery('SELECT * FROM Gift WHERE opened_on = NULL ORDER BY queued_on')
        opened_gifts = db.GqlQuery('SELECT * FROM Gift WHERE opened_on != NULL')
        
        gifts = list(queued_gifts)
        gifts_opened_count = len(list(opened_gifts))
        
        if not gifts:
            gifts = [""]

        values = { 
            'opening_now' : gifts[0],
            'queued_gifts' : gifts[1:],
            'gifts_opened_count' : gifts_opened_count,
        }
        self.response.out.write(template.render('giftqueue/templates/base.html', values))


class AdminHandler(webapp.RequestHandler):
    def get(self):
        queued_gifts = db.GqlQuery('SELECT * FROM Gift WHERE opened_on = NULL ORDER BY queued_on')
        opened_gifts = db.GqlQuery('SELECT * FROM Gift WHERE opened_on != NULL')
        
        gifts = list(queued_gifts)
        gifts_opened_count = len(list(opened_gifts))
        
        if not gifts:
            gifts = [""]

        values = { 
            'opening_now' : gifts[0],
            'queued_gifts' : gifts[1:],
            'gifts_opened_count' : gifts_opened_count,
        }
        self.response.out.write(template.render('giftqueue/templates/admin.html', values))

class AddToQueueHandler(webapp.RequestHandler):
    def post(self):
        gift = Gift(
            gift_from=self.request.get('gift_from'),
            gift_to=self.request.get('gift_to')
        )
        gift.put()
        self.redirect('/admin')

class GiftOpenHandler(webapp.RequestHandler):
    def post(self):
        for gift_id in self.request.get_all('on_deck'):
            gift = Gift.get_by_id(int(gift_id))
            gift.opened_on = datetime.now() 
            gift.put()
        self.redirect('/admin')

