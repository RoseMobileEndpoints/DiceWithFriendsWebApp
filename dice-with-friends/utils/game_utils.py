from google.appengine.ext import ndb
import logging

from models import Game

GAME_SCORE_TO_WIN = 10000

# Returns a query object for all games the player is in.
def get_all_games_for_player(player):
  return Game.query(ndb.OR(Game.creator_player_key == player.key,
                           Game.invited_player_key == player.key)).fetch()

def get_incomplete_games(games):
  incomplete_games = []
  for game in games:
    if not is_game_finished(game):
      incomplete_games.append(game)
  return incomplete_games

def is_game_finished(game):
  creator_score = sum(game.creator_scores)
  invited_player_score = sum(game.invited_player_scores)
  return creator_score >= GAME_SCORE_TO_WIN or invited_player_score >= GAME_SCORE_TO_WIN

# Input is a Game model object.
# Output needs addition fields:
#   opponent_name
#   last_update_by_opponent
#   official_round
#   current_player_round
#   is_opponent_finished
def add_incomplete_game_table_data(incomplete_games, current_player):
  for game in incomplete_games:
    created_by_current_player = game.creator_player_key == current_player.key
    if created_by_current_player:
      game.opponent_name = game.invited_player_key.get().get_name()
      game.last_update_by_opponent = game.last_update_by_invited_player
      game.current_player_round = len(game.creator_scores)
      opponent_rounds_complete = len(game.invited_player_scores)
      opponent_actual_score = sum(game.invited_player_scores)
    else:
      game.opponent_name = game.creator_player_key.get().get_name()
      game.last_update_by_opponent = game.last_update_by_creator
      game.current_player_round = len(game.invited_player_scores)
      opponent_rounds_complete = len(game.creator_scores)
      opponent_actual_score = sum(game.creator_scores)
    game.official_round = min(game.current_player_round, opponent_rounds_complete)
    if game.last_update_by_opponent is None:
      game.last_update_by_opponent = game.create_time
    game.is_opponent_finished = opponent_actual_score >= GAME_SCORE_TO_WIN


def game_complete_boolean_format(value):
  return "Yes" if value else "No"
