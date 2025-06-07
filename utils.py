def card_to_rank(card):
    """カード 'Ah' → 'A' のようにランクを抽出"""
    return card[0]

def card_to_suit(card):
    """カード 'Ah' → 'h' のようにスートを抽出"""
    return card[1]

def rank_to_int(rank):
    """ランク（文字）→ 数値変換"""
    table = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
             'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    return table.get(rank, 0)

def int_to_rank(value):
    """数値 → ランク文字"""
    table = {2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9',
             10:'T', 11:'J', 12:'Q', 13:'K', 14:'A'}
    return table.get(value, '?')
