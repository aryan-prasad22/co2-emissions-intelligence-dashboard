import pandas as pd

def load_data():
    df = pd.read_csv("data/co2.csv")

    df = df[['country', 'year', 'co2', 'co2_per_capita']]
    df = df.dropna()

    # Reduce dataset for performance
    df = df[df['year'] >= 2000]

    return df


def get_top_emitters(df):
    latest_year = df['year'].max()
    latest = df[df['year'] == latest_year]
    return latest.sort_values(by='co2', ascending=False).head(10)