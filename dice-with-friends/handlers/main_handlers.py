from google.appengine.api import users
import logging
import time
import webapp2

import base_handlers
import main
from utils import player_utils

### Pages ###

class HomePage(base_handlers.BasePage):
  def get_template(self):
    return "templates/home.html"

  def update_values(self, player, base_values):
    return

# Note, this one is specifically NOT a BasePage to allow users to enter without a display_name set.
# Also note the name is "Handler" not Page because it does both get and post.
class SetDisplayNameHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      template = main.jinja_env.get_template("templates/home.html")
      self.response.out.write(template.render({'login_url': users.create_login_url("/")}))
    else:
      player = player_utils.get_player_from_email(user.email())
      template = main.jinja_env.get_template("templates/set_display_name.html")
      self.response.out.write(template.render({'player': player, 'logout_url': users.create_logout_url("/")}))

  def post(self):
    """ Used to set the display name for a player. """
    user = users.get_current_user()
    if not user:
      raise Exception("Missing user.")
    player = player_utils.get_player_from_email(user.email())
    player.display_name = self.request.get('display_name')
    player.put()
    time.sleep(0.25)  # Hack.  Didn't want to implement a Parent key to get strong consistency.
    self.redirect("/")
