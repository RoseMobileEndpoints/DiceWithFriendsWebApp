import base_handlers
import models
from utils import game_utils
from utils import player_utils

import logging

### Pages ###

class PlayPage(base_handlers.BasePage):
  def get_template(self):
    return "templates/play.html"

  def update_values(self, player, values):
    return


class GamesPage(base_handlers.BasePage):
  def get_template(self):
    return "templates/games.html"

  def update_values(self, player, values):
    all_my_games = game_utils.get_all_games_for_player(player)
    incomplete_games = game_utils.get_incomplete_games(all_my_games)
    game_utils.add_incomplete_game_table_data(incomplete_games, player)
    values["incomplete_games"] = incomplete_games


### Actions ###

class ScoresUpdateAction(base_handlers.BaseAction):
  def handle_post(self, player):
    """ Receives the updated round scores from a player after they complete a round. """
    self.redirect(self.request.referer)


class NewGameAction(base_handlers.BaseAction):
  def handle_post(self, player):
    invited_player = player_utils.get_player_from_email(self.request.get('invited_player_email').lower())
    new_game = models.Game(parent=player.key,
                           creator_player_key=player.key,
                           invited_player_key=invited_player.key)
    new_game.put();
    self.redirect("/play?game_key=" + new_game.key.urlsafe())