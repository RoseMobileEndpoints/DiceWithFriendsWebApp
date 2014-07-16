import time

import base_handlers

### Pages ###

class HomePage(base_handlers.BasePage):
  def get_template(self):
    return "templates/home.html"

  def update_values(self, player, base_values):
    return

# Note, this one is specifically NOT a BasePage to allow users to enter without a display_name set.
# Also note the name is "Handler" not Page because it does both get and post.
class SetDisplayNameAction(base_handlers.BaseAction):
  def handle_post(self, player):
    """ Used to set the display name for a player. """
    player.display_name = self.request.get('display_name')
    player.put()
    time.sleep(0.25)
    self.redirect(self.request.referer)
