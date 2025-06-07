import eval7
import random
from utils import hand_to_cards

# ✅ 事前にスート展開された25%レンジ（重複なし・固定化）
from preflop_range_expanded import opponent_hands_25_range

def calculate_winrate(hero_hand, board, num_simulations=1000):
    hero_cards = hand_to_cards(hero_hand)
    hero_hand_eval = hero_cards[:2]

    deck = eval7.Deck()
    for card in hero_cards + board:
        deck.cards.remove(eval7.Card(card))

    wins, ties = 0, 0

    for _ in range(num_simulations):
        # 相手の手札をランダムに選ぶ（25%レンジから）
        opp_hand = random.choice(opponent_hands_25_range)
        if any(c in hero_hand_eval or c in board for c in opp_hand):
            continue  # 重複防止

        # 残りのボードカードを補完（最大5枚に）
        total_board = board + []
        while len(total_board) < 5:
            card = deck.peek()
            if card not in hero_hand_eval and card not in opp_hand and str(card) not in total_board:
                total_board.append(str(card))
                deck.shuffle()  # ランダム性を保つために適度に混ぜる

        hero_full = [eval7.Card(c) for c in hero_hand_eval + total_board]
        opp_full = [eval7.Card(c) for c in opp_hand + total_board]

        hero_score = eval7.evaluate(hero_full)
        opp_score = eval7.evaluate(opp_full)

        if hero_score > opp_score:
            wins += 1
        elif hero_score == opp_score:
            ties += 1

    total = wins + ties + (num_simulations - wins - ties)
    winrate = (wins + ties / 2) / total * 100
    return round(winrate, 2)
