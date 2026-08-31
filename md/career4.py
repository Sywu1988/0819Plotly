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
    # 4. 清理需要的欄位
    # =========================
    df = df.dropna(
        subset=["ppg", "rpg", "pos", "heightMeters"]
    )

    # 確保身高、得分、籃板為數值
    df["heightMeters"] = pd.to_numeric(
        df["heightMeters"],
        errors="coerce"
    )

    df["ppg"] = pd.to_numeric(
        df["ppg"],
        errors="coerce"
    )

    df["rpg"] = pd.to_numeric(
        df["rpg"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["heightMeters", "ppg", "rpg"]
    )

    # =========================
    # 5. 將身高分成 6 個等級
    # =========================
    min_height = df["heightMeters"].min()
    max_height = df["heightMeters"].max()

    # 以最矮球員為基準，將身高等距分成 6 級
    bins = [
        min_height,
        min_height + (max_height - min_height) / 6,
        min_height + (max_height - min_height) / 6 * 2,
        min_height + (max_height - min_height) / 6 * 3,
        min_height + (max_height - min_height) / 6 * 4,
        min_height + (max_height - min_height) / 6 * 5,
        max_height + 0.001
    ]

    df["heightLevel"] = pd.cut(
        df["heightMeters"],
        bins=bins,
        labels=[1, 2, 3, 4, 5, 6],
        include_lowest=True
    )

    # 轉成數字，才能當 size
    df["heightLevel"] = df["heightLevel"].astype(int)

    # =========================
    # 6. 顯示身高等級資訊
    # =========================
    print("最矮身高：", min_height)
    print("最高身高：", max_height)

    print("\n身高等級分布：")
    print(
        df.groupby("heightLevel", observed=False)["heightMeters"]
        .agg(["min", "max", "count"])
    )

    # =========================
    # 7. Plotly Scatter
    # =========================
    fig = px.scatter(
        df,
        x="ppg",
        y="rpg",
        color="pos",
        size="heightLevel",
        hover_name="personId",
        hover_data={
            "ppg": True,
            "rpg": True,
            "pos": True,
            "heightMeters": True,
            "heightLevel": True
        },
        size_max=35,
        title="得分籃板關係圖",
        labels={
            "ppg": "平均每場得分",
            "rpg": "平均每場籃板",
            "pos": "位置",
            "heightLevel": "身高等級",
            "heightMeters": "身高（公尺）"
        }
    )

    # =========================
    # 8. 顯示圖表
    # =========================
    fig.show()


if __name__ == "__main__":
    main()