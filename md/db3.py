import mysql.connector
import pandas as pd
import plotly.express as px


def main():

    # =========================
    # 1. 連接 MySQL
    # =========================
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="nba"
    )

    # =========================
    # 2. 讀取 career_summaries
    # =========================
    career_query = """
        SELECT *
        FROM career_summaries
    """

    career_df = pd.read_sql(career_query, conn)

    # =========================
    # 3. 讀取 players
    # =========================
    players_query = """
        SELECT *
        FROM players
    """

    players_df = pd.read_sql(players_query, conn)

    # =========================
    # 4. 關閉資料庫
    # =========================
    conn.close()

    # =========================
    # 5. 用 personId Join
    # =========================
    df = pd.merge(
        career_df,
        players_df,
        on="personId",
        how="inner"
    )

    # =========================
    # 6. 找 LeBron 和 Carmelo
    # =========================
    df = df[
        df["firstName"].isin(["LeBron", "Carmelo"])
    ].copy()

    # =========================
    # 7. 查看資料
    # =========================
    print(df[[
        "firstName",
        "lastName",
        "ppg",
        "rpg",
        "apg",
        "bpg",
        "mpg"
    ]])

    # =========================
    # 8. 整理 Plotly line_polar 所需資料
    # =========================
    stats = ["ppg", "rpg", "apg", "bpg", "mpg"]

    plot_df = df[[
        "firstName",
        "lastName",
        "ppg",
        "rpg",
        "apg",
        "bpg",
        "mpg"
    ]].copy()

    # 建立球員名稱
    plot_df["player"] = (
        plot_df["firstName"] + " " + plot_df["lastName"]
    )

    # =========================
    # 9. 寬表轉長表
    # =========================
    long_df = plot_df.melt(
        id_vars="player",
        value_vars=stats,
        var_name="stat",
        value_name="value"
    )

    # =========================
    # 10. Plotly line_polar
    # =========================
    fig = px.line_polar(
        long_df,
        r="value",
        theta="stat",
        color="player",
        line_close=True,
        markers=True,
        title="LeBron James vs Carmelo Anthony Career Statistics"
    )

    # =========================
    # 11. 顯示圖表
    # =========================
    fig.show()


if __name__ == "__main__":
    main()