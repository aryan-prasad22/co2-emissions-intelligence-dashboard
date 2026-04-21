from sklearn.cluster import KMeans
import numpy as np

def cluster_countries(df):
    latest = df[df['year'] == df['year'].max()].copy()

    X = latest[['co2', 'co2_per_capita']]

    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    latest['cluster'] = model.fit_predict(X)

    return latest


def forecast_country(df, country):
    data = df[df['country'] == country].sort_values('year')

    if len(data) < 10:
        return data, None

    y = data['co2'].values
    x = np.arange(len(y))

    coeffs = np.polyfit(x, y, 1)
    future_x = np.arange(len(y), len(y) + 5)

    forecast = np.polyval(coeffs, future_x)

    return data, forecast