from cards import Deck
from poker import Holdem

while True:
    d = Deck()
    # d.shuffle()
    # h = Hand(d.draw_card(), d.draw_card())
    # print h, h.suited
    print 'hands:'
    ps = d.deal_players(4)
    ps_str = ''
    for p in ps:
        ps_str += str(p) + ', '
    print ps_str

    print "community:"
    com = d.deal_community()
    com_str = ''
    for c in com:
        com_str += str(c) + ', '
    print com_str

    ss = list()
    ss.append(Holdem.showdown_hand_score(ps[0], com))
    ss.append(Holdem.showdown_hand_score(ps[1], com))
    ss.append(Holdem.showdown_hand_score(ps[2], com))
    ss.append(Holdem.showdown_hand_score(ps[3], com))
    for i in range(0, 4):
        print ps[i], ss[i]
        if ss[i][0] == '9':
            exit()
    print 'sorted:'
    # ss = sorted(ss)
    # for s in ss:
    #     print s
