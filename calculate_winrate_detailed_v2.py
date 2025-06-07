import random
import pandas as pd
from generate_flops_by_type import generate_flops_by_type
from calculate_winrate import calculate_winrate
from extract_features import extract_features_for_next_card

def run_winrate_evolution_by_floptype(hand, flop_type, stage, preflop_winrate, num_simulations=100000):
    """
    指定ハンド・フロップタイプ・ステージに対する勝率変動を計算し、ランキングを返す
    """
    shift_records = {}

    # フロップ候補を全通り生成
    flop_list = generate_flops_by_type(hand, flop_type)

    for flop in flop_list:
        used_cards = set(hand_to_cards(hand) + flop)
        board = flop.copy()

        # ターンの処理（リバーの場合のみ）
        if stage == "river":
            turn_card = draw_random_card(exclude=used_cards)
            board.append(turn_card)
            used_cards.add(turn_card)

        # 全カードから next_card 候補を抽出（未使用カード）
        all_cards = generate_full_deck()
        next_card_candidates = [c for c in all_cards if c not in used_cards]

        # 各 next_card について勝率計算とシフトを記録
        for next_card in next_card_candidates:
            full_board = board + [next_card]
            winrate = calculate_winrate(hand, full_board, num_simulations)

            if next_card not in shift_records:
                shift_records[next_card] = []

            shift = winrate - preflop_winrate
            shift_records[next_card].append(shift)

    # 平均化してランキング形式に変換
    rows = []
    for card, shifts in shift_records.items():
        avg_shift = sum(shifts) / len(shifts)
        feature = extract_features_for_next_card(hand_to_cards(hand), card, board)
        rows.append({
            "card": card,
            "shift": avg_shift,
            "feature": feature
        })

    df = pd.DataFrame(rows)
    df.sort_values("shift", ascending=False, inplace=True)
    return df

# 補助関数群
def hand_to_cards(hand_str):
    """'AKs' → ['Ah', 'Kh'] のように仮想カードを返す（スート重視しない簡略版）"""
    r1, r2 = hand_str[0], hand_str[1]
    if r1 == r2:
        return [r1 + 'h', r2 + 'd']
    elif hand_str[2] == 's':
        return [r1 + 'h', r2 + 'h']
    else:
        return [r1 + 'h', r2 + 'd']

def generate_full_deck():
    suits = ['h', 'd', 'c', 's']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    return [r + s for r in ranks for s in suits]

def draw_random_card(exclude):
    """exclude されていないカードから1枚ランダムに返す"""
    candidates = [c for c in generate_full_deck() if c not in exclude]
    return random.choice(candidates)
