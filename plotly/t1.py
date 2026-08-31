import mysql.connector
import pandas as pd


def connect_database():
    """連接 MySQL 資料庫"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="nba"
    )

    return connection


def export_players_to_csv():
    """讀取 players table 並輸出 CSV"""

    # 連接資料庫
    connection = connect_database()

    try:
        # 讀取 players table 全部資料
        query = "SELECT * FROM players"

        df = pd.read_sql(query, connection)

        # 輸出 CSV
        df.to_csv(
            "data/player.csv",
            index=False,
            encoding="utf-8-sig"
        )

        print("資料匯出成功！")
        print(f"資料筆數：{len(df)}")
        print("輸出檔案：data/player.csv")

    finally:
        # 關閉資料庫連線
        connection.close()


def main():
    export_players_to_csv()


if __name__ == "__main__":
    main()