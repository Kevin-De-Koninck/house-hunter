from .price import Price


class General:
    def __init__(self):
        self.residence_type = None
        self.building_condition = None
        self.construction_year = None
        self.available_as_of = None
        self.covered_parking_spaces = None
        self.outdoor_parking_spaces = None
        self.facades = None
        self.facade_width_street = None
        self.floor = None
        self.number_of_floors = None

    def __repr__(self):
        return repr(self.__dict__)


class Interior:
    def __init__(self):
        self.kitchen_type = None
        self.bedrooms = None
        self.bathrooms = None
        self.toilets = None
        self.basement = None
        self.attic = None
        self.furnished = None

    def __repr__(self):
        return repr(self.__dict__)


class Exterior:
    def __init__(self):
        self.surface_of_the_plot = None
        self.connected_to_the_sewer_network = None
        self.terrace = None
        self.has_gas_water_electricity = None

    def __repr__(self):
        return repr(self.__dict__)


class Energy:
    def __init__(self):
        self.energy_class = None
        self.epc = None
        self.heating_type = None
        self.double_glazing = None
        self.heat_pump = None
        self.pv_cells = None

    def __repr__(self):
        return repr(self.__dict__)


class Townplanning:
    def __init__(self):
        self.flood_zone = None
        self.Latest_land_use_designation = None
        self.planning_permission_obtained = None

    def __repr__(self):
        return repr(self.__dict__)


class Meta:
    def __init__(self):
        self.immo_site = None
        self.price = Price()
        self.reference_code = None
        self.address = None
        self.postal_code = None
        self.city = None

    def __repr__(self):
        return repr(self.__dict__)


class Residence:
    def __init__(self, general=General(), interior=Interior(), exterior=Exterior(),
                 energy=Energy(), townplanning=Townplanning(), meta=Meta()):
        self.general = general
        self.interior = interior
        self.exterior = exterior
        self.energy = energy
        self.townplanning = townplanning
        self.meta = meta

    def __repr__(self):
        return repr(self.__dict__)

