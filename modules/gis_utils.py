"""
gis_utils.py
Helpers to build pydeck layers for the GIS risk dashboard: colored
risk markers, a heatmap layer, and consistent color coding across the app.
"""

import pydeck as pdk

RISK_COLORS = {
    "Low": [46, 204, 113, 190],       # green
    "Medium": [241, 196, 15, 190],    # yellow
    "High": [230, 126, 34, 200],      # orange
    "Critical": [231, 76, 60, 220],   # red
}


def color_for(category: str):
    return RISK_COLORS.get(category, [149, 165, 166, 180])


def build_risk_scatter_layer(df):
    """df must have lat, lon, risk_category, risk_score, name columns; adds a color col."""
    data = df.copy()
    data["color"] = data["risk_category"].apply(color_for)
    data["radius"] = 2500 + data["risk_score"] * 60
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position="[lon, lat]",
        get_fill_color="color",
        get_radius="radius",
        pickable=True,
        opacity=0.75,
        stroked=True,
        get_line_color=[40, 40, 40],
        line_width_min_pixels=1,
    )
    return layer


def build_heatmap_layer(df):
    layer = pdk.Layer(
        "HeatmapLayer",
        data=df,
        get_position="[lon, lat]",
        get_weight="risk_score",
        radius_pixels=60,
        opacity=0.6,
    )
    return layer


def default_view_state():
    # centered roughly on the North Eastern Region of India
    return pdk.ViewState(latitude=25.6, longitude=92.5, zoom=6.0, pitch=30)


def build_deck(df, show_heatmap: bool = True, show_markers: bool = True):
    layers = []
    if show_heatmap:
        layers.append(build_heatmap_layer(df))
    if show_markers:
        layers.append(build_risk_scatter_layer(df))
    tooltip = {
        "html": "<b>{name}</b><br/>State: {state}<br/>Risk: {risk_category} ({risk_score}/100)",
        "style": {"backgroundColor": "steelblue", "color": "white"},
    }
    return pdk.Deck(
        layers=layers,
        initial_view_state=default_view_state(),
        tooltip=tooltip,
        map_provider="carto",
        map_style="light",
    )
