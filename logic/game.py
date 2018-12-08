from cards import Deck
from config import POSITIONS_LIST, POS_SB_VS_DEALER, POS_BB_VS_DEALER, POS_UTG_VS_DEALER
from poker import Holdem


CASHOUT_BUYIN_FACTOR_LOWER = 2
CASHOUT_BUYIN_FACTOR_UPPER = 4
START_BALANCE = 10000


class Player:
    def __init__(self, idx, strategy, wallet_balance, buyin):
        self.name = 'Player{}'.format(idx)
        self.strategy = strategy
        self.wallet_balance = wallet_balance
        self.buyin = buyin

        self.table_balance = -1
        self.n_spots = -1
        self.n_walks = -1
        self.n_folds = -1
        self.n_open_allins = -1
        self.n_over_allins = -1
        self.n_profits = -1
        self.n_losses = -1
        self.reset()

    def reset(self):
        self.table_balance = 0
        self.n_spots = 0
        self.n_walks = 0
        self.n_folds = 0
        self.n_open_allins = 0
        self.n_over_allins = 0
        self.n_profits = 0
        self.n_losses = 0

        self.attempt_add_chips()

    def __str__(self):
        return '{}: {}$ (plus {}$)'.format(self.name, self.table_balance, self.wallet_balance)

    def act(self, hand, balances, position, looseness_factors):
        return self.strategy.allin_or_fold(hand, balances, position, looseness_factors)

    def bet(self, bet_size):
        actual_bet_size = min(bet_size, self.table_balance)
        self.table_balance -= actual_bet_size
        return actual_bet_size

    def go_allin(self):
        return self.bet(self.table_balance)

    def cashout(self, amount):
        if amount > self.table_balance:
            raise Exception('Not enough balance to cashout')
        self.table_balance -= amount
        self.wallet_balance += amount

    def eval_walk(self, pot_won):
        self.n_walks += 1
        self.table_balance += pot_won

    def eval_spot_result(self, bet_size, pot_won):
        if pot_won >= bet_size:
            self.n_profits += 1
        else:
            self.n_losses += 1

        self.table_balance += pot_won
        # Cashout
        self.attempt_max_cashout()
        # Add chips
        self.attempt_add_chips()

    def attempt_add_chips(self):
        addon = self.buyin - self.table_balance
        if addon > 0:
            self.wallet_balance -= addon
            self.table_balance = self.buyin

    def attempt_partial_cashout(self, cashout_buyin_factor):
        if self.table_balance <= self.buyin:
            return
        profit = self.table_balance - self.buyin
        cashout = profit  # OCOC min(profit, self.buyin * cashout_buyin_factor_lower)
        self.table_balance -= cashout
        self.wallet_balance += cashout

    def attempt_max_cashout(self):
        if self.table_balance > self.buyin * CASHOUT_BUYIN_FACTOR_UPPER:  # OCOC - CASHOUT_BUYIN_FACTOR_LOWER, CASHOUT_BUYIN_FACTOR_UPPER
            self.attempt_partial_cashout(CASHOUT_BUYIN_FACTOR_LOWER)


class Session:
    def __init__(self, n_bbs, bb_size, rake_size, strategies):
        self.n_bbs = n_bbs
        self.bb_size = bb_size
        self.rake_size = rake_size

        self.n_spots = 0
        self.rake_accum = 0

        self.players = []
        for strategy in strategies:
            self.players.append(Player(len(self.players) + 1, strategy, START_BALANCE, n_bbs * bb_size))
        self.n_players = len(self.players)
        self.dealer_idx = self.n_players - 1  # Start with the first player as SB
        self.deck = Deck()

    def run(self, n_spots):
        self.report()
        for i in range(n_spots):
            self.handle_spot()
            self.dealer_idx = (self.dealer_idx + 1) % self.n_players
            self.report()
        self.report()

    def handle_spot(self):
        self.n_spots += 1
        self.deck.reset()
        hands = self.deck.deal_players(self.n_players)

        for h in hands:
            print h

        balances = [0] * self.n_players
        for i_player in range(self.n_players):
            player_idx = (self.dealer_idx + POS_UTG_VS_DEALER + i_player) % self.n_players
            balances[i_player] = self.players[player_idx].table_balance

        bet_sizes = [0] * self.n_players
        pot_size = 0
        player_sb_idx = (self.dealer_idx + POS_SB_VS_DEALER) % self.n_players
        bet_sizes[player_sb_idx] = self.players[player_sb_idx].bet(self.bb_size / 2)  # SB
        pot_size += bet_sizes[player_sb_idx]
        player_bb_idx = (self.dealer_idx + POS_BB_VS_DEALER) % self.n_players
        bet_sizes[player_bb_idx] = self.players[player_bb_idx].bet(self.bb_size)  # BB
        pot_size += bet_sizes[player_bb_idx]

        allin_participants = []
        for i_player in range(self.n_players):
            if i_player == self.n_players - 1 and len(allin_participants) == 0:
                break  # When no one bet and last player to act

            player_idx = (self.dealer_idx + POS_UTG_VS_DEALER + i_player) % self.n_players
            is_allin = self.players[player_idx].act(hands[player_idx], balances, POSITIONS_LIST[i_player], None)
            if is_allin:
                bet_sizes[player_idx] += self.players[player_idx].go_allin()
                pot_size += bet_sizes[player_idx]
                allin_participants.append({
                    'player_idx': player_idx,
                    'hand': hands[player_idx],
                    'bet': bet_sizes[player_idx]})
            else:
                balances[i_player] = 0

        if len(allin_participants) == 0:
            player_idx = (self.dealer_idx + POS_BB_VS_DEALER) % self.n_players
            self.players[player_idx].eval_walk(pot_size)
        elif len(allin_participants) == 1:
            player_idx = allin_participants[0]['player_idx']
            self.players[player_idx].eval_spot_result(allin_participants[0]['bet'], pot_size)
        else:
            com = self.deck.deal_community()
            for c in com:
                print c
            hand_ranks = []
            for i in range(0, len(allin_participants)):
                hand_ranks.append(Holdem.showdown_hand_score(allin_participants[i]['hand'], com))

            # OCOC evaluate hand ranks and side pots...
            participant_bets = [item['bet'] for item in allin_participants]
            participant_wins = Holdem.distribute_pot(hand_ranks, participant_bets)
            for i in range(0, len(allin_participants)):
                player_idx = allin_participants[i]['player_idx']
                self.players[player_idx].eval_spot_result(allin_participants[i]['bet'], participant_wins[i])

    def report(self):
        for pl in self.players:
            print pl
        print sum([p.wallet_balance + p.table_balance for p in self.players])
