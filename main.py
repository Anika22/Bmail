#!/usr/bin/env python
import os
import jinja2
import webapp2
from google.appengine.api import users
from models import Messages
import json
from google.appengine.api import urlfetch


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logged_in = True
            logout_url = users.create_logout_url("/")
            params = {"logged_in":logged_in, "logout_url":logout_url, "user":user}
            return self.render_template("received_messages.html", params=params)
        else:
            logged_in = False
            login_url = users.create_login_url("/")
            params = {"logged_in":logged_in, "login_url":login_url, "user":user}
        return self.render_template("login.html", params=params)

class NewMessageHandler(MainHandler):
    def get(self):
        return self.render_template("new_message.html")

    def post(self):
        sender = self.request.get("sender")
        receiver = self.reques.get("receiver")
        sent_message = self.request.get("sent_message")
        sent_messages = Messages(sender=sender, receiver=receiver, message=sent_message)
        sent_messages.put()
        return self.render_template("sent_messages.html")



class ReceivedMessagesHandler(MainHandler):
    def get(self):
        return self.render_template("received_messages.html")

class SentMessagesHandler(MainHandler):
    def get(self):
        list_sent_messages = Messages.query(Messages.receiver == "user").fetch()
        params={"list_sent_messages": list_sent_messages}
        return self.render_template("sent_messages.html", params=params)

class WeatherHandler(BaseHandler):
    def get(self):
        url_lj = "http://api.openweathermap.org/data/2.5/weather?q=Ljubljana,si&units=metric&appid=1a7a8316bbdf86386242c6b2271524f0"
        result_lj = urlfetch.fetch(url_lj)
        vreme_lj = json.loads(result_lj.content)
        url_mb = "http://api.openweathermap.org/data/2.5/weather?q=maribor,si&units=metric&appid=1a7a8316bbdf86386242c6b2271524f0"
        result_mb = urlfetch.fetch(url_mb)
        vreme_mb = json.loads(result_mb.content)
        url_kp = "http://api.openweathermap.org/data/2.5/weather?q=Koper,si&units=metric&appid=1a7a8316bbdf86386242c6b2271524f0"
        result_kp = urlfetch.fetch(url_kp)
        vreme_kp = json.loads(result_kp.content)
        params={"vreme_kp":vreme_kp, "vreme_lj":vreme_lj, "vreme_mb":vreme_mb}
        return self.render_template("weather.html", params=params)

class ProfileHandler(MainHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logged_in = True
            params={"user":user, "logged_in":logged_in}
        return self.render_template("profile.html", params=params)



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/received_messages', MainHandler),
    webapp2.Route('/new_message', NewMessageHandler),
    webapp2.Route('/sent_messages', SentMessagesHandler),
    webapp2.Route('/weather', WeatherHandler),
    webapp2.Route('/profile', ProfileHandler),
], debug=True)
