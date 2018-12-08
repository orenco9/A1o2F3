import operator
from cards import Deck, Card, Hand
from poker import Holdem

N_PLAYERS = 2
N_LOOP = 30000


def main():
    d = Deck()
    print 'hands:'
    c1 = raw_input('card1?')
    c2 = raw_input('card2?')
    c3 = raw_input('card3?')
    c4 = raw_input('card4?')
    card1 = Card(c1[0], c1[1])
    card2 = Card(c2[0], c2[1])
    card3 = Card(c3[0], c3[1])
    card4 = Card(c4[0], c4[1])
    ps = list()
    ps.append(Hand(card1, card2))
    ps.append(Hand(card3, card4))
    # ps = d.deal_players(N_PLAYERS)
    ps_str = ''
    for p in ps:
        ps_str += str(p) + ', '
    print ps_str

    wins = [0] * N_PLAYERS
    for loop in range(0, N_LOOP):
        d.reset()
        for p in ps:
            d.draw_card(p.card1)
            d.draw_card(p.card2)

        # print "community:"
        com = d.deal_community()
        com_str = ''
        for c in com:
            com_str += str(c) + ', '
        # print com_str

        ss = []
        for i in range(0, N_PLAYERS):
            ss.append(Holdem.showdown_hand_score(ps[i], com))
            # print ps[i], ss[i]
            # # if ss[i][0] == '9':
            # #     exit()
        # print 'best:'
        max_index, max_value = max(enumerate(ss), key=operator.itemgetter(1))
        # print max_index, max_value
        if ss[0] == ss[1]:
            wins[0] += 0.5
            wins[1] += 0.5
        else:
            wins[max_index] += 1  # OCOC what about ties?

    for i_wins in wins:
        print round(float(i_wins) / N_LOOP * 1000) / 10.0

if __name__ == "__main__":
    main()

# python -m cProfile -s cumtime main2.py
