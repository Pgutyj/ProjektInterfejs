class Player:
    def __init__(self,n='Anonymous'):
       self.name = n
       self.score = 0
    def get_name(self):
        return self.name

    def __repr__(self):
        return self.name