import mysql.connector
import pandas as pd
import plotly.express as px


def main():

    # ========================================
    # 1. 連接 MySQL
    # ========================================
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="nba"
    )

    # ========================================
    # 2. 讀取 career_summaries
    # ========================================
    career_query = """
        SELECT *
        FROM career_summaries
    """

    career_df = pd.read_sql(career_query, conn)

    # ========================================
    # 3. 讀取 players
    # ========================================
    players_query = """
        SELECT *
        FROM players
    """

    players_df = pd.read_sql(players_query, conn)

    # 關閉資料庫
    conn.close()

    # ========================================
    # 4. 兩張表使用 personId Join
    # ========================================
    df = pd.merge(
        career_df,
        players_df,
        on="personId",
        how="inner"
    )

    # ========================================
    # 5. 清理需要使用的欄位
    # ========================================
    columns = [
        "personId",
        "ppg",
        "rpg",
        "apg",
        "pos",
        "heightMeters"
    ]

    df = df[columns].copy()

    # 將數值欄位轉成 numeric
    df["ppg"] = pd.to_numeric(df["ppg"], errors="coerce")
    df["rpg"] = pd.to_numeric(df["rpg"], errors="coerce")
    df["apg"] = pd.to_numeric(df["apg"], errors="coerce")
    df["heightMeters"] = pd.to_numeric(
        df["heightMeters"],
        errors="coerce"
    )

    # 移除缺失值
    df = df.dropna(
        subset=[
            "ppg",
            "rpg",
            "apg",
            "pos",
            "heightMeters"
        ]
    )

    # ========================================
    # 6. 身高分成 6 個等級
    #
    # 以最矮球員為基準，
    # 將「最矮 ~ 最高」平均切成 6 個區間
    # ========================================

    min_height = df["heightMeters"].min()
    max_height = df["heightMeters"].max()

    # 如果所有球員身高都一樣，避免除以 0
    if min_height == max_height:
        df["height_level"] = 1
    else:
        # 利用等距區間分成 6 級
        bins = [
            min_height + (max_height - min_height) * i / 6
            for i in range(7)
        ]

        # 確保最後一個區間包含最高身高
        bins[-1] = max_height + 0.001

        df["height_level"] = pd.cut(
            df["heightMeters"],
            bins=bins,
            labels=[1, 2, 3, 4, 5, 6],
            include_lowest=True
        ).astype(int)

    # ========================================
    # 7. 將身高等級轉成 Size
    # ========================================
    size_mapping = {
        1: 8,
        2: 12,
        3: 16,
        4: 20,
        5: 25,
        6: 30
    }

    df["size"] = df["height_level"].map(size_mapping)

    # ========================================
    # 8. Plotly 3D Scatter
    # ========================================
    fig = px.scatter_3d(
        df,
        x="ppg",
        y="rpg",
        z="apg",
        color="pos",
        size="size",
        hover_name="personId",
        hover_data={
            "ppg": ":.1f",
            "rpg": ":.1f",
            "apg": ":.1f",
            "heightMeters": ":.2f",
            "height_level": True,
            "size": False
        },
        title="得分籃板助攻3D圖",
        labels={
            "ppg": "平均每場得分",
            "rpg": "平均每場籃板",
            "apg": "平均每場助攻",
            "pos": "位置",
            "heightMeters": "身高（m）",
            "height_level": "身高等級"
        }
    )

    # ========================================
    # 9. 調整圖表大小
    # ========================================
    fig.update_layout(
        width=1000,
        height=800
    )

    # ========================================
    # 10. 顯示圖表
    # ========================================
    fig.show()


if __name__ == "__main__":
    main()