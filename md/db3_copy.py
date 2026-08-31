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
# 2. 讀取 career_summaries
# ==========================================
career_query = """
SELECT *
FROM career_summaries
"""

career_df = pd.read_sql(career_query, conn)


# ==========================================
# 3. 讀取 players
# ==========================================
players_query = """
SELECT *
FROM players
"""

players_df = pd.read_sql(players_query, conn)


# ==========================================
# 4. 關閉資料庫連線
# ==========================================
conn.close()


# ==========================================
# 5. 用 personId JOIN 兩張表
# ==========================================
df = pd.merge(
    career_df,
    players_df,
    on="personId",
    how="inner"
)


# ==========================================
# 6. 根據 firstName 找 LeBron / Carmelo
# ==========================================
df = df[
    df["firstName"].isin(["LeBron", "Carmelo"])
].copy()


# 查看找到的球員
print(df[["personId", "firstName", "lastName"]])


# ==========================================
# 7. 要分析的數值欄位
# ==========================================
stats = ["ppg", "rpg", "apg", "bpg", "mpg"]


# ==========================================
# 8. 將各欄位 0 ~ 最大值
#    線性轉換成 0 ~ 10
# ==========================================
for col in stats:

    max_value = df[col].max()

    if max_value != 0:
        df[col + "_score"] = (df[col] / max_value) * 10
    else:
        df[col + "_score"] = 0


# ==========================================
# 9. 整理 Plotly 使用的資料
# ==========================================
score_cols = [col + "_score" for col in stats]

plot_df = df[
    ["firstName", "lastName"] + score_cols
].copy()


# ==========================================
# 10. 將資料轉成長格式
# ==========================================
plot_df = plot_df.melt(
    id_vars=["firstName", "lastName"],
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
# 11. 球員名稱
# ==========================================
plot_df["Player"] = (
    plot_df["firstName"]
    + " "
    + plot_df["lastName"]
)


# ==========================================
# 12. Plotly line_polar
# ==========================================
fig = px.line_polar(
    plot_df,
    r="Score",
    theta="Stat",
    color="Player",
    line_close=True,
    markers=True,
    title="LeBron vs Carmelo - NBA Career Statistics"
)


# ==========================================
# 13. 設定雷達圖最大值 10
# ==========================================
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 10]
        )
    )
)


# ==========================================
# 14. 顯示圖形
# ==========================================
fig.show()