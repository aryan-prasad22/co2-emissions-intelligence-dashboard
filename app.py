import streamlit as st
import plotly.express as px
from analysis import load_data
from model import cluster_countries, forecast_country

st.set_page_config(page_title="CO₂ Dashboard", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.main {background-color: #0e1117; color: white;}
h1, h2, h3 {color: #00c6ff;}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
@st.cache_data
def get_data():
    return load_data()

df = get_data()

st.title("🌍 CO₂ Emissions Intelligence Dashboard")

# ---------- SIDEBAR ----------
st.sidebar.header("Filters")

year = st.sidebar.slider(
    "Select Year",
    int(df['year'].min()),
    int(df['year'].max()),
    int(df['year'].max())
)

country = st.sidebar.selectbox(
    "Select Country",
    sorted(df['country'].unique())
)

filtered = df[df['year'] == year]

# ---------- METRICS ----------
col1, col2, col3 = st.columns(3)
col1.metric("Countries", filtered['country'].nunique())
col2.metric("Year", year)
col3.metric("Records", len(filtered))

# ---------- TOP EMITTERS ----------
st.subheader("🔥 Top CO₂ Emitters")

top = filtered.sort_values(by="co2", ascending=False).head(10)

fig_bar = px.bar(
    top,
    x="co2",
    y="country",
    orientation="h",
    color="co2",
    color_continuous_scale="reds"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ---------- MAP ----------
st.subheader("🌎 Global Emissions Map")

fig_map = px.choropleth(
    filtered,
    locations="country",
    locationmode="country names",
    color="co2",
    hover_name="country",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_map, use_container_width=True)

# ---------- CLUSTER ----------
st.subheader("📊 Country Segmentation")

clustered = cluster_countries(df)
clustered_year = clustered[clustered['year'] == year]

fig_cluster = px.scatter(
    clustered_year,
    x="co2",
    y="co2_per_capita",
    color="cluster",
    hover_name="country"
)

st.plotly_chart(fig_cluster, use_container_width=True)

# ---------- FORECAST ----------
st.subheader("📈 Emissions Forecast")

data, forecast = forecast_country(df, country)

fig_line = px.line(data, x="year", y="co2", title=f"{country} CO₂ Trend")

if forecast is not None:
    future_years = list(range(data['year'].max()+1, data['year'].max()+6))
    fig_line.add_scatter(x=future_years, y=forecast, mode='lines', name='Forecast')

st.plotly_chart(fig_line, use_container_width=True)

# ---------- ANIMATION ----------
st.subheader("🎬 Global Emissions Over Time")

fig_anim = px.scatter(
    df,
    x="co2",
    y="co2_per_capita",
    animation_frame="year",
    animation_group="country",
    size="co2",
    color="co2",
    hover_name="country"
)

st.plotly_chart(fig_anim, use_container_width=True)

# ---------- INSIGHTS ----------
st.subheader("📌 Key Insights")

top_country = top.iloc[0]['country']

st.markdown(f"""
- 🌍 **{top_country} dominates global emissions in {year}**
- 📊 Clear clustering between high and low emitters
- 📈 Increasing trend in developing economies
- ⚠️ Per capita emissions highlight inequality
""")

# ---------- DOWNLOAD ----------
st.subheader("⬇️ Download Data")

st.download_button(
    label="Download Filtered Data",
    data=filtered.to_csv(index=False),
    file_name="co2_filtered.csv",
    mime="text/csv"
)