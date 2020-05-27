from .price import Price
from .residence import Residence


class Posting:
    def __init__(self):
        self.picture = None
        self.reference_code = None
        self.address = None
        self.available_as_of = None
        self.cadastral_income = None
        self.price = Price()
        self.residence = Residence()

