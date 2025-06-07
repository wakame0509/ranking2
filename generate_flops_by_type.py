from itertools import combinations
from utils import card_to_rank, card_to_suit

def generate_flops_by_type(hand, flop_type):
    """
    指定されたハンドとフロップタイプに基づき、全通りの該当フロップを生成。
    """
    deck = generate_full_deck()
    hand_cards = hand_to_cards(hand)
    used = set(hand_cards)
    candidates = [c for c in deck if c not in used]

    flops = []
    for flop in combinations(candidates, 3):
        if flop_matches_type(flop, hand_cards, flop_type):
            flops.append(list(flop))

    return flops

def generate_full_deck():
    suits = ['h', 'd', 'c', 's']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    return [r + s for r in ranks for s in suits]

def hand_to_cards(hand_str):
    """'AKs' → ['Ah', 'Kh'] などの簡易変換。スートは仮で適当に割り当てる"""
    r1, r2 = hand_str[0], hand_str[1]
    if r1 == r2:
        return [r1 + 'h', r2 + 'd']
    elif hand_str[2] == 's':
        return [r1 + 'h', r2 + 'h']
    else:
        return [r1 + 'h', r2 + 'd']

def flop_matches_type(flop, hand, flop_type):
    """フロップが指定のタイプに一致するか判定"""

    ranks = [card_to_rank(c) for c in flop]
    suits = [card_to_suit(c) for c in flop]
    unique_ranks = set(ranks)
    unique_suits = set(suits)

    hand_ranks = set(card_to_rank(c) for c in hand)

    # フロップタイプ別条件分岐
    if flop_type == "hit+2suit":
        return any(r in hand_ranks for r in ranks) and max_suit_count(suits) >= 2

    elif flop_type == "no_hit_mixed":
        return hand_ranks.isdisjoint(unique_ranks) and len(unique_suits) == 3

    elif flop_type == "2connect":
        sorted_vals = sorted([rank_to_int(r) for r in unique_ranks])
        return has_consecutive_pair(sorted_vals)

    elif flop_type == "paired_board":
        return len(unique_ranks) <= 2

    elif flop_type == "monotone":
        return len(unique_suits) == 1

    elif flop_type == "highcard_dry":
        return all(rank_to_int(r) >= 10 for r in ranks) and len(unique_suits) == 3

    elif flop_type == "lowcard_dry":
        return all(rank_to_int(r) <= 9 for r in ranks) and len(unique_suits) == 3

    return False

def max_suit_count(suits):
    return max(suits.count(s) for s in set(suits))

def rank_to_int(rank):
    table = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
             'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    return table[rank]

def has_consecutive_pair(vals):
    vals = sorted(set(vals))
    for i in range(len(vals) - 1):
        if vals[i+1] - vals[i] == 1:
            return True
    return False
