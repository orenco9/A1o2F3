import random
from config import POSITIONS_LIST
from strategy import Strategy


class RandomStrategy(Strategy):
    def __init__(self, percentage_open_allins, percentage_over_allins):
        super(RandomStrategy, self).__init__()
        self.percentage_open_allins = percentage_open_allins
        self.percentage_over_allins = percentage_over_allins

    def allin_or_fold(self, hand, balances, position, looseness_factors):
        n_players = len(balances)
        n_prev_players = n_players - POSITIONS_LIST.index(position)
        for i in range(n_prev_players):
            if balances[i] > 0:
                return random.random() < self.percentage_over_allins
        return random.random() < self.percentage_open_allins
