import random
import pandas as pd
from generate_flops_by_type import generate_flops_by_type
from calculate_winrate import calculate_winrate  # Monte Carlo 勝率計算
from extract_features import extract_features_for_next_card

def run_winrate_evolution_by_floptype(hand, flop_type, stage, preflop_winrate, num_trials=30):
    """
    - hand: 例 '99'
    - flop_type: 'hit+2suit' など
    - stage: 'turn' または 'river'
    - preflop_winrate: float（プリフロップ勝率）
    - num_trials: 使用するランダムフロップ数
    """

    shift_records = {}

    for trial in range(num_trials):
        flop = random.choice(generate_flops_by_type(hand, flop_type))  # フロップを1つ選ぶ

        # 使われたカード（ハンド＋フロップ）を除外
        used_cards = set(hand_to_cards(hand) + flop)

        # ターン・リバー前のボード（ターンならフロップ、リバーならフロップ＋ターンダミー）
        board = flop.copy()
        if stage == "river":
            # ランダムターンカード1枚追加（usedと重複しないように）
            turn_card = random_card(exclude=used_cards)
            board.append(turn_card)
            used_cards.add(turn_card)

        # next_card 候補（まだ出ていないカードすべて）
        all_cards = generate_all_cards()
        next_card_candidates = [c for c in all_cards if c not in used_cards]

        for next_card in next_card_candidates:
            full_board = board + [next_card]
            winrate = calculate_winrate(hand, full_board)

            if next_card not in shift_records:
                shift_records[next_card] = []

            shift = winrate - preflop_winrate
            shift_records[next_card].append(shift)

    # 平均化してランキング用データフレームに
    rows = []
    for card, shifts in shift_records.items():
        avg_shift = sum(shifts) / len(shifts)
        feature = extract_features_for_next_card(hand, card, board)
        rows.append({"card": card, "shift": avg_shift, "feature": feature})

    df = pd.DataFrame(rows)
    df.sort_values("shift", ascending=False, inplace=True)
    return df

# 補助関数
def hand_to_cards(hand_str):
    """'AKs' → ['Ah', 'Kh'] などの簡易変換。ここではスート無視して仮カード返す"""
    rank_map = {'T':'10', 'J':'J', 'Q':'Q', 'K':'K', 'A':'A'}
    if hand_str.endswith('s') or hand_str.endswith('o'):
        r1, r2 = hand_str[0], hand_str[1]
    else:
        r1, r2 = hand_str[0], hand_str[1]

    return [r1 + 'h', r2 + 'd'] if r1 != r2 else [r1 + 'h', r2 + 'd']

def generate_all_cards():
    """全52枚のカードを返す"""
    suits = ['h', 'd', 'c', 's']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    return [r + s for r in ranks for s in suits]

def random_card(exclude):
    """used_cards に含まれないランダムカード1枚を返す"""
    deck = generate_all_cards()
    candidates = [c for c in deck if c not in exclude]
    return random.choice(candidates)
