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
    # 2. 讀取兩張 Table
    # =========================
    career_summaries = pd.read_sql(
        "SELECT * FROM career_summaries",
        conn
    )

    players = pd.read_sql(
        "SELECT * FROM players",
        conn
    )

    # 關閉資料庫連線
    conn.close()

    # =========================
    # 3. 用 personId Join
    # =========================
    df = pd.merge(
        career_summaries,
        players,
        on="personId",
        how="inner"
    )

    # =========================
    # 4. 確認需要的欄位
    # =========================
    df["ppg"] = pd.to_numeric(df["ppg"], errors="coerce")
    df["rpg"] = pd.to_numeric(df["rpg"], errors="coerce")
    df["heightMeters"] = pd.to_numeric(
        df["heightMeters"],
        errors="coerce"
    )

    # 移除沒有必要資料的球員
    df = df.dropna(
        subset=["ppg", "rpg", "pos", "heightMeters"]
    )

    # =========================
    # 5. 將身高分成 6 個等級
    # =========================
    min_height = df["heightMeters"].min()
    max_height = df["heightMeters"].max()

    print(f"最矮身高：{min_height:.2f} m")
    print(f"最高身高：{max_height:.2f} m")

    df["heightLevel"] = pd.cut(
        df["heightMeters"],
        bins=6,
        labels=[1, 2, 3, 4, 5, 6],
        include_lowest=True
    )

    # =========================
    # 6. 將 6 個等級轉成 size
    # =========================
    size_map = {
        1: 10,
        2: 14,
        3: 18,
        4: 22,
        5: 26,
        6: 30
    }

    df["size"] = (
        df["heightLevel"]
        .astype(int)
        .map(size_map)
    )

    # =========================
    # 7. Plotly Scatter
    # =========================
    fig = px.scatter(
        df,
        x="ppg",
        y="rpg",
        color="pos",
        size="size",
        hover_data=[
            "personId",
            "ppg",
            "rpg",
            "pos",
            "heightMeters",
            "heightLevel"
        ],
        title="NBA Players: PPG vs RPG"
    )

    # =========================
    # 8. 顯示圖表
    # =========================
    fig.show()


if __name__ == "__main__":
    main()