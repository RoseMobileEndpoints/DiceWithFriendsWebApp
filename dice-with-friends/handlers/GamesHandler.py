
from google.appengine.ext import ndb
import webapp2

import main


class GamesHandler(webapp2.RequestHandler):
    def get(self):
        template = main.jinja_env.get_template("templates/games.html")
        self.response.out.write(template.render({'placeholder': None}))

    def post(self):
        """ Receives the updated round scores from a player after they complete a round. """
        self.redirect(self.request.referer)