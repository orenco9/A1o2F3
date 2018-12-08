from config import POSITIONS_LIST
from strategy import Strategy


class RankAndPoseStrategy(Strategy):
    def __init__(self, percentage_open_allins_by_players_remain, percentage_over_allins_by_players_remain):
        super(RankAndPoseStrategy, self).__init__()
        self.percentage_open_allins_by_players_remain = percentage_open_allins_by_players_remain
        self.percentage_over_allins_by_players_remain = percentage_over_allins_by_players_remain

    def allin_or_fold(self, hand, balances, position, looseness_factors):
# n me prev
# 4 0 0
# 4 1 1
# 4 3 3
#
# 3 1 0
# 3 3 2
#
# 2_2_0
# 2_3_1
        n_players = len(balances)
        n_prev_players = n_players - POSITIONS_LIST.index(position)
        n_next_players = n_players - n_prev_players - 1
        n_prev_opps = 0
        for i in range(0, n_prev_players):
            if balances[i] > 0:
                n_prev_opps += 1
        n_next_opps = self.percentage_over_allins_by_players_remain[0] * n_next_players
        n_opps = round(n_prev_opps + n_next_opps)

        rank = hand.calc_percentile(n_opps)
        if n_prev_opps > 0:
            return rank >= self.percentage_over_allins_by_players_remain[n_next_players]
        else:
            return rank >= self.percentage_open_allins_by_players_remain[n_next_players]
