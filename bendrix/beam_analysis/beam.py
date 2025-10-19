# Define beam types and their reaction calculation methods
class CalculateReactions:
    def __init__(self, beam_type):
        self.beam_type = beam_type

        if beam_type == 'simply_supported':
            self.calc_simply_supported()
        elif beam_type == 'cantilever':
            self.calc_cantilever()
        elif beam_type == 'fixed':
            self.calc_fixed()
        elif beam_type == 'continuous':
            self.calc_continuous()
        elif beam_type == 'propped_cantilever':
            self.calc_propped_cantilever()
        elif beam_type == 'overhanging':
            self.calc_overhanging()

    def calc_simply_supported(self, length):
        self.beam = SimplySupported(length)

    def calc_cantilever(self):
        self.beam = Cantilever()

    def calc_fixed(self):
        self.beam = Fixed()

    def calc_continuous(self):
        self.beam = Continuous()

    def calc_propped_cantilever(self):
        self.beam = ProppedCantilever()

    def calc_overhanging(self):
        self.beam = Overhanging()

# Beam type classes
class SimplySupported:
    def __init__(self, length):
        self.length = length

class Cantilever:
    pass

class Fixed:
    pass

class Continuous:
    pass

class Overhanging:
    pass

class ProppedCantilever:
    pass