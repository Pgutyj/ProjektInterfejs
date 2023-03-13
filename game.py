from player import Player

class Game():
    def __init__(self, names):
        self.players=list()
        self.active_player=0
        self.start = False
        self.end = False
        self.stage = 0
        self.current = (6,5)
        for name in names:
            self.players.append(Player(name))

    def add_player(self, name):
        if self.start == False:
            self.players.append(Player(name))
        else:
            return -1

    def start_game(self):
        self.start = True