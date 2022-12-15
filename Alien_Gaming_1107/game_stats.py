class GameStats:
    def __init__(self, ai_settings):
        self.ship_left = None
        self.game_active = True
        self.ai_settings = ai_settings
        self.reset_stats()

    def reset_stats(self):
        self.ship_left = self.ai_settings.ship_limit - 1
        