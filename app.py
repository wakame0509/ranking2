import streamlit as st
import random
from calculate_winrate_detailed_v2 import run_winrate_evolution_by_floptype
from static_preflop_dict import preflop_winrates_vs_25_range  # ← 追加

st.set_page_config(page_title="勝率変動ランキング", layout="wide")
st.title("💥 勝率変動ランキングアプリ")

# --- 169通りのスターティングハンドを生成 ---
ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
hand_options = []

for i in range(len(ranks)):
    for j in range(len(ranks)):
        if i < j:
            hand_options.append(ranks[i] + ranks[j] + 's')
            hand_options.append(ranks[i] + ranks[j] + 'o')
        elif i == j:
            hand_options.append(ranks[i] + ranks[j])

# --- ハンド選択 ---
hand = st.selectbox("あなたのハンドを選んでください", hand_options)

# --- プリフロップ勝率取得（辞書にない場合は None）---
preflop_winrate = preflop_winrates_vs_25_range.get(hand, None)

# --- フロップタイプ選択（v1.1：7通り） ---
flop_type = st.selectbox("フロップタイプを選んでください", [
    "hit+2suit", "no_hit_mixed", "2connect", "paired_board",
    "monotone", "highcard_dry", "lowcard_dry"
])

# --- ステージ選択（ターン or リバー） ---
stage = st.radio("次に落ちるカードは？", ["ターン", "リバー"])
stage_flag = "turn" if stage == "ターン" else "river"

# --- 実行ボタン ---
if st.button("勝率変動ランキングを表示"):
    if preflop_winrate is None:
        st.error("このハンドのプリフロップ勝率データが存在しません。")
    else:
        with st.spinner("計算中...（少しお待ちください）"):
            try:
                df_result = run_winrate_evolution_by_floptype(
                    hand, flop_type, stage_flag, preflop_winrate  # ← 渡す
                )

                st.success("計算完了！")

                st.subheader("📈 勝率上昇ランキング Top10")
                st.dataframe(df_result.head(10))

                st.subheader("📉 勝率下降ランキング Top10")
                st.dataframe(df_result.sort_values("shift", ascending=True).head(10))

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
