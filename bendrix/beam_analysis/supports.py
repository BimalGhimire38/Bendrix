# Define support classes
class Support:
    def __init__(self, position, type='pinned'):
        self.position = position
        self.type = type  # 'pinned', 'roller', 'fixed'
        self.reaction_force = 0
        self.reaction_moment = 0 if type != 'fixed' else 0