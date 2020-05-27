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


class Interior:
    def __init__(self):
        self.kitchen_type = None
        self.bedrooms = None
        self.bedroom_surfaces = None
        self.bathrooms = None
        self.toilets = None
        self.basement = None
        self.toilets = None
        self.attic = None
        self.living_area = None
        self.living_room_surface = None
        self.furnished = None


class Exterior:
    def __init__(self):
        self.surface_of_the_plot = None
        self.connected_to_the_sewer_network = True
        self.terrace = None
        self.has_gas_water_electricity = True


class Energy:
    def __init__(self):
        self.e_level = None
        self.epc = None
        self.heating_type = None
        self.double_glazing = None
        self.heat_pump = None
        self.pv_cells = None


class Townplanning:
    def __init__(self):
        self.flood_zone = None
        self.Latest_land_use_designation = ""
        self.planning_permission_obtained = False


class Residence:
    def __init__(self):
        self.general = General()
        self.interior = Interior()
        self.exterior = Exterior()
        self.energy = Energy()
        self.townplanning = Townplanning()

