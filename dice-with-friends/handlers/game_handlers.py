from google.appengine.ext import ndb
from datetime import datetime
import main_handlers


class PlayHandler(main_handlers.BaseHandler):
  def get_template(self):
    return "templates/play.html"

  def update_values(self, player, values):
    return

  def post(self):
    """ Receives the updated round scores from a player after they complete a round. """
    self.redirect(self.request.referer)


class GamesHandler(main_handlers.BaseHandler):
  def get_template(self):
    return "templates/games.html"

  def update_values(self, player, values):
    incomplete_game1 = {"opponent": "Dave",
                        "key": "blank",
                        "last_update": datetime.now(),
                        "official_round": "1",
                        "my_round": "1",
                        "opponent_finished": "Yes"}
    incomplete_game2 = {"opponent": "Frank",
                        "key": "blank",
                        "last_update": datetime.now(),
                        "official_round": "42",
                        "my_round": "50",
                        "opponent_finished": "No"}
    incomplete_game3 = {"opponent": "Bob",
                        "key": "blank",
                        "last_update": datetime.now(),
                        "official_round": "10",
                        "my_round": "50",
                        "opponent_finished": "No"}
    incomplete_games = [incomplete_game1, incomplete_game2, incomplete_game3,
                        incomplete_game1, incomplete_game2, incomplete_game3,
                        incomplete_game1, incomplete_game2, incomplete_game3,
                        incomplete_game1, incomplete_game2, incomplete_game3,
                        incomplete_game1, incomplete_game2, incomplete_game3,
                        incomplete_game1, incomplete_game2, incomplete_game3,
                        incomplete_game1, incomplete_game2, incomplete_game3,
                        incomplete_game1, incomplete_game2, incomplete_game3,
                        incomplete_game1, incomplete_game2, incomplete_game3,
                        incomplete_game1, incomplete_game2, incomplete_game3,
                        incomplete_game1, incomplete_game2, incomplete_game3,
                        incomplete_game1, incomplete_game2, incomplete_game3]
    values["incomplete_games"] = incomplete_games
