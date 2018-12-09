import copy
import re


# Source: http://www.holdemhelpem.com/statistics/pocketrank.html
STARTING_HAND_RANKING_BY_OPPS = {
    1: ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', 'AKs', 'AQs', '77', 'AJs', 'AKo', 'ATs', 'AQo', 'AJo', 'KQs', 'A9s', 'ATo', '66', 'KJs', 'A8s', 'KTs', 'A7s', 'KQo', 'A9o', 'A5s', 'KJo', 'A6s', 'QJs', 'K9s', 'A8o', '55', 'KTo', 'A4s', 'QTs', 'A7o', 'A3s', 'K8s', 'A5o', 'A6o', 'QJo', 'A2s', 'K7s', 'K9o', 'Q9s', 'JTs', 'A4o', 'QTo', 'K6s', 'A3o', '44', 'K5s', 'Q8s', 'K8o', 'J9s', 'K7o', 'A2o', 'Q9o', 'K4s', 'JTo', 'K6o', 'Q7s', 'K3s', 'J8s', 'T9s', 'Q6s', 'K5o', 'Q8o', 'K2s', 'J9o', 'Q5s', '33', 'K4o', 'T8s', 'J7s', 'Q4s', 'Q7o', 'K3o', 'J8o', 'T9o', 'Q3s', 'Q6o', '98s', 'J6s', 'T7s', 'K2o', 'Q5o', 'Q2s', 'J5s', 'J7o', 'T8o', 'Q4o', 'J4s', '22', '97s', 'T6s', 'Q3o', 'J3s', '87s', '98o', 'T7o', 'J6o', '96s', 'J2s', 'Q2o', 'T5s', 'J5o', 'T4s', '86s', 'J4o', '97o', 'T6o', '95s', 'T3s', '76s', 'J3o', '87o', 'T2s', '85s', '96o', 'J2o', 'T5o', '75s', '94s', 'T4o', '65s', '86o', '93s', '84s', '95o', 'T3o', '76o', '92s', '74s', '54s', '64s', 'T2o', '85o', '83s', '75o', '94o', '65o', '82s', '73s', '53s', '93o', '63s', '84o', '92o', '43s', '74o', '54o', '64o', '72s', '52s', '62s', '83o', '42s', '82o', '73o', '53o', '63o', '32s', '43o', '72o', '52o', '62o', '42o', '32o'],
    2: ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', 'AKs', 'AQs', '88', 'AJs', 'AKo', 'ATs', 'KQs', 'AQo', 'KJs', '77', 'AJo', 'KTs', 'A9s', 'ATo', 'KQo', 'QJs', 'A8s', 'QTs', 'KJo', 'A7s', 'K9s', '66', 'A5s', 'JTs', 'KTo', 'A9o', 'A6s', 'QJo', 'A4s', 'A8o', 'Q9s', 'K8s', 'A3s', 'QTo', 'A7o', 'K7s', 'J9s', 'A2s', 'K9o', '55', 'JTo', 'A5o', 'T9s', 'K6s', 'Q8s', 'A6o', 'K5s', 'A4o', 'Q9o', 'J8s', 'K8o', 'K4s', 'A3o', 'T8s', 'Q7s', 'J9o', 'K7o', 'K3s', '98s', 'Q6s', 'A2o', '44', 'T9o', 'J7s', 'Q8o', 'K6o', 'K2s', 'Q5s', 'T7s', 'K5o', 'Q4s', '97s', 'J8o', '87s', 'J6s', 'T8o', 'Q3s', 'K4o', 'Q7o', 'J5s', 'T6s', '98o', 'Q2s', '33', 'Q6o', 'K3o', '96s', 'J4s', '86s', 'J7o', '76s', 'Q5o', 'K2o', 'T7o', 'J3s', 'T5s', '97o', 'Q4o', 'J2s', '87o', '95s', '65s', 'T4s', '75s', '85s', 'J6o', 'Q3o', 'T3s', '22', 'J5o', 'T6o', '54s', 'Q2o', 'T2s', '96o', '64s', '86o', '76o', '94s', 'J4o', '74s', '84s', '93s', 'J3o', 'T5o', '53s', '92s', '65o', '95o', 'J2o', '63s', '75o', 'T4o', '85o', '73s', '83s', '43s', '82s', 'T3o', '54o', '52s', '64o', 'T2o', '62s', '94o', '74o', '42s', '72s', '84o', '93o', '32s', '53o', '92o', '63o', '43o', '73o', '83o', '82o', '52o', '62o', '42o', '72o', '32o'],
    3: ['AA', 'KK', 'QQ', 'JJ', 'TT', 'AKs', '99', 'AQs', 'AJs', 'AKo', 'KQs', 'ATs', 'KJs', '88', 'AQo', 'KTs', 'QJs', 'AJo', 'KQo', 'A9s', 'QTs', 'ATo', 'JTs', 'A8s', 'KJo', '77', 'K9s', 'A7s', 'QJo', 'KTo', 'A5s', 'Q9s', 'A6s', 'A4s', 'A9o', 'J9s', 'QTo', 'T9s', 'K8s', 'A3s', 'JTo', '66', 'A8o', 'K7s', 'A2s', 'Q8s', 'K9o', 'K6s', 'A7o', 'J8s', 'T8s', 'K5s', 'A5o', '98s', 'Q9o', 'A6o', 'K4s', 'J9o', '55', 'Q7s', 'A4o', 'T9o', 'K8o', 'Q6s', 'J7s', 'K3s', 'T7s', 'A3o', '97s', '87s', 'Q5s', 'K7o', 'K2s', 'Q8o', 'A2o', 'Q4s', 'J8o', 'K6o', 'T8o', 'J6s', '44', 'T6s', 'Q3s', '76s', '98o', '86s', 'J5s', '96s', 'K5o', 'Q2s', 'J4s', 'Q7o', 'K4o', '65s', 'J7o', 'Q6o', 'J3s', '75s', 'T5s', 'T7o', '85s', 'K3o', '87o', '95s', '97o', '33', 'T4s', 'J2s', 'Q5o', '54s', 'K2o', 'T3s', '64s', 'Q4o', '74s', 'J6o', 'T2s', '84s', '76o', '94s', 'T6o', '86o', '96o', '53s', 'Q3o', 'J5o', '93s', '22', '63s', 'Q2o', 'J4o', '43s', '92s', '65o', '73s', '83s', '75o', 'T5o', '85o', 'J3o', '52s', '82s', '95o', 'T4o', '54o', 'J2o', '42s', '62s', '72s', '64o', 'T3o', '74o', '32s', '84o', 'T2o', '94o', '53o', '93o', '63o', '43o', '92o', '73o', '83o', '52o', '82o', '42o', '62o', '72o', '32o'],
}
N_STARTING_HAND_RANKING = len(STARTING_HAND_RANKING_BY_OPPS[1])


