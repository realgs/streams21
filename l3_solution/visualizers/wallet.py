from json import JSONEncoder


class Wallet:

    def __init__(self, profit=0):
        self.transactions = []
        self.profit = profit

    def add_transaction(self, wallet_item):
        if wallet_item.quantity == 0:
            return
        else:
            self.transactions.append(wallet_item)

    def sell_crypto(self, quantity, price):
        self.profit = price * quantity
        for i in range(len(self.transactions)):
            if len(self.transactions) > i:
                if self.transactions[i].quantity == quantity:
                    self.profit -= self.transactions[i].total_value()
                    self.transactions.pop(i)
                    break
                elif self.transactions[i].quantity > quantity:
                    self.profit -= self.transactions[i].price * quantity
                    self.transactions[i].quantity -= quantity
                    break
                else:
                    self.profit -= self.transactions[i].total_value()
                    quantity -= self.transactions[i].quantity
                    self.transactions.pop(i)

    def avg_buy(self):
        total_values = sum([wi.total_value() for wi in self.transactions])
        total_quantity = sum([wi.quantity for wi in self.transactions])
        if total_quantity == 0 or total_quantity == 0:
            return None
        return total_values / total_quantity

    def total_quantity(self):
        return sum([wi.quantity for wi in self.transactions])

    def to_json_conventer(self):
        return {"profit": self.profit, "transactions": [i.to_json_conventer() for i in self.transactions]}


class WalletItem:
    def __init__(self, quantity, price):
        self.quantity = quantity
        self.price = price

    def total_value(self):
        return self.quantity * self.price

    def to_json_conventer(self):
        return self.__dict__
