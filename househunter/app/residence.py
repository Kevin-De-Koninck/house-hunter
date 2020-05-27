from datetime import datetime


class Price:
    def __init__(self):
        self.date_of_change = None
        self.history = []

    @property
    def price(self):
        if not len(self.history):
            return None
        return self.history[0].get('price')

    @property
    def price_has_been_lowered(self):
        if not len(self.history) > 1:
            return False
        return self.history[0].get('price') < self.history[1].get('price')

    @property
    def date_of_last_change(self):
        if not len(self.history):
            return None
        return self.history[0].get('date_of_change')

    def add(self, price):
        self.history.append({"date_of_change": datetime.now().timestamp(),
                             "price": price})
        self.history.sort(key = lambda x:x['date_of_change'], reverse=True)


class Residence:
    def __init__(self):
        self.state = ""
        self.build_year = ""
        self.current_price = Price()
        self.postal_code = ""
        self.is_new_real_estate = True
        self.bedrooms = 0
        self.double_glazing = False
        self.planning_permission_obtained = False
        self.epc = 0
        self.building_state = ""
        self.kitchen_installed = True
        self.garage = False
        self.mobi_score = 0
        self.living_area = 0


class House(Residence):
    def __init__(self):
        super().__init__()
        self.type = "house"
        self.connected_to_the_sewer_network = True
        self.in_flood_zone = False
        self.has_gas_water_electricity = True
        self.Latest_land_use_designation = ""
        self.facades = 4
        self.garden = True
        self.total_area = 0


class appartment(Residence):
    def __init__(self):
        super().__init__()
        self.type = "appartment"


