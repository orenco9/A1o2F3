from strategy import Strategy


class BinaryStrategy(Strategy):
    def __init__(self, always_call):
        super(BinaryStrategy, self).__init__()
        self.always_call = always_call

    def allin_or_fold(self, hand, balances, position, looseness_factors):
        return self.always_call
