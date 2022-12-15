from global_var import ai_settings


class GameStats:
    def __init__(self):
        self.ship_left = None
        self.game_active = False
        self.score = 0
        self.ship_left = ai_settings.ship_limit
        self.game_difficulty = 0

    def reset_stats(self):
        self.ship_left = ai_settings.ship_limit
        self.score = 0
        self.game_active = False
        self.game_difficulty = 1
