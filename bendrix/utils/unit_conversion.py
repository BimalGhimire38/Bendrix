# Handle unit conversions
class UnitConversion:
    def __init__(self):
        self.conversion_factors = {
            'm_to_ft': 3.28084,
            'ft_to_m': 0.3048,
            'kg_to_lb': 2.20462,
            'lb_to_kg': 0.453592,
            'cm_to_in': 0.393701,
            'm_to_mm': 1000,
            'mm_to_m': 0.001,
            'kN_to_N': 1000,
            'N_to_kN': 0.001,
            'Pa_to_kPa': 0.001,
            'kPa_to_Pa': 1000,
            'MPa_to_Pa': 1000000,
            'Pa_to_MPa': 0.000001,
            'm2_to_ft2': 10.7639,
            'ft2_to_m2': 0.092903,
            'm3_to_ft3': 35.3147,
            'ft3_to_m3': 0.0283168,
            'mm3_to_in3': 0.0000610237,
            'in3_to_mm3': 16387.1,
            'mm4_to_in4': 3.861e-8,
            'in4_to_mm4': 25910600000,
            'mm4_to_ft4': 3.861e-12,
            'ft4_to_mm4': 2591060000000,
            'mm4_to_m4': 1e-12,
            'm4_to_mm4': 1e12,
        }

    def convert(self, value, from_unit, to_unit):
        key = f"{from_unit}_to_{to_unit}"
        if key in self.conversion_factors:
            return value * self.conversion_factors[key]
        else:
            raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported.")