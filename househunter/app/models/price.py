from datetime import datetime
from copy import deepcopy

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
        if len(self.history) == 0:
            return 'O'
        return min([p.get('price') for p in self.history])

    @property
    def date_of_last_change(self):
        if len(self.history) == 0:
            return ''
        return self.history[0].get('date_of_change')

    def add(self, price):
        self.history.append({"date_of_change": datetime.now().timestamp(),
                             "price": int(price)})
        self.history.sort(key=lambda x: x['date_of_change'], reverse=True)

    def __repr__(self):
        d = deepcopy(self.__dict__)
        human_history = []
        for item in self.history:
            new_item = {}
            new_item['date_of_change'] = str(datetime.fromtimestamp(item['date_of_change']).strftime('%Y-%m-%d %H:%M:%S'))
            new_item['price'] = '{:,.2f}'.format(int(item['price']))
            human_history.append(new_item)
        d['history'] = human_history
        d['lowest_recorded_price'] = '{:,.2f}'.format(int(self.lowest_recorded_price))
        d['date_of_last_change'] = str(datetime.fromtimestamp(self.date_of_last_change).strftime('%Y-%m-%d %H:%M:%S'))

        return repr(d)
