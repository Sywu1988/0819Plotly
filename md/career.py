import mysql.connector
import pandas as pd
import plotly.express as px


def connect_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="nba"
    )
    return conn


def read_career_summaries(conn):
    query = "SELECT * FROM career_summaries"
    df = pd.read_sql(query, conn)
    return df


def plot_scatter(df):
    fig = px.scatter(
        df,
        x="ppg",
        y="rpg",
        title="PPG vs RPG",
        labels={
            "ppg": "Points Per Game (PPG)",
            "rpg": "Rebounds Per Game (RPG)"
        }
    )

    fig.show()


def main():
    conn = connect_database()

    try:
        df = read_career_summaries(conn)

        print(df)

        plot_scatter(df)

    finally:
        conn.close()


if __name__ == "__main__":
    main()