import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Player Comparison Scatter",
    layout="wide"
)

st.title("Player Comparison Scatter")

df = pd.read_csv("player_season_per90_clean.csv")

# Numeric metric columns
numeric_cols = df.select_dtypes(include="number").columns.tolist()

# Remove ID-style fields from selectable metrics
metric_cols = [
    col for col in numeric_cols
    if col not in ["player_id", "team_id"]
]

# Sidebar filters
st.sidebar.header("Filters")

positions = sorted(df["primary_position"].dropna().unique())
selected_positions = st.sidebar.multiselect(
    "Position",
    options=positions,
    default=positions
)

leagues = sorted(df["competition"].dropna().unique())
selected_leagues = st.sidebar.multiselect(
    "League",
    options=leagues,
    default=leagues
)

min_minutes = int(df["minutes"].fillna(0).min())
max_minutes = int(df["minutes"].fillna(0).max())

selected_minutes = st.sidebar.slider(
    "Minimum minutes",
    min_value=min_minutes,
    max_value=max_minutes,
    value=300,
    step=50
)

# Axis selectors
col1, col2 = st.columns(2)

with col1:
    x_metric = st.selectbox("X-axis metric", metric_cols, index=0)

with col2:
    y_metric = st.selectbox("Y-axis metric", metric_cols, index=1)

# Apply filters
filtered = df[
    (df["primary_position"].isin(selected_positions)) &
    (df["competition"].isin(selected_leagues)) &
    (df["minutes"] >= selected_minutes)
].copy()

st.caption(f"Showing {len(filtered):,} players")

fig = px.scatter(
    filtered,
    x=x_metric,
    y=y_metric,
    hover_name="player_name",
    hover_data={
        "team_name": True,
        "competition": True,
        "primary_position": True,
        "minutes": ":.0f",
        x_metric: ":.2f",
        y_metric: ":.2f",
    },
    color="primary_position",
    size="minutes",
)

fig.update_layout(
    height=750,
    xaxis_title=x_metric,
    yaxis_title=y_metric,
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(
    filtered[[
        "player_name",
        "team_name",
        "competition",
        "primary_position",
        "minutes",
        x_metric,
        y_metric,
    ]].sort_values(y_metric, ascending=False),
    use_container_width=True
)
