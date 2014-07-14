
from google.appengine.ext import ndb
import main_handlers

class PlayHandler(main_handlers.BaseHandler):
  def get_template(self):
    return "templates/play.html"

  def update_values(self, player, base_values):
    return

  def post(self):
    """ Receives the updated round scores from a player after they complete a round. """
    self.redirect(self.request.referer)


class GamesHandler(main_handlers.BaseHandler):
  def get_template(self):
    return "templates/games.html"

  def update_values(self, player, base_values):
    return
