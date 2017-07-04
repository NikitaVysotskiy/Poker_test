from collections import Counter
from itertools import combinations


RANKS = "A23456789TJQKA"


def get_ranks_list(lst):
    return [card[0] for card in lst]


def get_suits_list(lst):
    return [card[1] for card in lst]


def cmp_cards(card):
    return RANKS[1:].index(card[:-1])   # cmp ranks for sorting


def find_ngrams(input_list, n):
    ngrams = zip(*[input_list[i:] for i in range(n)])   # n-grams(5) in str combs for straight order
    return ["".join(tpl) for tpl in ngrams]  # to str


def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]   # split input onto deals of 10 cards


def check_straight_flush(deal):
    suits = get_suits_list(deal)
    suitable = list()

    for suit in set(suits):
        if suits.count(suit) > 4: # all suits, that have 4 cards in deal
            suitable.append(suit)

    for suit in suitable:
        wanted_cards = sorted([card for card in deal if card[1:] == suit], key=cmp_cards)  # cards, that might be in comb
        ranks_str = "".join(get_ranks_list(wanted_cards))   # their ranks
        for ngram in find_ngrams(ranks_str, 5):
            if ngram in RANKS * 2:      # check for straightness
                ngram_cards = {card for card in wanted_cards if card[0] in ngram}
                deck_wanted = ngram_cards & set(deal[5:])   # intersection for wanted cards in deck
                hand_excess = (ngram_cards ^ set(deal[:5])) - deck_wanted   # count of cards, that might be changed
                if len(deck_wanted) > len(hand_excess):
                    return False
                else:
                    for card in deck_wanted:
                        if deal[5:].index(card) >= len(hand_excess):  # check if cards are reachable
                            return False
                return True
    return False


def check_four(deal):
    counts = {k: v for k, v in Counter(get_ranks_list(deal)).items() if v > 3}
    wanted_cards = set()
    if counts:
        for rank in counts:
            wanted_cards.update({card for card in deal if rank in card})
        deck_wanted = set(deal[5:]) & wanted_cards
        hand_excess = (set(deal[:5]) ^ wanted_cards) - deck_wanted
        for card in deck_wanted:
            if hand_excess and deal[5:].index(card) >= len(hand_excess):
                return False
        return True
    return False


def check_full_house(deal):
    counts_2 = {k: v for k, v in Counter(get_ranks_list(deal)).items() if v > 1}
    counts_3 = {k: v for k, v in counts_2.items() if v > 2}
    if counts_3:
        wanted_cards = set()
        for rank_2 in counts_2:
            wanted_cards.update({card for card in deal if rank_2 in card})
        if len(wanted_cards) >= 5:
            deck_wanted = set(deal[5:]) & wanted_cards
            hand_excess = (set(deal[:5]) ^ wanted_cards) - deck_wanted
            for card in deck_wanted:
                if hand_excess and deal[5:].index(card) >= len(hand_excess):
                    return False
            return True
    return False


def check_flush(deal):
    suits = get_suits_list(deal)
    suitable = list()

    for suit in set(suits):
        if suits.count(suit) > 4:
            suitable.append(suit)

    for suit in suitable:
        wanted_cards = {card for card in deal if card[1] == suit}
        deck_wanted = wanted_cards & set(deal[5:])
        hand_excess = (wanted_cards ^ set(deal[:5])) - deck_wanted

        cnt = len(deck_wanted)
        for card in deck_wanted:
            if hand_excess and deal[5:].index(card) >= len(hand_excess):
                cnt -= 1
        return bool(cnt)

    return False


def check_straight(deal):
    ranks_str = "".join(sorted(set(get_ranks_list(deal)),
                               key=lambda card: RANKS.index(card)))
    cnt = 0
    for ngram in find_ngrams(ranks_str, 5):
        if ngram in RANKS * 2:
            ngram_cards = {card for card in deal if card[0] in ngram}
            deck_wanted = ngram_cards & set(deal[5:])
            hand_excess = (ngram_cards ^ set(deal[:5])) - deck_wanted

            cnt = len(deck_wanted)
            for card in deck_wanted:
                if hand_excess and deal[5:].index(card) >= len(hand_excess):
                    cnt -= 1
    return bool(cnt)


def check_three(deal):
    counts = {k: v for k, v in Counter(get_ranks_list(deal)).items() if v > 2}
    wanted_cards = set()
    if counts:
        for rank in counts:
            wanted_cards.update({card for card in deal if rank in card})
        deck_wanted = set(deal[5:]) & wanted_cards
        hand_excess = (set(deal[:5]) ^ wanted_cards) - deck_wanted
        cnt = len(deck_wanted)
        for card in deck_wanted:
            if hand_excess and deal[5:].index(card) >= len(hand_excess):
                cnt -= 1
        return bool(cnt)
    return False


def check_two_pairs(deal):
    # print(deal)
    counts = {k: v for k, v in Counter(get_ranks_list(deal)).items() if v > 1}
    res = True
    if len(counts) > 1:
        for comb in combinations(counts, 2):
            wanted_cards = set()
            for rank in comb:
                wanted_cards.update({card for card in deal if rank in card})
            deck_wanted = set(deal[5:]) & wanted_cards
            hand_excess = (set(deal[:5]) ^ wanted_cards) - deck_wanted

            for card in deck_wanted:
                if hand_excess and deal[5:].index(card) >= len(hand_excess):
                    res = False
                    break
            else:
                return True
    else:
        res = False
    return res


def check_pair(deal):
    counts = {k: v for k, v in Counter(get_ranks_list(deal)).items() if v > 1}
    if counts and len(counts) == 1:
        rank = next(iter(counts))
        if counts[rank] == 2 and rank in deal[-1]:
            return False
    return True


if __name__ == '__main__':
    input_cards = """  
                     TH JH QC QD QS QH KH AH 2S 6S 
                     2H 2S 3H 3S 3C 2D 3D 6C 9C TH
                     2H 2S 3H 3S 3C 2D 9C 3D 6C TH
                     2H AD 5H AC 7H AH 6H 9H 4H 3C
                     AC 2D 9C 3S KD 5S 4D KS AS 4C
                     KS AH 2H 3C 4H KC 2C TC 2D AS
                     AH 2C 9S AD 3C QH KS JS JD KD
                     6C 9C 8C 2D 7C 2H TC 4C 9S AH
                     3D 5S 2H QD TD 6S KH 9H AD QH
                  """

    input_cards_list = input_cards.split()
    deals = list(chunk(input_cards_list, 10))
    comb_funcs = [check_straight_flush, check_four, check_full_house, check_flush,
                  check_straight, check_three, check_two_pairs, check_pair]
    fmt = "Hand: {hand}, Deck: {deck}\t||\tBest hand: {comb}"
    for dl in deals:
        for func in comb_funcs:
            if func(dl):
                print(fmt.format(hand=dl[:5], deck=dl[:5], comb=func.__name__[6:]))
                break
        else:
            print(fmt.format(hand=dl[:5], deck=dl[:5], comb="highest card"))

