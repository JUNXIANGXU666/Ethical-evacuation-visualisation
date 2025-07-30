import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Evacuation Strategy Demo", layout="wide")
st.title("Three Evacuation Strategy Visualisation")

# Sidebar controls
st.sidebar.header("Scenario Setup")
disaster = st.sidebar.selectbox("Disaster Type", ["Flood", "Wildfire", "Earthquake"])
selected_strategies = st.sidebar.multiselect(
    "Select Strategies to Display",
    ["Shortest Path", "Ethical decision-making balance", "Vulnerable Priority"],
    default=[]
)

# Simulated node coordinates
node_coords = {
    "Node_1": [-33.870, 151.200],
    "Node_2": [-33.865, 151.210],
    "Node_3": [-33.860, 151.220],
    "Node_4": [-33.855, 151.230],
    "Node_5": [-33.850, 151.240],
    "Node_6": [-33.845, 151.250],
    "Node_7": [-33.850, 151.225],
    "Node_8": [-33.860, 151.205]
}

vulnerable_nodes = {"Node_3", "Node_5", "Node_7"}

edges = [
    ("Node_1", "Node_2"), ("Node_2", "Node_3"), ("Node_3", "Node_4"), ("Node_4", "Node_5"), ("Node_5", "Node_6"),
    ("Node_1", "Node_8"), ("Node_8", "Node_7"), ("Node_7", "Node_5"), ("Node_2", "Node_7"), ("Node_7", "Node_6")
]

paths = {
    "Shortest Path": ["Node_1", "Node_2", "Node_3", "Node_4"],
    "Ethical decision-making balance": ["Node_1", "Node_8", "Node_7", "Node_5"],
    "Vulnerable Priority": ["Node_1", "Node_2", "Node_7", "Node_6"]
}

colors = {
    "Shortest Path": "red",
    "Ethical decision-making balance": "blue",
    "Vulnerable Priority": "green"
}

# Create base map
m = folium.Map(location=[-33.86, 151.22], zoom_start=13)
for u, v in edges:
    folium.PolyLine([node_coords[u], node_coords[v]], color="gray", weight=1, opacity=0.4).add_to(m)

for strategy in selected_strategies:
    coords = [node_coords[n] for n in paths[strategy]]
    folium.PolyLine(coords, color=colors[strategy], weight=5, opacity=0.9, tooltip=strategy).add_to(m)

for node, coord in node_coords.items():
    popup = f"{node}<br>Vulnerable Area: {'Yes' if node in vulnerable_nodes else 'No'}"
    folium.Marker(location=coord, popup=popup).add_to(m)

legend = """
<div style="position: fixed; bottom: 30px; left: 30px; z-index:9999; font-size:14px;
             background-color:white; padding:10px; border:2px solid grey;">
<b>Strategy Legend</b><br>
<span style="color:red;">■</span> Shortest Path<br>
<span style="color:blue;">■</span> Ethical decision-making balance<br>
<span style="color:green;">■</span> Vulnerable Priority
</div>
"""
m.get_root().html.add_child(folium.Element(legend))

st.subheader("Evacuation network (nodes and routes) on a real map")
st_folium(m, width=1100, height=500)

df_all = pd.DataFrame({
    "Strategy": ["Shortest Path", "Ethical decision-making balance", "Vulnerable Priority"],
    "Path Length (km)": [4.5, 4.7, 3.8],
    "Evacuees Covered": [950, 1200, 900],
    "Fairness Score": [0.6, 0.95, 0.85]
})
df_selected = df_all[df_all["Strategy"].isin(selected_strategies)]
st.subheader("Strategy Performance Comparison Table")
st.dataframe(df_selected, use_container_width=True)

# Radar chart
if st.checkbox("Show Ethical Metric Radar Chart", value=False):
    st.subheader("Ethical Metrics for Each Strategy")
    ethical_df = pd.DataFrame({
        "Metric": ["EEI", "WVPPR", "EPE", "NFII", "CCDI"],
        "Shortest Path": [0.65, 0.55, 0.30, 0.70, 0.65],
        "Ethical decision-making balance": [0.85, 0.95, 0.90, 0.85, 0.50],
        "Vulnerable Priority": [0.75, 0.80, 0.75, 0.60, 0.55]
    })

    categories = ethical_df["Metric"].tolist()
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6.5, 5.5), subplot_kw=dict(polar=True))

    for strategy in selected_strategies:
        values = ethical_df[strategy].tolist()
        values += values[:1]
        ax.plot(angles, values, label=strategy)
        ax.fill(angles, values, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticklabels([])
    ax.set_title("Ethical Metric Comparison", fontsize=14, pad=20)

    ax.legend(
        loc='center left',
        bbox_to_anchor=(1.1, 0.5),
        frameon=True,
        borderaxespad=0.5
    )

    st.pyplot(fig)
    st.markdown("**Ethical Metric Table**")
    st.dataframe(ethical_df, use_container_width=True)