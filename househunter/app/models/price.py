from datetime import datetime


class Price:
    def __init__(self):
        self.history = []

    @property
    def price(self):
        if len(self.history) == 0:
            return None
        return self.history[0].get('price')

    @property
    def lowest_recorded_price(self):
        if len(self.history) <= 1:
            return True
        return min([p.get('price') for p in self.history])

    @property
    def date_of_last_change(self):
        if len(self.history) == 0:
            return None
        return self.history[0].get('date_of_change')

    def add(self, price):
        self.history.append({"date_of_change": datetime.now().timestamp(),
                             "price": price})
        self.history.sort(key=lambda x: x['date_of_change'], reverse=True)

