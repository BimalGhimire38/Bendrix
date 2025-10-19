# Entry point to run the beam analysis
from beam_analysis import CalculateReactions
from loads.loads import Loads
from utils.unit_conversion import UnitConversion

def main():
    # Example usage
    calc = CalculateReactions('simply_supported')
    loads = Loads()
    converter = UnitConversion()

    # Add a point load
    magnitude, position = loads.point_load(1000, 0, 2)
    converted_length = converter.convert(position, 'm', 'ft')
    print(f"Point load: {magnitude}N at {converted_length}ft")

if __name__ == "__main__":
    main()