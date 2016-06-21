from google.appengine.ext import ndb

class Messages(ndb.Model):
    receiver = ndb.StringProperty(required=True)
    sender = ndb.StringProperty(required=True)
    sent_message = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

