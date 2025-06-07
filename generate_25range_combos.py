from itertools import combinations

def generate_25percent_range_combos():
    """
    25%レンジに含まれるスート付きハンドコンボ（例：'AhKh', 'AdKd', ...）をすべて返す
    重複を除外
    """
    suited_hands = ['AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'QJs', 'JTs', 'T9s',
                    '98s', '87s', '76s', '65s', '54s']
    offsuit_hands = ['AKo', 'AQo', 'AJo', 'KQo', 'KJo', 'QJo', 'JTo']
    pairs = ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55']

    suits = ['h', 'd', 'c', 's']
    combos = []

    # ペア展開（同ランクの異なるスート）
    for pair in pairs:
        rank = pair[0]
        for s1, s2 in combinations(suits, 2):
            combos.append(rank + s1)
            combos.append(rank + s2)

    # スーテッド展開
    for hand in suited_hands:
        r1, r2 = hand[0], hand[1]
        for s in suits:
            combos.append(r1 + s)
            combos.append(r2 + s)

    # オフスート展開（スートが異なる）
    for hand in offsuit_hands:
        r1, r2 = hand[0], hand[1]
        for s1 in suits:
            for s2 in suits:
                if s1 != s2:
                    combos.append(r1 + s1)
                    combos.append(r2 + s2)

    # 2枚1組に変換
    combos_grouped = []
    for i in range(0, len(combos), 2):
        c1, c2 = combos[i], combos[i+1]
        # 重複チェック（同じ2枚の組み合わせが逆順含めて重複しないように）
        if {c1, c2} not in [set(pair) for pair in combos_grouped]:
            combos_grouped.append([c1, c2])

    return combos_grouped
