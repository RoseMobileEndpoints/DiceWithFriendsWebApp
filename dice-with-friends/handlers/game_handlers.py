
from google.appengine.ext import ndb
from google.appengine.api import users
import main
import main_handlers

class PlayHandler(main_handlers.BaseHandler):
    def load_page(self, player):
        template = main.jinja_env.get_template("templates/play.html")
        self.response.out.write(template.render({'player': player, 'logout_url': users.create_logout_url("/")}))

    def post(self):
        """ Receives the updated round scores from a player after they complete a round. """
        self.redirect(self.request.referer)


class GamesHandler(main_handlers.BaseHandler):
    def load_page(self, player):
        template = main.jinja_env.get_template("templates/games.html")
        self.response.out.write(template.render({'player': player, 'logout_url': users.create_logout_url("/")}))

    def post(self):
        """ Receives the updated round scores from a player after they complete a round. """
        self.redirect(self.request.referer)