from google.appengine.ext import ndb
from datetime import datetime

from utils import game_utils, player_utils
import base_handlers
import logging
import models


### Pages ###

class PlayPage(base_handlers.BasePage):
  def get_template(self):
    return "templates/play.html"

  def update_values(self, player, values):
    game_key = ndb.Key(urlsafe=self.request.get('game_key'))
    values["game"] = game_key.get()
    return


class GamesInProgressPage(base_handlers.BasePage):
  def get_template(self):
    return "templates/gamesinprogress.html"

  def update_values(self, player, values):
    all_my_games = game_utils.get_all_games_for_player(player)
    incomplete_games = game_utils.get_incomplete_games_for_player(all_my_games, player)
    game_utils.add_incomplete_game_table_data(incomplete_games, player)
    values["incomplete_games"] = incomplete_games


class AllGamesWithFriendsPage(base_handlers.BasePage):
  def get_template(self):
    return "templates/all_games_with_friends.html"

### Actions ###

class ScoresUpdateAction(base_handlers.BaseAction):
  def handle_post(self, player):
    """ Receives the updated round scores from a player after they complete a round. """
    game = ndb.Key(urlsafe=self.request.get('game_key')).get()
    new_score = int(self.request.get("new_score"))
    if player.key == game.creator_key:
      game.creator_scores.append(new_score)
      game.last_update_by_creator = datetime.now()
    else:
      game.invitee_scores.append(new_score)
      game.last_update_by_invitee = datetime.now()
    game.put()
    self.redirect(self.request.referer)


class NewGameAction(base_handlers.BaseAction):
  def handle_post(self, player):
    invited_player = player_utils.get_player_from_email(self.request.get('invited_player_email').lower())
    new_game = models.Game(parent=player.key,
                           creator_key=player.key,
                           invitee_key=invited_player.key)
    new_game.put();
    self.redirect("/play?game_key=" + new_game.key.urlsafe())