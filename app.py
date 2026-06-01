import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import random

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Daki Capital — MSA Dashboard",
    page_icon="assets/favicon.png" if False else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand CSS (Daki Capital palette: dark teal #0D4F45, white, light gray) ────
st.markdown("""
<style>
/* Global */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0D4F45;
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #a8d5cc !important;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span {
    color: #ffffff !important;
}

/* Top header bar */
.daki-header {
    background: linear-gradient(135deg, #0D4F45 0%, #1A7A6B 100%);
    padding: 18px 28px;
    border-radius: 8px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.daki-logo-text {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.02em;
}
.daki-logo-sub {
    font-size: 13px;
    color: rgba(255,255,255,0.65);
    margin-top: 2px;
}
.daki-logo-icon {
    width: 44px;
    height: 44px;
}

/* KPI cards */
.kpi-row { display: flex; gap: 12px; margin-bottom: 20px; }
.kpi-card {
    flex: 1;
    background: #ffffff;
    border: 1px solid #e8ede9;
    border-radius: 8px;
    padding: 14px 18px;
    border-top: 3px solid #0D4F45;
}
.kpi-val { font-size: 26px; font-weight: 700; color: #0D4F45; }
.kpi-lbl { font-size: 12px; color: #6b7c75; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.05em; }
.kpi-card.green { border-top-color: #1D9E75; }
.kpi-card.blue  { border-top-color: #378ADD; }
.kpi-card.amber { border-top-color: #BA7517; }
.kpi-card.gray  { border-top-color: #888780; }

/* Tier badges */
.tier-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
}
.tier-alta    { background: #E1F5EE; color: #0F6E56; }
.tier-asset   { background: #E6F1FB; color: #185FA5; }
.tier-macro   { background: #FAEEDA; color: #854F0B; }
.tier-monitor { background: #F1EFE8; color: #5F5E5A; }

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 2px solid #e0e8e5;
}
.stTabs [data-baseweb="tab"] {
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 500;
    color: #6b7c75;
    border-radius: 6px 6px 0 0;
}
.stTabs [aria-selected="true"] {
    background: #0D4F45 !important;
    color: #ffffff !important;
}

/* Section titles */
.section-title {
    font-size: 15px;
    font-weight: 600;
    color: #0D4F45;
    border-left: 3px solid #1D9E75;
    padding-left: 10px;
    margin-bottom: 14px;
}

/* Streamlit metric overrides */
[data-testid="metric-container"] {
    background: #f7faf9;
    border: 1px solid #e0e8e5;
    border-radius: 8px;
    padding: 12px 16px;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ── Scoring constants ─────────────────────────────────────────────────────────
MACRO_VARS = [
    {"key": "pop_growth",      "name": "Crecimiento Poblacional",    "weight": 0.20, "min": 0,        "max": 1,       "higher_is_better": True},
    {"key": "employment",      "name": "Población Empleada",         "weight": 0.10, "min": 0,        "max": 1,       "higher_is_better": True},
    {"key": "education",       "name": "Años de Escolaridad",        "weight": 0.03, "min": 0,        "max": 25,      "higher_is_better": True},
    {"key": "avg_salary",      "name": "Salario Promedio",           "weight": 0.05, "min": 0,        "max": 200000,  "higher_is_better": True},
    {"key": "gdp_per_capita",  "name": "PIB Per Cápita",             "weight": 0.20, "min": 0,        "max": 200000,  "higher_is_better": True},
    {"key": "households",      "name": "Número de Hogares",          "weight": 0.02, "min": 0,        "max": 10000000,"higher_is_better": True},
    {"key": "household_spend", "name": "Consumo Promedio Por Hogar", "weight": 0.20, "min": 0,        "max": 200000,  "higher_is_better": True},
    {"key": "pct_renters",     "name": "% Viviendas Alquiladas",     "weight": 0.10, "min": 0,        "max": 1,       "higher_is_better": True},
    {"key": "ecommerce_index", "name": "Índice E-commerce",          "weight": 0.10, "min": 0,        "max": 1,       "higher_is_better": True},
]
ASSET_VARS = [
    {"key": "rent_growth", "name": "Crecimiento Alquileres",     "weight": 0.1667, "min": 0,    "max": 1,    "higher_is_better": True},
    {"key": "occupancy",   "name": "Ocupación Promedio",         "weight": 0.3333, "min": 0,    "max": 1,    "higher_is_better": True},
    {"key": "pipeline",    "name": "Inventario en Construcción", "weight": 0.1667, "min": 0,    "max": 1,    "higher_is_better": False},
    {"key": "cap_rate",    "name": "Cap Rates",                  "weight": 0.0833, "min": 0.01, "max": 0.15, "higher_is_better": True},
    {"key": "rent_psf",    "name": "Alquiler Por Pie²",          "weight": 0.0833, "min": 1.25, "max": 5,    "higher_is_better": True},
    {"key": "sale_psf",    "name": "Venta Por Pie²",             "weight": 0.1667, "min": 12,   "max": 100,  "higher_is_better": True},
]
MAX_SCORE = 5.0
TIER_COLORS = {
    "Alta Convicción": "#1D9E75",
    "Asset Fuerte":    "#378ADD",
    "Macro Fuerte":    "#BA7517",
    "Monitorear":      "#888780",
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def normalize(value, vmin, vmax, higher_is_better):
    value = max(vmin, min(vmax, float(value)))
    ratio = (value - vmin) / (vmax - vmin) if vmax != vmin else 0
    return ratio if higher_is_better else 1 - ratio

def compute_score(row, var_list):
    total = 0
    for v in var_list:
        if v["key"] in row and pd.notna(row[v["key"]]):
            n = normalize(row[v["key"]], v["min"], v["max"], v["higher_is_better"])
            total += n * v["weight"] * MAX_SCORE
    return round(total, 3)

def assign_tier(macro, asset, macro_mid=3.0, asset_mid=3.25):
    if macro >= macro_mid and asset >= asset_mid:
        return "Alta Convicción"
    elif macro < macro_mid and asset >= asset_mid:
        return "Asset Fuerte"
    elif macro >= macro_mid and asset < asset_mid:
        return "Macro Fuerte"
    else:
        return "Monitorear"

# ── Sample data ───────────────────────────────────────────────────────────────
BASE_DATA = [
    {"msa":"Atlanta","short":"ATL","macro_score":3.02,"asset_score":4.60},
    {"msa":"Austin","short":"AUS","macro_score":3.30,"asset_score":4.63},
    {"msa":"Baltimore","short":"BAL","macro_score":2.54,"asset_score":1.82},
    {"msa":"Boston","short":"BOS","macro_score":1.91,"asset_score":2.17},
    {"msa":"Charlotte","short":"CHL","macro_score":4.25,"asset_score":1.33},
    {"msa":"Chicago","short":"CHI","macro_score":2.54,"asset_score":1.36},
    {"msa":"Cincinnati","short":"CIN","macro_score":0.98,"asset_score":0.97},
    {"msa":"Cleveland","short":"CLE","macro_score":4.28,"asset_score":3.61},
    {"msa":"Columbus","short":"COL","macro_score":1.60,"asset_score":4.04},
    {"msa":"D.C. Metro","short":"WDC","macro_score":4.77,"asset_score":2.23},
    {"msa":"Dallas / Fort Worth","short":"DFW","macro_score":0.53,"asset_score":3.76},
    {"msa":"Denver","short":"DEN","macro_score":1.31,"asset_score":4.90},
    {"msa":"Detroit","short":"DET","macro_score":4.31,"asset_score":4.95},
    {"msa":"Fort Lauderdale","short":"FTL","macro_score":1.03,"asset_score":3.30},
    {"msa":"Houston","short":"HOU","macro_score":4.60,"asset_score":3.58},
    {"msa":"Indianapolis","short":"IND","macro_score":3.77,"asset_score":2.59},
    {"msa":"Inland Empire","short":"INE","macro_score":4.80,"asset_score":4.59},
    {"msa":"Jacksonville","short":"JAC","macro_score":4.32,"asset_score":0.67},
    {"msa":"Kansas City","short":"KC","macro_score":2.35,"asset_score":3.61},
    {"msa":"Las Vegas","short":"LV","macro_score":2.83,"asset_score":3.91},
    {"msa":"Los Angeles","short":"LA","macro_score":2.02,"asset_score":3.74},
    {"msa":"Louisville","short":"LOU","macro_score":2.71,"asset_score":3.31},
    {"msa":"Memphis","short":"MEM","macro_score":3.92,"asset_score":3.38},
    {"msa":"Miami","short":"MIA","macro_score":2.71,"asset_score":1.85},
    {"msa":"Minneapolis","short":"MIN","macro_score":1.34,"asset_score":0.02},
    {"msa":"Nashville","short":"NAS","macro_score":2.92,"asset_score":4.35},
    {"msa":"New Jersey (N)","short":"NJN","macro_score":3.63,"asset_score":3.55},
    {"msa":"New York","short":"NYC","macro_score":2.98,"asset_score":0.12},
    {"msa":"Orange County","short":"OC","macro_score":2.09,"asset_score":4.11},
    {"msa":"Orlando","short":"ORL","macro_score":0.47,"asset_score":1.84},
    {"msa":"Palm Beach","short":"PLB","macro_score":4.12,"asset_score":3.31},
    {"msa":"Philadelphia","short":"PHI","macro_score":0.29,"asset_score":2.15},
    {"msa":"Phoenix","short":"PHX","macro_score":4.50,"asset_score":0.26},
    {"msa":"Pittsburgh","short":"PIT","macro_score":1.92,"asset_score":2.84},
    {"msa":"Portland","short":"POR","macro_score":0.52,"asset_score":3.86},
    {"msa":"Richmond","short":"RIC","macro_score":0.62,"asset_score":4.14},
    {"msa":"Sacramento","short":"SAC","macro_score":2.96,"asset_score":3.16},
    {"msa":"Salt Lake City","short":"SLC","macro_score":1.47,"asset_score":1.79},
    {"msa":"San Antonio","short":"SA","macro_score":2.91,"asset_score":4.57},
    {"msa":"San Diego","short":"SD","macro_score":2.69,"asset_score":1.14},
    {"msa":"San Francisco","short":"SF","macro_score":2.54,"asset_score":1.71},
    {"msa":"Seattle","short":"SEA","macro_score":0.56,"asset_score":0.06},
    {"msa":"St. Louis","short":"SL","macro_score":1.36,"asset_score":3.01},
    {"msa":"Tampa","short":"TMP","macro_score":2.69,"asset_score":3.88},
]

def get_base_df(macro_mid=3.0, asset_mid=3.25):
    df = pd.DataFrame(BASE_DATA)
    df["tier"] = df.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)
    return df

# ── Simulated time-series (quarters) ─────────────────────────────────────────
def get_timeseries_df():
    quarters = ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026"]
    rows = []
    random.seed(42)
    for city in BASE_DATA:
        m = city["macro_score"]
        a = city["asset_score"]
        for i, q in enumerate(quarters):
            noise_m = random.uniform(-0.15, 0.15) * i
            noise_a = random.uniform(-0.2, 0.25) * i
            ms = round(max(0.1, min(4.99, m + noise_m)), 2)
            as_ = round(max(0.1, min(4.99, a + noise_a)), 2)
            rows.append({
                "msa": city["msa"],
                "short": city["short"],
                "quarter": q,
                "macro_score": ms,
                "asset_score": as_,
                "combined": round(ms + as_, 2),
            })
    return pd.DataFrame(rows)

# ── Charts ────────────────────────────────────────────────────────────────────
def make_scatter(df, macro_mid, asset_mid):
    fig = go.Figure()

    # Quadrant fills
    fig.add_shape(type="rect", x0=macro_mid, x1=5.3, y0=asset_mid, y1=5.5,
                  fillcolor="rgba(29,158,117,0.07)", line_width=0)
    fig.add_shape(type="rect", x0=0, x1=macro_mid, y0=asset_mid, y1=5.5,
                  fillcolor="rgba(55,138,221,0.06)", line_width=0)
    fig.add_shape(type="rect", x0=macro_mid, x1=5.3, y0=0, y1=asset_mid,
                  fillcolor="rgba(186,117,23,0.06)", line_width=0)
    fig.add_shape(type="rect", x0=0, x1=macro_mid, y0=0, y1=asset_mid,
                  fillcolor="rgba(136,135,128,0.04)", line_width=0)

    # Midlines
    for x0, x1, y0, y1 in [(macro_mid, macro_mid, 0, 5.5), (0, 5.3, asset_mid, asset_mid)]:
        fig.add_shape(type="line", x0=x0, x1=x1, y0=y0, y1=y1,
                      line=dict(color="rgba(13,79,69,0.25)", width=1, dash="dash"))

    # Quadrant labels
    for txt, x, y, anchor in [
        ("Alta Convicción", macro_mid + 0.08, 5.35, "left"),
        ("Asset Fuerte",    0.08,              5.35, "left"),
        ("Macro Fuerte",    macro_mid + 0.08,  0.12, "left"),
        ("Monitorear",      0.08,              0.12, "left"),
    ]:
        fig.add_annotation(text=txt, x=x, y=y, showarrow=False,
                           font=dict(size=10, color="rgba(13,79,69,0.45)"),
                           xanchor=anchor)

    for tier, grp in df.groupby("tier"):
        fig.add_trace(go.Scatter(
            x=grp["macro_score"], y=grp["asset_score"],
            mode="markers+text",
            name=tier,
            text=grp["short"],
            textposition="top center",
            textfont=dict(size=9, color="#333"),
            marker=dict(
                size=11,
                color=TIER_COLORS[tier],
                opacity=0.9,
                line=dict(width=1.5, color="white")
            ),
            customdata=grp[["msa", "macro_score", "asset_score", "tier"]].values,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Macro: %{customdata[1]:.2f}  |  Asset: %{customdata[2]:.2f}<br>"
                "Tier: %{customdata[3]}<extra></extra>"
            )
        ))

    fig.update_layout(
        xaxis=dict(title="Daki Macro Score", range=[0, 5.3],
                   showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False,
                   title_font=dict(size=12, color="#0D4F45")),
        yaxis=dict(title="Daki Asset Class Score", range=[0, 5.5],
                   showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False,
                   title_font=dict(size=12, color="#0D4F45")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.01,
                    xanchor="right", x=1, font=dict(size=11)),
        margin=dict(l=40, r=10, t=30, b=40),
        height=500,
        font=dict(family="Inter, sans-serif"),
        clickmode="event+select",
    )
    return fig

def make_heatmap(ts_df, metric="combined"):
    quarters = ts_df["quarter"].unique().tolist()
    cities = ts_df.groupby("msa")[metric].mean().sort_values(ascending=False).index.tolist()
    matrix = []
    for city in cities:
        row = []
        for q in quarters:
            val = ts_df[(ts_df["msa"] == city) & (ts_df["quarter"] == q)][metric]
            row.append(round(val.values[0], 2) if len(val) > 0 else None)
        matrix.append(row)

    short_names = []
    for c in cities:
        match = ts_df[ts_df["msa"] == c]["short"].values
        short_names.append(match[0] if len(match) > 0 else c[:6])

    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=quarters,
        y=short_names,
        colorscale=[[0, "#E1F5EE"], [0.4, "#5DCAA5"], [0.7, "#0F6E56"], [1, "#04342C"]],
        text=[[f"{v:.2f}" if v else "" for v in row] for row in matrix],
        texttemplate="%{text}",
        textfont=dict(size=9),
        hoverongaps=False,
        hovertemplate="<b>%{y}</b> — %{x}<br>Score: %{z:.2f}<extra></extra>",
        showscale=True,
        colorbar=dict(title=dict(text="Score", side="right"), thickness=12, len=0.8),
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=60, t=20, b=40),
        height=max(400, len(cities) * 18 + 80),
        xaxis=dict(side="top", tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=10), autorange="reversed"),
        font=dict(family="Inter, sans-serif"),
    )
    return fig

def make_trajectory(ts_df, selected_cities):
    fig = go.Figure()
    quarters = ts_df["quarter"].unique().tolist()
    palette = ["#1D9E75", "#378ADD", "#BA7517", "#D85A30", "#533AB7", "#0D4F45"]
    for i, city in enumerate(selected_cities):
        cdf = ts_df[ts_df["msa"] == city].sort_values("quarter")
        color = palette[i % len(palette)]
        fig.add_trace(go.Scatter(
            x=cdf["macro_score"], y=cdf["asset_score"],
            mode="lines+markers+text",
            name=city,
            line=dict(color=color, width=2),
            marker=dict(size=[8]*( len(cdf)-1) + [13], color=color,
                        symbol=["circle"]*(len(cdf)-1) + ["diamond"]),
            text=[""] * (len(cdf)-1) + [cdf["short"].values[0]],
            textposition="top right",
            textfont=dict(size=10),
            hovertemplate="<b>" + city + "</b><br>%{text}<br>Macro: %{x:.2f}  Asset: %{y:.2f}<extra></extra>",
            customdata=cdf["quarter"].values,
        ))

    # Quadrant lines
    fig.add_shape(type="line", x0=3, x1=3, y0=0, y1=5.5,
                  line=dict(color="rgba(13,79,69,0.2)", dash="dash", width=1))
    fig.add_shape(type="line", x0=0, x1=5.3, y0=3.25, y1=3.25,
                  line=dict(color="rgba(13,79,69,0.2)", dash="dash", width=1))

    fig.update_layout(
        xaxis=dict(title="Daki Macro Score", range=[0, 5.3], showgrid=True,
                   gridcolor="rgba(0,0,0,0.06)", zeroline=False),
        yaxis=dict(title="Daki Asset Class Score", range=[0, 5.5], showgrid=True,
                   gridcolor="rgba(0,0,0,0.06)", zeroline=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(size=11)),
        margin=dict(l=40, r=20, t=20, b=40),
        height=460,
        font=dict(family="Inter, sans-serif"),
    )
    return fig

# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="padding: 8px 0 20px; text-align: center;">
            <svg width="48" height="48" viewBox="0 0 100 100" fill="none">
                <path d="M50 10 L85 30 L85 70 L50 90 L15 70 L15 30 Z" fill="rgba(255,255,255,0.15)" stroke="white" stroke-width="2"/>
                <path d="M50 25 L72 38 L72 62 L50 75 L28 62 L28 38 Z" fill="rgba(255,255,255,0.2)" stroke="white" stroke-width="1.5"/>
                <path d="M50 40 L62 47 L62 57 L50 64 L38 57 L38 47 Z" fill="white"/>
            </svg>
            <div style="font-size:20px;font-weight:700;color:white;margin-top:8px;letter-spacing:0.05em;">DAKI CAPITAL</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.55);margin-top:3px;letter-spacing:0.08em;">MSA INTELLIGENCE</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**FUENTE DE DATOS**")
        data_mode = st.radio("", ["Datos de muestra", "Subir archivo", "Google Sheet"],
                             label_visibility="collapsed")

        uploaded = None
        sheet_url = None
        if data_mode == "Subir archivo":
            uploaded = st.file_uploader("CSV o Excel", type=["csv", "xlsx"])
        elif data_mode == "Google Sheet":
            sheet_url = st.text_input("URL del Google Sheet",
                                      placeholder="https://docs.google.com/spreadsheets/d/...")

        st.markdown("---")
        st.markdown("**FILTROS**")
        tiers = st.multiselect("Conviction tier",
            ["Alta Convicción", "Asset Fuerte", "Macro Fuerte", "Monitorear"],
            default=["Alta Convicción", "Asset Fuerte", "Macro Fuerte", "Monitorear"])

        macro_range = st.slider("Rango Macro Score", 0.0, 5.0, (0.0, 5.0), 0.1)
        asset_range = st.slider("Rango Asset Score", 0.0, 5.0, (0.0, 5.0), 0.1)

        st.markdown("---")
        st.markdown("**UMBRALES**")
        macro_mid = st.slider("Línea media Macro", 0.0, 5.0, 3.0, 0.05)
        asset_mid = st.slider("Línea media Asset", 0.0, 5.0, 3.25, 0.05)

    return uploaded, sheet_url, tiers, macro_range, asset_range, macro_mid, asset_mid

# ── Data loader ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def load_from_sheets(url):
    sheet_id = url.split("/d/")[1].split("/")[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(csv_url)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    uploaded, sheet_url, tiers, macro_range, asset_range, macro_mid, asset_mid = render_sidebar()

    # Header
    st.markdown("""
    <div class="daki-header">
        <svg width="42" height="42" viewBox="0 0 100 100" fill="none">
            <path d="M50 8 L88 30 L88 70 L50 92 L12 70 L12 30 Z" fill="rgba(255,255,255,0.15)" stroke="white" stroke-width="2"/>
            <path d="M50 24 L74 38 L74 62 L50 76 L26 62 L26 38 Z" fill="rgba(255,255,255,0.2)" stroke="white" stroke-width="1.5"/>
            <path d="M50 40 L63 48 L63 58 L50 66 L37 58 L37 48 Z" fill="white"/>
        </svg>
        <div>
            <div class="daki-logo-text">DAKI CAPITAL — MSA Dashboard</div>
            <div class="daki-logo-sub">Industrial · Small Bay · Framework de Selección de Mercados</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    df = get_base_df(macro_mid, asset_mid)

    if uploaded is not None:
        try:
            if uploaded.name.endswith(".csv"):
                raw = pd.read_csv(uploaded)
            else:
                raw = pd.read_excel(uploaded)
            raw.columns = [c.strip().lower().replace(" ", "_") for c in raw.columns]
            if "macro_score" in raw.columns and "asset_score" in raw.columns:
                raw["tier"] = raw.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)
                df = raw
                st.success(f"Archivo cargado: {len(df)} mercados")
        except Exception as e:
            st.error(f"Error al cargar archivo: {e}")

    elif sheet_url and "docs.google.com" in sheet_url:
        try:
            with st.spinner("Cargando Google Sheet..."):
                raw = load_from_sheets(sheet_url)
            if "macro_score" in raw.columns and "asset_score" in raw.columns:
                raw["tier"] = raw.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)
                df = raw
                st.success(f"Google Sheet conectado: {len(df)} mercados")
        except Exception as e:
            st.error(f"Error al conectar Sheet. Asegúrate de que sea público.\n{e}")

    # Recompute tiers with current midlines
    df["tier"] = df.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)

    # Apply filters
    filtered = df[
        df["tier"].isin(tiers) &
        df["macro_score"].between(*macro_range) &
        df["asset_score"].between(*asset_range)
    ].copy()

    # KPI cards
    alta  = len(filtered[filtered["tier"] == "Alta Convicción"])
    asset = len(filtered[filtered["tier"] == "Asset Fuerte"])
    macro = len(filtered[filtered["tier"] == "Macro Fuerte"])
    watch = len(filtered[filtered["tier"] == "Monitorear"])

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card"><div class="kpi-val">{len(filtered)}</div><div class="kpi-lbl">Total MSAs</div></div>
        <div class="kpi-card green"><div class="kpi-val">{alta}</div><div class="kpi-lbl">Alta Convicción</div></div>
        <div class="kpi-card blue"><div class="kpi-val">{asset}</div><div class="kpi-lbl">Asset Fuerte</div></div>
        <div class="kpi-card amber"><div class="kpi-val">{macro}</div><div class="kpi-lbl">Macro Fuerte</div></div>
        <div class="kpi-card gray"><div class="kpi-val">{watch}</div><div class="kpi-lbl">Monitorear</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Scatter Plot", "Heat Map", "Trayectorias", "Rankings", "Calculadora"])

    # ── Tab 1: Scatter ────────────────────────────────────────────────────────
    with tab1:
        col_chart, col_detail = st.columns([3, 1])
        with col_chart:
            st.markdown('<div class="section-title">Mapa de Convicción de Mercados</div>', unsafe_allow_html=True)
            fig = make_scatter(filtered, macro_mid, asset_mid)
            selected = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="scatter")

        with col_detail:
            st.markdown('<div class="section-title">Detalle de Ciudad</div>', unsafe_allow_html=True)
            sel_city = None
            if selected and selected.get("selection") and selected["selection"].get("points"):
                pt = selected["selection"]["points"][0]
                match = filtered[
                    (filtered["macro_score"].round(2) == round(pt["x"], 2)) &
                    (filtered["asset_score"].round(2) == round(pt["y"], 2))
                ]
                if not match.empty:
                    sel_city = match.iloc[0]["msa"]

            if sel_city:
                row = filtered[filtered["msa"] == sel_city].iloc[0]
                tc = TIER_COLORS[row["tier"]]
                tier_class = {"Alta Convicción":"tier-alta","Asset Fuerte":"tier-asset",
                              "Macro Fuerte":"tier-macro","Monitorear":"tier-monitor"}.get(row["tier"],"")
                st.markdown(f"### {row['msa']}")
                st.markdown(f'<span class="tier-badge {tier_class}">{row["tier"]}</span>', unsafe_allow_html=True)
                st.markdown("")
                c1, c2 = st.columns(2)
                c1.metric("Macro Score", f"{row['macro_score']:.2f}")
                c2.metric("Asset Score", f"{row['asset_score']:.2f}")
                combined = row["macro_score"] + row["asset_score"]
                st.markdown(f"**Score combinado: {combined:.2f} / 10**")
                st.progress(min(combined / 10, 1.0))
            else:
                st.info("Haz clic en cualquier punto del gráfico para ver el detalle.")
                st.markdown("**Referencia de cuadrantes:**")
                for tier, cls in [("Alta Convicción","tier-alta"),("Asset Fuerte","tier-asset"),
                                   ("Macro Fuerte","tier-macro"),("Monitorear","tier-monitor")]:
                    st.markdown(f'<span class="tier-badge {cls}">{tier}</span>', unsafe_allow_html=True)
                    st.markdown("")

    # ── Tab 2: Heat Map ───────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-title">Heat Map — Evolución por Trimestre</div>', unsafe_allow_html=True)
        st.caption("Muestra cómo ha cambiado el score de cada mercado a lo largo del tiempo. Colores más oscuros = score más alto.")

        ts_df = get_timeseries_df()
        # Filter to same cities as main filter
        ts_filtered = ts_df[ts_df["msa"].isin(filtered["msa"].tolist())]

        col_hm1, col_hm2 = st.columns(2)
        with col_hm1:
            st.markdown("**Daki Macro Score**")
            fig_hm1 = make_heatmap(ts_filtered, "macro_score")
            st.plotly_chart(fig_hm1, use_container_width=True)
        with col_hm2:
            st.markdown("**Daki Asset Class Score**")
            fig_hm2 = make_heatmap(ts_filtered, "asset_score")
            st.plotly_chart(fig_hm2, use_container_width=True)

        st.markdown("**Score Combinado (Macro + Asset)**")
        fig_hm3 = make_heatmap(ts_filtered, "combined")
        st.plotly_chart(fig_hm3, use_container_width=True)

    # ── Tab 3: Trajectories ───────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-title">Trayectorias de Mercados — Movimiento en el Scatter</div>', unsafe_allow_html=True)
        st.caption("Selecciona ciudades para ver cómo se han movido en el scatter a lo largo del tiempo. El diamante indica la posición más reciente.")

        all_cities = sorted([d["msa"] for d in BASE_DATA])
        default_cities = ["Houston", "Nashville", "Chicago", "Tampa", "Detroit"]
        selected_cities = st.multiselect("Selecciona mercados para comparar",
                                         all_cities, default=default_cities, max_selections=8)
        if selected_cities:
            ts_df = get_timeseries_df()
            fig_traj = make_trajectory(ts_df, selected_cities)
            st.plotly_chart(fig_traj, use_container_width=True)

            # Quarter-by-quarter table
            st.markdown('<div class="section-title">Scores por Trimestre</div>', unsafe_allow_html=True)
            ts_sel = ts_df[ts_df["msa"].isin(selected_cities)][["msa","quarter","macro_score","asset_score","combined"]]
            ts_pivot = ts_sel.pivot_table(index="msa", columns="quarter", values="combined").round(2)
            st.dataframe(ts_pivot, use_container_width=True)
        else:
            st.info("Selecciona al menos un mercado arriba.")

    # ── Tab 4: Rankings ───────────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-title">Rankings de MSAs — por score combinado</div>', unsafe_allow_html=True)

        ranked = filtered[["msa", "macro_score", "asset_score", "tier"]].copy()
        ranked["combined"] = (ranked["macro_score"] + ranked["asset_score"]).round(2)
        ranked = ranked.sort_values("combined", ascending=False).reset_index(drop=True)
        ranked.index += 1
        ranked.columns = ["MSA", "Macro Score", "Asset Score", "Tier", "Combined"]
        ranked["Macro Score"] = ranked["Macro Score"].round(2)
        ranked["Asset Score"] = ranked["Asset Score"].round(2)

        def color_tier(val):
            colors = {
                "Alta Convicción": "background-color: #E1F5EE; color: #0F6E56; font-weight: 600",
                "Asset Fuerte":    "background-color: #E6F1FB; color: #185FA5; font-weight: 600",
                "Macro Fuerte":    "background-color: #FAEEDA; color: #854F0B; font-weight: 600",
                "Monitorear":      "background-color: #F1EFE8; color: #5F5E5A; font-weight: 600",
            }
            return colors.get(val, "")

        # Use map instead of applymap (newer pandas compatibility)
        styled = ranked.style.map(color_tier, subset=["Tier"])
        st.dataframe(styled, use_container_width=True, height=580)

        csv = ranked.to_csv(index=True).encode("utf-8")
        st.download_button("Descargar rankings CSV", csv, "daki_rankings.csv", "text/csv")

    # ── Tab 5: Calculator ─────────────────────────────────────────────────────
    with tab5:
        st.markdown('<div class="section-title">Calculadora de Score — Ingreso Manual</div>', unsafe_allow_html=True)
        st.caption("Ingresa los datos brutos de un MSA para calcular su Daki Score al instante.")

        col_m, col_a = st.columns(2)
        with col_m:
            st.markdown("**Variables Macro**")
            macro_inputs = {}
            for v in MACRO_VARS:
                macro_inputs[v["key"]] = st.number_input(
                    f"{v['name']} — peso {v['weight']:.0%}",
                    min_value=float(v["min"]), max_value=float(v["max"]),
                    value=float((v["min"] + v["max"]) / 2), key=f"m_{v['key']}")
        with col_a:
            st.markdown("**Variables Asset Class**")
            asset_inputs = {}
            for v in ASSET_VARS:
                asset_inputs[v["key"]] = st.number_input(
                    f"{v['name']} — peso {v['weight']:.0%}",
                    min_value=float(v["min"]), max_value=float(v["max"]),
                    value=float((v["min"] + v["max"]) / 2), key=f"a_{v['key']}")

        if st.button("Calcular Score", type="primary"):
            ms  = compute_score(pd.Series(macro_inputs), MACRO_VARS)
            as_ = compute_score(pd.Series(asset_inputs), ASSET_VARS)
            tier = assign_tier(ms, as_, macro_mid, asset_mid)
            tc = TIER_COLORS[tier]
            tier_class = {"Alta Convicción":"tier-alta","Asset Fuerte":"tier-asset",
                          "Macro Fuerte":"tier-macro","Monitorear":"tier-monitor"}.get(tier,"")
            r1, r2, r3 = st.columns(3)
            r1.metric("Macro Score", f"{ms:.2f} / 5.00")
            r2.metric("Asset Score", f"{as_:.2f} / 5.00")
            r3.metric("Score Combinado", f"{ms+as_:.2f} / 10.00")
            st.markdown(f"""
            <div style="padding:14px;border-left:4px solid {tc};background:{tc}15;
                        border-radius:6px;margin-top:12px">
                <span class="tier-badge {tier_class}">{tier}</span>
                <span style="margin-left:12px;color:#444;font-size:14px">
                Score combinado: <strong>{ms+as_:.2f} / 10</strong></span>
            </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
