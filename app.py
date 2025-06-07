import streamlit as st
import random
from calculate_winrate_detailed_v2 import run_winrate_evolution_by_floptype
from static_preflop_dict import preflop_winrates_vs_25_range

st.set_page_config(page_title="勝率変動ランキング", layout="wide")
st.title("💥 勝率変動ランキングアプリ")

# --- スターティングハンド（169通り） ---
ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
hand_options = []
for i in range(len(ranks)):
    for j in range(len(ranks)):
        if i < j:
            hand_options.append(ranks[i] + ranks[j] + 's')
            hand_options.append(ranks[i] + ranks[j] + 'o')
        elif i == j:
            hand_options.append(ranks[i] + ranks[j])
hand = st.selectbox("あなたのハンドを選んでください", hand_options)
preflop_winrate = preflop_winrates_vs_25_range.get(hand, None)

# --- フロップタイプ ---
flop_type = st.selectbox("フロップタイプを選んでください", [
    "hit+2suit", "no_hit_mixed", "2connect", "paired_board",
    "monotone", "highcard_dry", "lowcard_dry"
])

# --- ステージ選択 ---
stage = st.radio("次に落ちるカードは？", ["ターン", "リバー"])
stage_flag = "turn" if stage == "ターン" else "river"

# --- モンテカルロ試行回数の選択 ---
num_simulations = st.selectbox("モンテカルロ試行回数", [1000, 10000, 50000, 100000])

# --- 実行 ---
if st.button("勝率変動ランキングを表示"):
    if preflop_winrate is None:
        st.error("このハンドのプリフロップ勝率データがありません。")
    else:
        with st.spinner("計算中..."):
            try:
                df_result = run_winrate_evolution_by_floptype(
                    hand, flop_type, stage_flag, preflop_winrate, num_simulations
                )
                st.success("計算完了！")
                st.subheader("📈 勝率上昇ランキング Top10")
                st.dataframe(df_result.head(10))
                st.subheader("📉 勝率下降ランキング Top10")
                st.dataframe(df_result.sort_values("shift", ascending=True).head(10))
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
