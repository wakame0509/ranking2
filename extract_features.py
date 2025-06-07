from utils import card_to_rank, card_to_suit, rank_to_int

def extract_features_for_next_card(hand, next_card, board):
    """
    特徴量分類を1つ返す（現状は1カード1特徴量の単純分類）

    hand: ['9h', '9d']
    next_card: 'Qh'
    board: ['7s', '2d', 'Th'] など
    """

    all_board = board + [next_card]
    all_ranks = [card_to_rank(c) for c in all_board]
    all_suits = [card_to_suit(c) for c in all_board]
    unique_ranks = set(all_ranks)
    unique_suits = set(all_suits)

    # --- セット完成 ---
    hand_ranks = set(card_to_rank(c) for c in hand)
    if any(all_ranks.count(r) >= 3 and r in hand_ranks for r in hand_ranks):
        return "Set完成"

    # --- オーバーカード出現（ボードの全カードより大きい）---
    next_value = rank_to_int(card_to_rank(next_card))
    board_values = [rank_to_int(card_to_rank(c)) for c in board]
    if all(next_value > v for v in board_values):
        return "Overcard出現"

    # --- フラッシュ完成 ---
    if all_suits.count(card_to_suit(next_card)) >= 3:  # 簡易チェック（3枚同スート）
        return "Flush完成"

    # --- ストレート完成（簡易チェック）---
    all_values = sorted(set(rank_to_int(r) for r in all_ranks))
    for i in range(len(all_values) - 4 + 1):
        if all_values[i+4] - all_values[i] == 4:
            return "Straight完成"

    return "その他"