class Holdem:
    def __init__(self):
        pass

    @staticmethod
    def showdown_hand_score(hand, community):
        all_cards = copy.copy(community)
        all_cards.append(hand.card1)
        all_cards.append(hand.card2)
        
        all_cards_sorted = sorted(all_cards, key=lambda card: card.value())  # sort by value

        hand_values_hex = ''
        hand_suits = ''
        for c in all_cards_sorted:
            hand_values_hex += c.hex_value()
            hand_suits += c.suit

        # 9 - Straight flush
        res_flush = re.match(r'.*(.)(.*\1){4,6}.*', hand_suits)
        if res_flush:
            match_suit = res_flush.group(1)
            indices = [i for i, x in enumerate(hand_suits) if x == match_suit]
            all_suited_cards = [hand_values_hex[i] for i in indices]
            all_suited_cards = ''.join(all_suited_cards)
            res = re.match(r'.*(23456|34567|45678|56789|6789a|789ab|89abc|9abcd|abcde).*', all_suited_cards)
            if res:
                match_cards = res.group(1)
                score = match_cards + '9'
                return score[::-1]
        # 8 - Four of a kind
        res = re.match(r'.*(.)\1\1\1.*', hand_values_hex)
        if res:
            match_card = res.group(1)
            hand_values_hex_new = hand_values_hex.replace(match_card, '')
            score = hand_values_hex_new[-1:] + match_card + match_card + match_card + match_card + '8'
            return score[::-1]
        # 7 - Full house
        res = re.match(r'.*(.)\1\1.*', hand_values_hex)
        if res:
            match_card1 = res.group(1)
            hand_values_hex_new = hand_values_hex.replace(match_card1, '')
            res = re.match(r'.*(.)\1.*', hand_values_hex_new)
            if res:
                match_card2 = res.group(1)
                score = match_card2 + match_card2 + match_card1 + match_card1 + match_card1 + '7'
                return score[::-1]
        # 6 - Flush
        if res_flush:  # (already calc-ed)
            match_suit = res_flush.group(1)
            indices = [i for i, x in enumerate(hand_suits) if x == match_suit]
            best_suited_cards = [hand_values_hex[i] for i in indices[-5:]]
            score = ''.join(best_suited_cards) + '6'
            return score[::-1]
        # 5 - Straight
        unique_hand_values_hex = ''.join(sorted(set(hand_values_hex), key=hand_values_hex.index))
        res = re.match(r'.*(23456|34567|45678|56789|6789a|789ab|89abc|9abcd|abcde).*', unique_hand_values_hex)
        if res:
            match_cards = res.group(1)
            score = match_cards + '5'
            return score[::-1]
        # 4 - Three of a kind
        res = re.match(r'.*(.)\1\1.*', hand_values_hex)
        if res:
            match_card = res.group(1)
            hand_values_hex_new = hand_values_hex.replace(match_card, '')
            score = hand_values_hex_new[-2:] + match_card + match_card + match_card + '4'
            return score[::-1]
        # 3 - Two pair
        res = re.match(r'.*(.)\1.*(.)\2.*', hand_values_hex)
        if res:
            match_card1 = res.group(1)
            match_card2 = res.group(2)
            hand_values_hex_new = hand_values_hex.replace(match_card1, '')
            hand_values_hex_new = hand_values_hex_new.replace(match_card2, '')
            score = hand_values_hex_new[-1:] + match_card1 + match_card1 + match_card2 + match_card2 + '3'
            return score[::-1]
        # 2 - One pair
        res = re.match(r'.*(.)\1.*', hand_values_hex)
        if res:
            match_card = res.group(1)
            hand_values_hex_new = hand_values_hex.replace(match_card, '')
            score = hand_values_hex_new[-3:] + match_card + match_card + '2'
            return score[::-1]
        # 1 - High card
        score = hand_values_hex[-5:] + '1'
        return score[::-1]

    @staticmethod
    def hand_percentile(hand, n_opponents):
        hand_rank = STARTING_HAND_RANKING_BY_OPPS[n_opponents].index(hand.compact_repr())
        return round(float(hand_rank + 1) / N_STARTING_HAND_RANKING * 1000) / 10.0


    @staticmethod
    def distribute_pot(hand_ranks, participant_bets):
        '''
        keep 1 x MAIN + N x SIDE (sorted) pots. Per pot keep a list of players that are part of it.
        If hand ranks is: [cc, bb, aa, aa, zz, aa], then hand rank orders is: [2, 1, 0, 0, 3, 0].
        Divide each pot (from main to last) between the X players with the same highest rank order.
        So if POT #2 contains players [0, 2, 3] -> the pot will be split between players 2 & 3 (both with order = 0)
        '''

        sorted_hand_ranks_idxs = sorted(range(len(hand_ranks)), key=lambda k: hand_ranks[k], reverse=True)
        sorted_bets_idxs = sorted(range(len(participant_bets)), key=lambda k: participant_bets[k])

        participant_wins = [0] * len(participant_bets)
        unclaimed_pot = 0
        partial_bet_distributed = 0

        # Enumerate over players from short to biggest stack
        for i, bet_idx in enumerate(sorted_bets_idxs):
            # Find the relative place of the hand rank for the i-th smallest player
            ith_smallest_player_relative_hand_rank = sorted_hand_ranks_idxs.index(bet_idx)
            if ith_smallest_player_relative_hand_rank <= i:
                # i-th player won partial pot
                side_pot = (participant_bets[bet_idx] - partial_bet_distributed) * (len(participant_bets) - i) + unclaimed_pot
                participant_wins[bet_idx] = side_pot
                partial_bet_distributed = participant_bets[bet_idx]
                unclaimed_pot = 0
            else:
                unclaimed_pot += participant_bets[bet_idx]

        return participant_wins
