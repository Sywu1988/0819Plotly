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
    career_sql = """
        SELECT *
        FROM career_summaries
    """

    career_df = pd.read_sql(career_sql, conn)

    # =========================
    # 3. 讀取 players
    # =========================
    players_sql = """
        SELECT *
        FROM players
    """

    players_df = pd.read_sql(players_sql, conn)

    # =========================
    # 4. 關閉資料庫
    # =========================
    conn.close()

    # =========================
    # 5. 兩張表用 personId JOIN
    # =========================
    df = pd.merge(
        career_df,
        players_df,
        on="personId",
        how="inner"
    )

    # =========================
    # 6. 查看 JOIN 後資料
    # =========================
    print(df.head())
    print(f"JOIN 後共有 {len(df)} 筆資料")

    # =========================
    # 7. Plotly Scatter
    # =========================
    fig = px.scatter(
        df,
        x="ppg",
        y="rpg",
        color="pos",
        hover_data=["personId"]
    )

    # =========================
    # 8. 圖表設定
    # =========================
    fig.update_layout(
        title="NBA Players: PPG vs RPG",
        xaxis_title="Points Per Game (PPG)",
        yaxis_title="Rebounds Per Game (RPG)"
    )

    # =========================
    # 9. 顯示圖表
    # =========================
    fig.show()


if __name__ == "__main__":
    main()