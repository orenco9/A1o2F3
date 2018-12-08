import random
from config import SUITS_LIST, RANKS
from poker import Holdem


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return "Card(%s, %s)" % (self.rank, self.suit)

    def __eq__(self, other):
        if isinstance(other, Card):
            return (self.rank == other.rank) and (self.suit == other.suit)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())
    
    def __str__(self):
        return '{}{}'.format(self.rank, self.suit)

    def value(self):
        return RANKS.index(self.rank) + 2

    def hex_value(self):
        return hex(self.value())[2]

    @staticmethod
    def get_all_cards():
        cards = set()
        for rank in RANKS:
            for suit in SUITS_LIST:
                cards.add(Card(rank, suit))
        return cards
ALL_CARDS = Card.get_all_cards()


class Hand:
    def __init__(self, card1, card2):
        self.card1 = card1
        self.card2 = card2
        self.suited = card1.suit == card2.suit

    def __str__(self):
        flip = self.card2.value() > self.card1.value()
        if flip:
            return '{}{}'.format(self.card2, self.card1)
        else:
            return '{}{}'.format(self.card1, self.card2)

    def compact_repr(self):
        full_repr = str(self)
        notation = '' if full_repr[0] == full_repr[2] else 's' if self.suited else 'o'
        return '{}{}{}'.format(full_repr[0], full_repr[2], notation)

    def calc_percentile(self, n_opponents):
        return Holdem.hand_percentile(self, n_opponents)


class Deck:
    def __init__(self):
        self.cards = None
        self.i_card = -1
        self.reset()

    def reset(self):
        self.cards = set(ALL_CARDS)
        self.i_card = 0

    # def shuffle(self):
    #     random.shuffle(self.cards)
    #     self.i_card = 0

    def draw_card(self, card=None):
        if card is None:
            card = random.sample(self.cards, 1)[0]
        self.cards.remove(card)
        self.i_card += 1
        return card

    def deal_players(self, n_players):
        hands = []
        for i in range(0, n_players):
            hands.append(Hand(self.draw_card(), self.draw_card()))
        return hands

    def deal_community(self):
        return [self.draw_card(), self.draw_card(), self.draw_card(), self.draw_card(), self.draw_card()]
