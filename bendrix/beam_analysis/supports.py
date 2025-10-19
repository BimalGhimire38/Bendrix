from ..utils.unit_conversion import UnitConversion

class Support:
    def __init__(self, position, type='pinned', position_unit='mm'):
        # Convert position to mm internally
        self.position = UnitConversion.convert(position, position_unit, 'mm')
        self.type = type  # 'pinned' (vertical reaction), 'roller' (vertical), 'fixed' (vertical + moment)
        self.reaction_force = 0.0  # Vertical reaction in N
        self.reaction_moment = 0.0 if type != 'fixed' else 0.0  # Moment in N*mm