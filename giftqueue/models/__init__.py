from google.appengine.ext import db

class Gift(db.Model):
    gift_from = db.StringProperty(required=True)
    gift_to = db.StringProperty(required=True)
    queued_on = db.DateTimeProperty( auto_now_add=True)
    opened_on = db.DateTimeProperty()
    gift_name = db.StringProperty(required=False)

    def __repr__(self):
        return "<Gift to: %s from: %s>" % (self.gift_to, self.gift_from)