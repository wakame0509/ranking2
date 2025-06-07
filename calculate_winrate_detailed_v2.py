import random
import pandas as pd
from generate_flops_by_type import generate_flops_by_type
from calculate_winrate import calculate_winrate
from extract_features import extract_features_for_next_card

def run_winrate_evolution_by_floptype(hand, flop_type, stage, preflop_winrate, num_simulations=100000):
    shift_records = {}

    flop_list = generate_flops_by_type(hand, flop_type)

    for flop in flop_list:
        used_cards = set(hand_to_cards(hand) + flop)
        board = flop.copy()

        if stage == "river":
            turn_card = random_card(exclude=used_cards)
            board.append(turn_card)
            used_cards.add(turn_card)

        all_cards = generate_all_cards()
        next_card_candidates = [c for c in all_cards if c not in used_cards]

        for next_card in next_card_candidates:
            full_board = board + [next_card]
            winrate = calculate_winrate(hand, full_board, num_simulations)

            if next_card not in shift_records:
                shift_records[next_card] = []

            shift = winrate - preflop_winrate
            shift_records[next_card].append(shift)

    rows = []
    for card, shifts in shift_records.items():
        avg_shift = sum(shifts) / len(shifts)
        feature = extract_features_for_next_card(hand_to_cards(hand), card, board)
        rows.append({"card": card, "shift": avg_shift, "feature": feature})

    df = pd.DataFrame(rows)
    df.sort_values("shift", ascending=False, inplace=True)
    return df

# 補助関数
def hand_to_cards(hand_str):
    r1, r2 = hand_str[0], hand_str[1]
    if r1 == r2:
        return [r1 + 'h', r2 + 'd']
    elif hand_str[2] == 's':
        return [r1 + 'h', r2 + 'h']
    else:
        return [r1 + 'h', r2 + 'd']

def generate_all_cards():
    suits = ['h', 'd', 'c', 's']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    return [r + s for r in ranks for s in suits]

def random_card(exclude):
    deck = generate_all_cards()
    candidates = [c for c in deck if c not in exclude]
    return random.choice(candidates)
