import eval7
import random
from generate_25range_combos import generate_25percent_range_combos

# 事前に全ハンド展開済みの25%レンジコンボを取得
OPPONENT_COMBOS_25 = generate_25percent_range_combos()

def calculate_winrate(hand_str, board_cards, num_simulations=100000):
    """
    Monte Carlo シミュレーションで勝率を計算（25%レンジ相手）
    hand_str: 例 'AKs'
    board_cards: 例 ['Ah', 'Kd', 'Ts']
    """

    # 自分の手札を eval7.Card に変換
    hero_hand = convert_hand_str_to_cards(hand_str)
    board = [eval7.Card(c) for c in board_cards]

    wins = 0
    used_cards = set(str(c) for c in hero_hand + board)

    for _ in range(num_simulations):
        # 相手ハンドを25%レンジからランダムに選び、使用カードに含まれていなければ採用
        while True:
            opp_combo = random.choice(OPPONENT_COMBOS_25)
            if not any(c in used_cards for c in opp_combo):
                break
        opp_hand = [eval7.Card(c) for c in opp_combo]

        # 使用済カード更新
        all_used = set(str(c) for c in hero_hand + opp_hand + board)

        # 山札から残りのカードを抽出
        deck = [eval7.Card(c) for c in generate_full_deck() if c not in all_used]

        # 必要なボードカード数（最大5枚まで）
        needed = 5 - len(board)
        sim_board = board + random.sample(deck, needed)

        # 勝敗判定
        score_self = eval7.evaluate(hero_hand + sim_board)
        score_opp = eval7.evaluate(opp_hand + sim_board)

        if score_self > score_opp:
            wins += 1
        elif score_self == score_opp:
            wins += 0.5

    return 100 * wins / num_simulations

def convert_hand_str_to_cards(hand_str):
    r1, r2 = hand_str[0], hand_str[1]
    if r1 == r2:
        return [eval7.Card(r1 + 'h'), eval7.Card(r2 + 'd')]
    elif hand_str[2] == 's':
        return [eval7.Card(r1 + 'h'), eval7.Card(r2 + 'h')]
    else:
        return [eval7.Card(r1 + 'h'), eval7.Card(r2 + 'd')]

def generate_full_deck():
    suits = ['h', 'd', 'c', 's']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    return [r + s for r in ranks for s in suits]
