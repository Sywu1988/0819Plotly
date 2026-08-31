import mysql.connector
import pandas as pd
import plotly.express as px


# ==========================================
# 1. 連接 MySQL
# ==========================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="nba"
)


# ==========================================
# 2. 使用 pandas 讀取兩張 Table
# ==========================================

career_df = pd.read_sql(
    "SELECT * FROM career_summaries",
    conn
)

players_df = pd.read_sql(
    "SELECT * FROM players",
    conn
)


# ==========================================
# 3. 關閉資料庫連線
# ==========================================

conn.close()


# ==========================================
# 4. 兩張表用 personId Join
# ==========================================

df = pd.merge(
    career_df,
    players_df,
    on="personId",
    how="inner"
)


# ==========================================
# 5. 根據 firstName 找 LeBron 和 Carmelo
# ==========================================

df = df[
    df["firstName"].isin(["LeBron", "Carmelo"])
].copy()


# ==========================================
# 6. 要分析的欄位
# ==========================================

stats = ["ppg", "rpg", "apg", "bpg", "mpg"]


# ==========================================
# 7. 將數值轉成 0~10
#
# 每一個欄位都使用「所有球員」的最大值
# ==========================================

for col in stats:

    # career_summaries 全部球員的最大值
    max_value = career_df[col].max()

    # 轉換成 0~10
    df[col + "_score"] = (
        df[col] / max_value * 10
    )


# ==========================================
# 8. 整理 Plotly Radar Chart 資料
# ==========================================

score_cols = [col + "_score" for col in stats]

radar_df = df[
    ["firstName"] + score_cols
].copy()


# ==========================================
# 9. 改成 Plotly line_polar 需要的格式
# ==========================================

plot_df = radar_df.melt(
    id_vars="firstName",
    value_vars=score_cols,
    var_name="Stat",
    value_name="Score"
)


# 去掉 "_score"
plot_df["Stat"] = plot_df["Stat"].str.replace(
    "_score",
    "",
    regex=False
)


# ==========================================
# 10. Plotly line_polar
# ==========================================

fig = px.line_polar(
    plot_df,
    r="Score",
    theta="Stat",
    color="firstName",
    line_close=True,
    markers=True,
    range_r=[0, 10],
    title="LeBron vs Carmelo NBA Career Radar"
)


# ==========================================
# 11. 顯示圖形
# ==========================================

fig.show()