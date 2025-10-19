from ..utils.unit_conversion import UnitConversion

class Support:
    def __init__(self, position, type='pinned', position_unit='mm'):
        self.position = UnitConversion.convert(position, position_unit, 'mm')
        self.type = type
        self.reaction_force = 0.0  # N, positive up
        self.reaction_moment = 0.0 if type != 'fixed' else 0.0  # N*mm