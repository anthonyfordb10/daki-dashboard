import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import random
import base64
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Daki Capital — MSA Dashboard",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Logo loader ───────────────────────────────────────────────────────────────
def get_logo_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_b64("logo_blanco.png")
logo_img         = f'<img src="data:image/png;base64,{logo_b64}" style="height:72px;object-fit:contain;" />' if logo_b64 else '<span style="font-size:22px;font-weight:700;color:white;letter-spacing:0.05em;">DAKI CAPITAL</span>'
logo_img_sidebar = f'<img src="data:image/png;base64,{logo_b64}" style="height:58px;object-fit:contain;max-width:200px;" />' if logo_b64 else '<span style="font-size:18px;font-weight:700;color:white;">DAKI CAPITAL</span>'

# ── Brand CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

/* Dark background */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background-color: #0F1E1B !important;
}}
[data-testid="stMainBlockContainer"], .block-container {{
    background-color: #0F1E1B !important;
}}

/* Text colors for dark bg */
p, span, label, div, h1, h2, h3, h4 {{
    color: #E0EBE8;
}}
.section-title {{
    color: #A8D5CC !important;
}}

[data-testid="stSidebar"] {{ background-color: #0D4F45; }}
[data-testid="stSidebar"] * {{ color: #ffffff !important; }}
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stMultiSelect label {{
    color: #a8d5cc !important; font-size: 11px;
    text-transform: uppercase; letter-spacing: 0.06em;
}}
[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.15) !important; }}

.daki-header {{
    background: linear-gradient(135deg, #0D4F45 0%, #1A7A6B 100%);
    padding: 16px 24px; border-radius: 8px; margin-bottom: 18px;
    display: flex; align-items: center; gap: 14px;
}}
.daki-header-sub {{ font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 3px; letter-spacing: 0.04em; }}

.kpi-row {{ display: flex; gap: 10px; margin-bottom: 18px; }}
.kpi-card {{
    flex: 1; background: #1A2E2A; border: 1px solid #2A4A44;
    border-radius: 8px; padding: 12px 16px; border-top: 3px solid #0D4F45;
}}
.kpi-val {{ font-size: 24px; font-weight: 700; color: #A8D5CC; }}
.kpi-lbl {{ font-size: 11px; color: #6b9e95; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.05em; }}
.kpi-card.green {{ border-top-color: #1D9E75; }} .kpi-card.blue {{ border-top-color: #378ADD; }}
.kpi-card.amber {{ border-top-color: #BA7517; }} .kpi-card.gray  {{ border-top-color: #888780; }}

.tier-badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
.tier-alta    {{ background: #E1F5EE; color: #0F6E56; }}
.tier-asset   {{ background: #E6F1FB; color: #185FA5; }}
.tier-macro   {{ background: #FAEEDA; color: #854F0B; }}
.tier-monitor {{ background: #F1EFE8; color: #5F5E5A; }}

.stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 2px solid #2A4A44; }}
.stTabs [data-baseweb="tab"] {{ padding: 8px 18px; font-size: 13px; font-weight: 500; color: #6b9e95; border-radius: 6px 6px 0 0; }}
.stTabs [aria-selected="true"] {{ background: #0D4F45 !important; color: #ffffff !important; }}

.section-title {{
    font-size: 14px; font-weight: 600; color: #A8D5CC;
    border-left: 3px solid #1D9E75; padding-left: 10px; margin-bottom: 12px;
}}
[data-testid="metric-container"] {{
    background: #1A2E2A; border: 1px solid #2A4A44; border-radius: 8px; padding: 10px 14px;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1rem; }}

/* Selectbox selected value text — black */
div[data-baseweb="select"] div[data-testid="stMarkdownContainer"],
div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
div[data-baseweb="select"] p,
[data-testid="stSelectbox"] div[data-baseweb="select"] span,
[data-testid="stSelectbox"] div[data-baseweb="select"] div {{
    color: #111111 !important;
}}
/* Multiselect and selectbox dropdown options — black text */
div[data-baseweb="popover"] li,
div[data-baseweb="menu"] li,
div[data-baseweb="select"] li,
[data-baseweb="menu"] [role="option"],
div[data-baseweb="popover"] span,
.stMultiSelect div[role="option"],
div[data-testid="stMultiSelect"] div[role="listbox"] span,
div[data-baseweb="select"] div[role="option"] span,
div[data-baseweb="menu"] ul li span,
div[data-baseweb="menu"] ul li div,
[data-baseweb="menu"] span,
[data-baseweb="menu"] div,
[data-baseweb="popover"] ul li,
[data-baseweb="popover"] ul li span,
[data-baseweb="popover"] ul li div {{
    color: #111111 !important;
}}
/* Selected tags in multiselect */
div[data-baseweb="tag"] span {{
    color: #ffffff !important;
}}
div[data-testid="stButton"] button {{
    background: #1D9E75 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    padding: 8px 14px !important;
    transition: background 0.2s;
}}
div[data-testid="stButton"] button:hover {{
    background: #178a64 !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
TIER_COLORS = {
    "High Conviction": "#1D9E75",
    "Strong Asset":    "#378ADD",
    "Strong Macro":    "#BA7517",
    "Monitor":         "#888780",
}
TIER_CLASS = {
    "High Conviction": "tier-alta",
    "Strong Asset":    "tier-asset",
    "Strong Macro":    "tier-macro",
    "Monitor":         "tier-monitor",
}

MACRO_VARS = [
    {"key": "pop_growth",      "name": "Population Growth",         "weight": 0.20},
    {"key": "employment",      "name": "Employment Rate",           "weight": 0.10},
    {"key": "education",       "name": "Years of Schooling",        "weight": 0.03},
    {"key": "avg_salary",      "name": "Average Salary",            "weight": 0.05},
    {"key": "gdp_per_capita",  "name": "GDP Per Capita",            "weight": 0.20},
    {"key": "households",      "name": "Number of Households",      "weight": 0.02},
    {"key": "household_spend", "name": "Avg Household Spend",       "weight": 0.20},
    {"key": "pct_renters",     "name": "% Renter-Occupied",         "weight": 0.10},
    {"key": "ecommerce_index", "name": "E-Commerce Index",          "weight": 0.10},
]
ASSET_VARS = [
    {"key": "rent_growth", "name": "Rent Growth",              "weight": 0.1667},
    {"key": "occupancy",   "name": "Average Occupancy",        "weight": 0.3333},
    {"key": "pipeline",    "name": "Pipeline / Inventory",     "weight": 0.1667},
    {"key": "cap_rate",    "name": "Cap Rates",                "weight": 0.0833},
    {"key": "rent_psf",    "name": "Asking Rent PSF",          "weight": 0.0833},
    {"key": "sale_psf",    "name": "Sale Price PSF",           "weight": 0.1667},
]

def assign_tier(macro, asset, macro_mid=2.25, asset_mid=2.56):
    if macro >= macro_mid and asset >= asset_mid:   return "High Conviction"
    elif macro < macro_mid and asset >= asset_mid:  return "Strong Asset"
    elif macro >= macro_mid and asset < asset_mid:  return "Strong Macro"
    else:                                            return "Monitor"

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

QUARTERS = ["Q1 2021","Q2 2021","Q3 2021","Q4 2021",
            "Q1 2022","Q2 2022","Q3 2022","Q4 2022",
            "Q1 2023","Q2 2023","Q3 2023","Q4 2023",
            "Q1 2024","Q2 2024","Q3 2024","Q4 2024",
            "Q1 2025","Q2 2025","Q3 2025","Q4 2025",
            "Q1 2026"]

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1VV_IfUe3QCuDvF3uaR8IohbbL3i-Hy-ZjqsK-yVXPkw/edit?usp=sharing"

@st.cache_data(ttl=3600)
def load_google_sheet(url):
    """Load data from public Google Sheet. Refreshes every hour."""
    sheet_id = url.split("/d/")[1].split("/")[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(csv_url)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def get_base_df(macro_mid=2.25, asset_mid=2.56):
    # 1. Try live Google Sheet (primary source)
    try:
        df = load_google_sheet(GOOGLE_SHEET_URL)
        if "macro_score" in df.columns and "asset_score" in df.columns:
            df = df[df["msa"].notna()].copy()
            df["tier"] = df.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)
            return df
    except Exception:
        pass
    # 2. Fall back to local CSV
    try:
        df = pd.read_csv("greenstreet_data.csv")
        df = df[df["msa"].notna()].copy()
        df["tier"] = df.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)
        return df
    except Exception:
        pass
    # 3. Last resort: sample data
    df = pd.DataFrame(BASE_DATA)
    df["tier"] = df.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)
    return df

def get_timeseries_df():
    """Generate consistent simulated quarterly history based on real Green Street scores."""
    base_df = get_base_df()
    rows = []
    for _, city in base_df.iterrows():
        m, a = city["macro_score"], city["asset_score"]
        rng = random.Random(hash(city["msa"]))  # consistent seed per city
        for i, q in enumerate(QUARTERS):
            # Gentle drift — earlier quarters slightly different from current
            drift = (i - len(QUARTERS) + 1) * 0.02  # negative = earlier
            noise_m = rng.uniform(-0.08, 0.08) + drift * rng.uniform(0.5, 1.5)
            noise_a = rng.uniform(-0.10, 0.10) + drift * rng.uniform(0.5, 1.5)
            ms  = round(max(0.1, min(4.99, m + noise_m)), 2)
            as_ = round(max(0.1, min(4.99, a + noise_a)), 2)
            rows.append({"msa": city["msa"], "short": city["short"],
                         "quarter": q, "quarter_idx": i,
                         "macro_score": ms, "asset_score": as_,
                         "combined": round((ms + as_) / 2, 2)})
    return pd.DataFrame(rows)

def filter_quarters_by_period(ts_df, time_filter):
    """Filter timeseries dataframe by selected time period."""
    if time_filter == "All (5 years)":
        return ts_df
    else:
        filtered = ts_df[ts_df["quarter"].str.contains(time_filter)].copy()
        return filtered if not filtered.empty else ts_df
def make_scatter(df, macro_mid, asset_mid):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=macro_mid, x1=5.3, y0=asset_mid, y1=5.5, fillcolor="rgba(29,158,117,0.07)", line_width=0)
    fig.add_shape(type="rect", x0=0, x1=macro_mid, y0=asset_mid, y1=5.5, fillcolor="rgba(55,138,221,0.06)", line_width=0)
    fig.add_shape(type="rect", x0=macro_mid, x1=5.3, y0=0, y1=asset_mid, fillcolor="rgba(186,117,23,0.06)", line_width=0)
    for x0,x1,y0,y1 in [(macro_mid,macro_mid,0,5.5),(0,5.3,asset_mid,asset_mid)]:
        fig.add_shape(type="line",x0=x0,x1=x1,y0=y0,y1=y1,line=dict(color="rgba(168,213,204,0.2)",width=1,dash="dash"))
    for txt,x,y in [("High Conviction ↗",macro_mid+0.08,5.35),("Strong Asset",0.08,5.35),
                    ("Strong Macro",macro_mid+0.08,0.15),("Monitor",0.08,0.15)]:
        fig.add_annotation(text=txt,x=x,y=y,showarrow=False,font=dict(size=10,color="rgba(168,213,204,0.5)"),xanchor="left")
    for tier, grp in df.groupby("tier"):
        fig.add_trace(go.Scatter(
            x=grp["macro_score"], y=grp["asset_score"],
            mode="markers+text", name=tier,
            text=grp["short"], textposition="top center", textfont=dict(size=9, color="white"),
            marker=dict(size=11, color=TIER_COLORS[tier], opacity=0.9, line=dict(width=1.5, color="white")),
            customdata=grp[["msa","macro_score","asset_score","tier"]].values,
            hovertemplate="<b>%{customdata[0]}</b><br>Macro: %{customdata[1]:.2f}  |  Asset: %{customdata[2]:.2f}<br>Tier: %{customdata[3]}<extra></extra>"
        ))
    fig.update_layout(
        xaxis=dict(title="Daki Macro Score", range=[0,5.3], showgrid=True, gridcolor="rgba(255,255,255,0.07)", zeroline=False, title_font=dict(size=12,color="#A8D5CC")),
        yaxis=dict(title="Daki Asset Class Score", range=[0,5.5], showgrid=True, gridcolor="rgba(255,255,255,0.07)", zeroline=False, title_font=dict(size=12,color="#A8D5CC")),
        plot_bgcolor="#0F1E1B", paper_bgcolor="#0F1E1B",
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1, font=dict(size=11, color="white")),
        margin=dict(l=40,r=10,t=30,b=40), height=500,
        font=dict(family="Inter, sans-serif"), clickmode="event+select",
    )
    return fig

def make_blackrock_heatmap(ts_df, metric, top_n=20):
    """
    BlackRock-style ranked heat map.
    Columns = quarters. Each column shows the top_n cities ranked best→worst.
    Cells are large enough to read clearly.
    """
    # Sort quarters chronologically using QUARTERS order
    quarters = [q for q in QUARTERS if q in ts_df["quarter"].unique()]

    # For each quarter, rank cities by metric descending, keep top_n
    col_data = {}
    for q in quarters:
        qdf = ts_df[ts_df["quarter"] == q][["msa", "short", metric]].copy()
        qdf = qdf.sort_values(metric, ascending=False).head(top_n).reset_index(drop=True)
        col_data[q] = qdf

    # Build matrix rows = rank 1..top_n, cols = quarters
    z, text, hover = [], [], []
    for rank in range(top_n):
        z_row, t_row, h_row = [], [], []
        for q in quarters:
            qdf = col_data[q]
            if rank < len(qdf):
                val = round(qdf.iloc[rank][metric], 2)
                short = qdf.iloc[rank]["short"]
                msa   = qdf.iloc[rank]["msa"]
                z_row.append(val)
                t_row.append(f"<b>{short}</b><br>{val:.2f}")
                h_row.append(f"<b>{msa}</b><br>{q} — Rank #{rank+1}<br>Score: {val:.2f}")
            else:
                z_row.append(None)
                t_row.append("")
                h_row.append("")
        z.append(z_row)
        text.append(t_row)
        hover.append(h_row)

    cell_h = 48  # px per row — tall enough to read
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=[f"<b>{q}</b>" for q in quarters],
        y=[f"#{i+1}" for i in range(top_n)],
        colorscale=[
            [0.0,  "#C8EDE4"],
            [0.3,  "#5DCAA5"],
            [0.6,  "#0F6E56"],
            [1.0,  "#04342C"],
        ],
        text=text,
        texttemplate="%{text}",
        textfont=dict(size=11, color="white"),
        customdata=hover,
        hovertemplate="%{customdata}<extra></extra>",
        showscale=True,
        colorbar=dict(
            thickness=14, len=0.85,
            title=dict(text="Score", side="right"),
            tickfont=dict(size=11),
        ),
        zmin=0, zmax=5,
        xgap=3, ygap=3,
    ))
    fig.update_layout(
        plot_bgcolor="#0F1E1B",
        paper_bgcolor="#0F1E1B",
        margin=dict(l=50, r=80, t=40, b=20),
        height=top_n * cell_h + 80,
        xaxis=dict(
            side="top",
            tickfont=dict(size=13, color="#0D4F45"),
            showgrid=False, zeroline=False,
        ),
        yaxis=dict(
            tickfont=dict(size=12, color="#A8D5CC"),
            autorange="reversed",
            showgrid=False, zeroline=False,
        ),
        font=dict(family="Inter, sans-serif"),
    )
    return fig

def make_trajectory(ts_df, selected_cities):
    fig = go.Figure()
    palette = ["#1D9E75","#378ADD","#BA7517","#D85A30","#533AB7","#0D4F45","#C0392B","#8E44AD"]
    for i, city in enumerate(selected_cities):
        cdf = ts_df[ts_df["msa"] == city].sort_values("quarter")
        color = palette[i % len(palette)]
        fig.add_trace(go.Scatter(
            x=cdf["macro_score"], y=cdf["asset_score"],
            mode="lines+markers+text", name=city,
            line=dict(color=color, width=2),
            marker=dict(size=[8]*(len(cdf)-1)+[13], color=color, symbol=["circle"]*(len(cdf)-1)+["diamond"]),
            text=[""] * (len(cdf)-1) + [cdf["short"].values[0]],
            textposition="top right", textfont=dict(size=10),
            customdata=cdf["quarter"].values,
            hovertemplate="<b>" + city + "</b><br>%{customdata}<br>Macro: %{x:.2f}  |  Asset: %{y:.2f}<extra></extra>",
        ))
    fig.add_shape(type="line",x0=3,x1=3,y0=0,y1=5.5,line=dict(color="rgba(168,213,204,0.2)",dash="dash",width=1))
    fig.add_shape(type="line",x0=0,x1=5.3,y0=3.25,y1=3.25,line=dict(color="rgba(168,213,204,0.2)",dash="dash",width=1))
    fig.update_layout(
        xaxis=dict(title="Daki Macro Score", range=[0,5.3], showgrid=True, gridcolor="rgba(255,255,255,0.07)", zeroline=False),
        yaxis=dict(title="Daki Asset Class Score", range=[0,5.5], showgrid=True, gridcolor="rgba(255,255,255,0.07)", zeroline=False),
        plot_bgcolor="#0F1E1B", paper_bgcolor="#0F1E1B",
        legend=dict(font=dict(size=11, color="white")),
        margin=dict(l=40,r=20,t=20,b=40), height=460,
        font=dict(family="Inter, sans-serif"),
    )
    return fig

# ── MSA → state mapping for choropleth ───────────────────────────────────────
MSA_STATE = {
    "Atlanta": "GA", "Austin": "TX", "Baltimore": "MD", "Boston": "MA",
    "Charlotte": "NC", "Chicago": "IL", "Cincinnati": "OH", "Cleveland": "OH",
    "Columbus": "OH", "D.C. Metro": "VA", "Dallas / Fort Worth": "TX",
    "Denver": "CO", "Detroit": "MI", "Fort Lauderdale": "FL", "Houston": "TX",
    "Indianapolis": "IN", "Inland Empire": "CA", "Jacksonville": "FL",
    "Kansas City": "MO", "Las Vegas": "NV", "Los Angeles": "CA",
    "Louisville": "KY", "Memphis": "TN", "Miami": "FL", "Minneapolis": "MN",
    "Nashville": "TN", "New Jersey (N)": "NJ", "New York": "NY",
    "Orange County": "CA", "Orlando": "FL", "Palm Beach": "FL",
    "Philadelphia": "PA", "Phoenix": "AZ", "Pittsburgh": "PA",
    "Portland": "OR", "Richmond": "VA", "Sacramento": "CA",
    "Salt Lake City": "UT", "San Antonio": "TX", "San Diego": "CA",
    "San Francisco": "CA", "Seattle": "WA", "St. Louis": "MO", "Tampa": "FL",
}

# Lat/lon for each MSA bubble
MSA_COORDS = {
    "Atlanta": (33.749, -84.388), "Austin": (30.267, -97.743),
    "Baltimore": (39.290, -76.612), "Boston": (42.360, -71.059),
    "Charlotte": (35.227, -80.843), "Chicago": (41.878, -87.630),
    "Cincinnati": (39.103, -84.512), "Cleveland": (41.499, -81.695),
    "Columbus": (39.961, -82.999), "D.C. Metro": (38.907, -77.037),
    "Dallas / Fort Worth": (32.776, -96.797), "Denver": (39.739, -104.984),
    "Detroit": (42.331, -83.046), "Fort Lauderdale": (26.122, -80.143),
    "Houston": (29.760, -95.370), "Indianapolis": (39.768, -86.158),
    "Inland Empire": (34.055, -117.182), "Jacksonville": (30.332, -81.656),
    "Kansas City": (39.099, -94.578), "Las Vegas": (36.175, -115.137),
    "Los Angeles": (34.052, -118.244), "Louisville": (38.252, -85.758),
    "Memphis": (35.149, -90.049), "Miami": (25.775, -80.208),
    "Minneapolis": (44.977, -93.265), "Nashville": (36.162, -86.781),
    "New Jersey (N)": (40.714, -74.006), "New York": (40.713, -74.006),
    "Orange County": (33.684, -117.794), "Orlando": (28.538, -81.379),
    "Palm Beach": (26.715, -80.053), "Philadelphia": (39.952, -75.164),
    "Phoenix": (33.448, -112.074), "Pittsburgh": (40.440, -79.996),
    "Portland": (45.523, -122.676), "Richmond": (37.541, -77.434),
    "Sacramento": (38.582, -121.494), "Salt Lake City": (40.760, -111.891),
    "San Antonio": (29.425, -98.494), "San Diego": (32.715, -117.157),
    "San Francisco": (37.774, -122.419), "Seattle": (47.606, -122.332),
    "St. Louis": (38.627, -90.198), "Tampa": (27.950, -82.457),
}

def make_us_map(df, metric="combined", zoom_state=None):
    # Compute value per city
    df = df.copy()
    df["_val"] = df.apply(
        lambda r: (r["macro_score"] + r["asset_score"]) / 2 if metric == "combined" else r[metric], axis=1)

    # Aggregate to state level (average of all MSAs in that state)
    state_scores = {}
    state_msas   = {}
    for _, row in df.iterrows():
        state = MSA_STATE.get(row["msa"])
        if not state:
            continue
        state_scores.setdefault(state, []).append(row["_val"])
        state_msas.setdefault(state, []).append(row["msa"])

    states      = list(state_scores.keys())
    avg_scores  = [round(sum(v)/len(v), 2) for v in state_scores.values()]
    hover_texts = []
    for s in states:
        msas = state_msas[s]
        lines = [f"<b>{s}</b> — avg {round(sum(state_scores[s])/len(state_scores[s]),2):.2f}"]
        for msa in msas:
            r = df[df["msa"]==msa].iloc[0]
            lines.append(f"  · {msa}: {r['_val']:.2f}")
        hover_texts.append("<br>".join(lines))

    # State center coordinates for zoom
    STATE_CENTERS = {
        "AL":(32.8,-86.8),"AZ":(34.3,-111.1),"AR":(34.8,-92.2),"CA":(37.2,-119.5),
        "CO":(39.0,-105.5),"CT":(41.6,-72.7),"DE":(39.0,-75.5),"FL":(28.0,-81.5),
        "GA":(33.0,-83.6),"HI":(20.8,-156.3),"ID":(44.4,-114.6),"IL":(40.0,-89.2),
        "IN":(40.3,-86.1),"IA":(42.0,-93.5),"KS":(38.5,-98.4),"KY":(37.5,-85.3),
        "LA":(31.2,-91.8),"ME":(44.7,-69.4),"MD":(39.0,-76.8),"MA":(42.3,-71.8),
        "MI":(44.3,-85.4),"MN":(46.4,-93.1),"MS":(32.7,-89.7),"MO":(38.5,-92.5),
        "MT":(47.0,-110.0),"NE":(41.5,-99.9),"NV":(39.3,-116.6),"NH":(43.7,-71.6),
        "NJ":(40.1,-74.5),"NM":(34.8,-106.2),"NY":(42.9,-75.5),"NC":(35.5,-79.8),
        "ND":(47.5,-100.5),"OH":(40.4,-82.8),"OK":(35.6,-96.9),"OR":(44.6,-120.5),
        "PA":(40.6,-77.2),"RI":(41.7,-71.5),"SC":(33.8,-81.2),"SD":(44.4,-100.2),
        "TN":(35.9,-86.7),"TX":(31.5,-99.3),"UT":(39.3,-111.1),"VT":(44.0,-72.7),
        "VA":(37.8,-79.5),"WA":(47.4,-120.5),"WV":(38.6,-80.6),"WI":(44.3,-89.8),
        "WY":(43.0,-107.6),
    }

    fig = go.Figure()

    # ── Layer 1: state choropleth ─────────────────────────────────────────────
    fig.add_trace(go.Choropleth(
        locations=states,
        z=avg_scores,
        locationmode="USA-states",
        colorscale=[
            [0.0, "#0D2B24"],
            [0.3, "#0D4F45"],
            [0.6, "#1D9E75"],
            [1.0, "#A8EDD4"],
        ],
        zmin=0, zmax=5,
        marker_line_color="#2A4A44",
        marker_line_width=0.8,
        hovertext=hover_texts,
        hoverinfo="text",
        showscale=True,
        colorbar=dict(
            title=dict(text="Avg Score", font=dict(color="white", size=11)),
            thickness=14, len=0.7,
            tickfont=dict(color="white", size=10),
            bgcolor="rgba(15,30,27,0.7)",
            bordercolor="#2A4A44",
            borderwidth=1,
            x=1.01,
        ),
        name="State avg score",
    ))

    # ── Layer 2: city bubbles ─────────────────────────────────────────────────
    # If zoomed into a state, only show MSAs in that state
    if zoom_state:
        visible_msas = {msa for msa, st in MSA_STATE.items() if st == zoom_state}
        plot_df = df[df["msa"].isin(visible_msas)]
    else:
        plot_df = df

    for tier, color in TIER_COLORS.items():
        tier_df = plot_df[plot_df["tier"] == tier]
        t_lats, t_lons, t_texts, t_sizes, t_hovers = [], [], [], [], []
        for _, row in tier_df.iterrows():
            msa = row["msa"]
            if msa not in MSA_COORDS:
                continue
            lat, lon = MSA_COORDS[msa]
            val = row["_val"]
            t_lats.append(lat)
            t_lons.append(lon)
            t_texts.append(row["short"])
            t_sizes.append(8 + val * 4) if not zoom_state else t_sizes.append(14 + val * 5)
            t_hovers.append(
                f"<b>{msa}</b><br>"
                f"Macro: {row['macro_score']:.2f}  |  Asset: {row['asset_score']:.2f}<br>"
                f"Score: {val:.2f}  |  {tier}"
            )
        if t_lats:
            fig.add_trace(go.Scattergeo(
                lat=t_lats, lon=t_lons,
                mode="markers+text",
                name=tier,
                text=t_texts,
                textposition="top center",
                textfont=dict(size=9 if not zoom_state else 12, color="white"),
                marker=dict(
                    size=t_sizes,
                    color=color,
                    opacity=0.92,
                    line=dict(width=1.5, color="white"),
                ),
                hovertext=t_hovers,
                hoverinfo="text",
            ))

    # ── Geo layout — zoom if state selected ──────────────────────────────────
    if zoom_state and zoom_state in STATE_CENTERS:
        clat, clon = STATE_CENTERS[zoom_state]
        geo_settings = dict(
            scope="usa",
            projection_type="albers usa",
            showland=True,  landcolor="#1A2E2A",
            showlakes=True, lakecolor="#0D1F1C",
            showcoastlines=True, coastlinecolor="#2A4A44", coastlinewidth=0.5,
            showsubunits=True, subunitcolor="#1D9E75", subunitwidth=1.5,
            showframe=False,
            bgcolor="#0F1E1B",
            center=dict(lat=clat, lon=clon),
            lonaxis_range=[clon - 6, clon + 6],
            lataxis_range=[clat - 4, clat + 4],
        )
        map_height = 480
    else:
        geo_settings = dict(
            scope="usa",
            projection_type="albers usa",
            showland=True,  landcolor="#1A2E2A",
            showlakes=True, lakecolor="#0D1F1C",
            showcoastlines=True, coastlinecolor="#2A4A44", coastlinewidth=0.5,
            showsubunits=True, subunitcolor="#2A4A44", subunitwidth=0.5,
            showframe=False,
            bgcolor="#0F1E1B",
        )
        map_height = 520

    fig.update_layout(
        geo=geo_settings,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.01,
            xanchor="right", x=0.92,
            font=dict(size=11, color="white"),
            bgcolor="rgba(15,30,27,0.6)",
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=map_height,
        paper_bgcolor="#0F1E1B",
        font=dict(family="Inter, sans-serif"),
    )
    return fig


def make_executive_summary(df, quarter, logo_b64=None):
    """Generate a self-contained HTML executive summary page."""
    from datetime import date

    ranked = df[["msa","macro_score","asset_score","tier"]].copy()
    ranked["combined"] = ((ranked["macro_score"] + ranked["asset_score"]) / 2).round(2)
    ranked = ranked.sort_values("combined", ascending=False).reset_index(drop=True)

    alta  = df[df["tier"]=="High Conviction"].sort_values("combined" if "combined" in df.columns else "macro_score", ascending=False)
    top5  = ranked.head(5)

    tier_counts = df["tier"].value_counts().to_dict()

    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:40px;" />' if logo_b64 else "<strong>DAKI CAPITAL</strong>"

    rows_html = ""
    for i, r in top5.iterrows():
        cls = {"High Conviction":"#1D9E75","Strong Asset":"#378ADD",
               "Strong Macro":"#BA7517","Monitor":"#888780"}.get(r["Tier"] if "Tier" in r else r["tier"], "#888")
        msa = r["MSA"] if "MSA" in r else r["msa"]
        rows_html += f"""
        <tr>
          <td style="padding:8px 12px;font-weight:600;color:#0D4F45">{i+1}. {msa}</td>
          <td style="padding:8px 12px;text-align:center">{r['macro_score']:.2f}</td>
          <td style="padding:8px 12px;text-align:center">{r['asset_score']:.2f}</td>
          <td style="padding:8px 12px;text-align:center;font-weight:700;color:#0D4F45">{r['combined']:.2f}</td>
          <td style="padding:8px 12px;text-align:center">
            <span style="background:{cls}22;color:{cls};padding:3px 10px;border-radius:10px;font-size:12px;font-weight:600">{r['tier'] if 'tier' in r else r['Tier']}</span>
          </td>
        </tr>"""

    # Tier summary pills
    pills = ""
    for tier, color in TIER_COLORS.items():
        count = tier_counts.get(tier, 0)
        pills += f'<div style="background:{color}18;border:1px solid {color}44;border-radius:8px;padding:12px 20px;text-align:center;min-width:110px"><div style="font-size:24px;font-weight:700;color:{color}">{count}</div><div style="font-size:11px;color:#555;margin-top:2px;text-transform:uppercase;letter-spacing:0.05em">{tier}</div></div>'

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: 'Inter', Arial, sans-serif; margin: 0; padding: 0; background: #fff; color: #222; }}
  .header {{ background: linear-gradient(135deg, #0D4F45, #1A7A6B); padding: 24px 40px; display: flex; align-items: center; justify-content: space-between; }}
  .header-right {{ text-align: right; color: rgba(255,255,255,0.7); font-size: 13px; }}
  .body {{ padding: 32px 40px; }}
  .section {{ margin-bottom: 32px; }}
  .section-title {{ font-size: 13px; font-weight: 600; color: #0D4F45; border-left: 3px solid #1D9E75; padding-left: 10px; margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.05em; }}
  .pills {{ display: flex; gap: 12px; flex-wrap: wrap; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  thead tr {{ background: #0D4F45; color: white; }}
  thead th {{ padding: 10px 12px; text-align: left; font-weight: 500; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; }}
  tbody tr:nth-child(even) {{ background: #F7FAF9; }}
  tbody tr {{ border-bottom: 1px solid #E8EDE9; }}
  .footer {{ background: #F7FAF9; border-top: 1px solid #E0E8E5; padding: 16px 40px; font-size: 11px; color: #888; display: flex; justify-content: space-between; margin-top: 40px; }}
  .disclaimer {{ font-size: 10px; color: #aaa; margin-top: 6px; }}
</style>
</head>
<body>
<div class="header">
  <div>{logo_html}</div>
  <div class="header-right">
    <div style="font-size:16px;font-weight:600;color:white">MSA Intelligence Report</div>
    <div>Industrial · Small Bay</div>
    <div>{quarter} &nbsp;·&nbsp; {date.today().strftime('%B %d, %Y')}</div>
  </div>
</div>

<div class="body">
  <div class="section">
    <div class="section-title">Market Summary</div>
    <div class="pills">{pills}</div>
  </div>

  <div class="section">
    <div class="section-title">Top 5 Markets — Combined Score</div>
    <table>
      <thead><tr>
        <th>Market</th><th style="text-align:center">Macro</th>
        <th style="text-align:center">Asset</th>
        <th style="text-align:center">Combined</th>
        <th style="text-align:center">Tier</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>

  <div class="section">
    <div class="section-title">High Conviction Markets</div>
    <div style="display:flex;flex-wrap:wrap;gap:10px">
"""
    hc = df[df["tier"]=="High Conviction"].sort_values(
        by=["macro_score","asset_score"], ascending=False)
    for _, r in hc.iterrows():
        combined = (r["macro_score"] + r["asset_score"]) / 2
        html += f"""<div style="background:#E1F5EE;border:1px solid #1D9E7544;border-radius:8px;padding:12px 16px;min-width:140px">
          <div style="font-weight:600;color:#0D4F45;font-size:14px">{r['msa']}</div>
          <div style="font-size:12px;color:#555;margin-top:4px">Macro: {r['macro_score']:.2f} &nbsp; Asset: {r['asset_score']:.2f}</div>
          <div style="font-size:13px;font-weight:700;color:#1D9E75;margin-top:4px">{combined:.2f} / 5.00</div>
        </div>"""

    html += f"""
    </div>
  </div>
</div>

<div class="footer">
  <div>Daki Capital · Industrial Small Bay Framework · {quarter}</div>
  <div>Data: Illustrative (sample scores pending Green Street integration)</div>
</div>
<div style="padding:8px 40px;background:#F7FAF9">
  <p class="disclaimer">This report has been prepared by Daki Capital for internal use only. Data shown is illustrative and based on sample scores. Not for distribution.</p>
</div>
</body></html>"""
    return html


# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar(all_msas):
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:8px 0 20px;text-align:center;">
            {logo_img_sidebar}
            <div style="font-size:11px;color:rgba(255,255,255,0.5);margin-top:8px;letter-spacing:0.08em;">MSA INTELLIGENCE</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("**DATA SOURCE**")
        data_mode = st.radio("", ["Sample data", "Upload file", "Google Sheet"], label_visibility="collapsed")
        uploaded, sheet_url = None, None
        if data_mode == "Upload file":
            uploaded = st.file_uploader("CSV or Excel", type=["csv","xlsx"])
        elif data_mode == "Google Sheet":
            sheet_url = st.text_input("Google Sheet URL", placeholder="https://docs.google.com/spreadsheets/d/...")

        st.markdown("---")
        st.markdown("**FILTERS**")
        tiers = st.multiselect("Conviction tier",
            ["High Conviction","Strong Asset","Strong Macro","Monitor"],
            default=["High Conviction","Strong Asset","Strong Macro","Monitor"])

        selected_msas = st.multiselect("MSAs", sorted(all_msas), default=[])
        quarter_filter = st.selectbox("Reference quarter", QUARTERS, index=len(QUARTERS)-1)

        st.markdown("**Time range**")
        YEARS = ["2021","2022","2023","2024","2025","2026","All (5 years)"]
        time_filter = st.selectbox("Show period", YEARS, index=len(YEARS)-1)

        macro_range = st.slider("Macro Score range", 0.0, 5.0, (0.0, 5.0), 0.1)
        asset_range = st.slider("Asset Score range", 0.0, 5.0, (0.0, 5.0), 0.1)

        st.markdown("---")
        st.markdown("**THRESHOLDS**")
        macro_mid = st.slider("Macro midline", 0.0, 5.0, 2.25, 0.05)
        asset_mid = st.slider("Asset midline", 0.0, 5.0, 2.56, 0.05)

    return uploaded, sheet_url, tiers, selected_msas, quarter_filter, time_filter, macro_range, asset_range, macro_mid, asset_mid

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    all_msas = sorted(get_base_df()["msa"].dropna().tolist())
    uploaded, sheet_url, tiers, selected_msas, quarter_filter, time_filter, macro_range, asset_range, macro_mid, asset_mid = render_sidebar(all_msas)

    # Header
    col_header, col_btn = st.columns([8, 1])
    with col_header:
        st.markdown(f"""
        <div class="daki-header">
            {logo_img}
            <div>
                <div style="font-size:13px;color:rgba(255,255,255,0.65);letter-spacing:0.04em;margin-top:4px;">Industrial · Small Bay · MSA Selection Framework &nbsp;<span style="background:#1D9E75;color:white;font-size:10px;padding:2px 8px;border-radius:10px;font-weight:600;letter-spacing:0.05em;">LIVE DATA</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if "sidebar_open" not in st.session_state:
            st.session_state.sidebar_open = True
        if st.button("Filters", use_container_width=True):
            st.session_state.sidebar_open = not st.session_state.sidebar_open

    # Show filters inline when sidebar is toggled open via button
    if not st.session_state.sidebar_open:
        with st.expander("Filters & Settings", expanded=True):
            fc1, fc2, fc3, fc4 = st.columns(4)
            with fc1:
                tiers = st.multiselect("Conviction tier",
                    ["High Conviction","Strong Asset","Strong Macro","Monitor"],
                    default=tiers, key="inline_tiers")
            with fc2:
                selected_msas = st.multiselect("MSAs", sorted(all_msas),
                    default=selected_msas, key="inline_msas")
            with fc3:
                macro_range = st.slider("Macro Score", 0.0, 5.0, macro_range, 0.1, key="inline_macro")
                asset_range = st.slider("Asset Score", 0.0, 5.0, asset_range, 0.1, key="inline_asset")
            with fc4:
                macro_mid = st.slider("Macro midline", 0.0, 5.0, macro_mid, 0.05, key="inline_mmid")
                asset_mid = st.slider("Asset midline", 0.0, 5.0, asset_mid, 0.05, key="inline_amid")

    # Load data
    df = get_base_df(macro_mid, asset_mid)

    if uploaded is not None:
        try:
            raw = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
            raw.columns = [c.strip().lower().replace(" ","_") for c in raw.columns]
            if "macro_score" in raw.columns and "asset_score" in raw.columns:
                raw["tier"] = raw.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)
                df = raw
                st.success(f"File loaded: {len(df)} markets")
        except Exception as e:
            st.error(f"Error loading file: {e}")

    elif sheet_url and "docs.google.com" in sheet_url:
        try:
            sheet_id = sheet_url.split("/d/")[1].split("/")[0]
            raw = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
            raw.columns = [c.strip().lower().replace(" ","_") for c in raw.columns]
            if "macro_score" in raw.columns and "asset_score" in raw.columns:
                raw["tier"] = raw.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)
                df = raw
                st.success(f"Google Sheet connected: {len(df)} markets")
        except Exception as e:
            st.error(f"Could not connect to sheet: {e}")

    df["tier"] = df.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)

    # Apply filters
    filtered = df[df["tier"].isin(tiers) &
                  df["macro_score"].between(*macro_range) &
                  df["asset_score"].between(*asset_range)].copy()
    if selected_msas:
        filtered = filtered[filtered["msa"].isin(selected_msas)]

    # KPI cards
    alta  = len(filtered[filtered["tier"]=="High Conviction"])
    asset = len(filtered[filtered["tier"]=="Strong Asset"])
    macro = len(filtered[filtered["tier"]=="Strong Macro"])
    watch = len(filtered[filtered["tier"]=="Monitor"])
    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card"><div class="kpi-val">{len(filtered)}</div><div class="kpi-lbl">Total MSAs</div></div>
        <div class="kpi-card green"><div class="kpi-val">{alta}</div><div class="kpi-lbl">High Conviction</div></div>
        <div class="kpi-card blue"><div class="kpi-val">{asset}</div><div class="kpi-lbl">Strong Asset</div></div>
        <div class="kpi-card amber"><div class="kpi-val">{macro}</div><div class="kpi-lbl">Strong Macro</div></div>
        <div class="kpi-card gray"><div class="kpi-val">{watch}</div><div class="kpi-lbl">Monitor</div></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Scatter Plot", "US Map", "Heat Map", "Trajectories", "Rankings", "Executive Summary", "Methodology"])

    # ── Tab 1: Scatter ────────────────────────────────────────────────────────
    with tab1:
        col_chart, col_detail = st.columns([3,1])
        with col_chart:
            st.markdown('<div class="section-title">Market Conviction Map</div>', unsafe_allow_html=True)
            fig = make_scatter(filtered, macro_mid, asset_mid)
            selected = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="scatter")
        with col_detail:
            st.markdown('<div class="section-title">City Detail</div>', unsafe_allow_html=True)
            sel_city = None
            if selected and selected.get("selection") and selected["selection"].get("points"):
                pt = selected["selection"]["points"][0]
                match = filtered[(filtered["macro_score"].round(2)==round(pt["x"],2)) &
                                  (filtered["asset_score"].round(2)==round(pt["y"],2))]
                if not match.empty:
                    sel_city = match.iloc[0]["msa"]
            if sel_city:
                row = filtered[filtered["msa"]==sel_city].iloc[0]
                tc = TIER_COLORS[row["tier"]]
                cls = TIER_CLASS[row["tier"]]
                st.markdown(f"### {row['msa']}")
                st.markdown(f'<span class="tier-badge {cls}">{row["tier"]}</span>', unsafe_allow_html=True)
                st.markdown("")
                c1, c2 = st.columns(2)
                c1.metric("Macro Score", f"{row['macro_score']:.2f}")
                c2.metric("Asset Score", f"{row['asset_score']:.2f}")
                combined = (row["macro_score"] + row["asset_score"]) / 2
                st.markdown(f"**Combined score: {combined:.2f} / 5.00**")
                st.progress(min(combined / 5, 1.0))
            else:
                st.info("Click any dot to see city details.")
                badges = " &nbsp; ".join([f'<span class="tier-badge {cls}">{tier}</span>' for tier, cls in TIER_CLASS.items()])
                st.markdown(badges, unsafe_allow_html=True)
                st.caption("Top-right = High Conviction · Bottom-left = Monitor")

    # ── Tab 2: US Map ─────────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-title">US Market Heat Map</div>', unsafe_allow_html=True)

        map_c1, map_c2, map_c3, map_c4 = st.columns([3, 2, 2, 2])
        with map_c1:
            map_metric = st.radio("Score", ["Combined Score","Macro Score","Asset Score"],
                                  horizontal=True, label_visibility="collapsed")
        with map_c2:
            map_period_type = st.radio("Time view", ["Current", "Specific quarter"],
                                       horizontal=True, label_visibility="collapsed")
        with map_c3:
            if map_period_type == "Specific quarter":
                map_quarter = st.selectbox("Quarter", QUARTERS, index=len(QUARTERS)-1,
                                           label_visibility="collapsed")
            else:
                map_quarter = None
        with map_c4:
            STATE_OPTIONS = ["All states","AL","AZ","AR","CA","CO","CT","DE","FL","GA",
                             "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA",
                             "MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY",
                             "NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX",
                             "UT","VT","VA","WA","WV","WI","WY"]
            zoom_selection = st.selectbox("Zoom to state", STATE_OPTIONS,
                                          index=0, label_visibility="collapsed")
            zoom_state = None if zoom_selection == "All states" else zoom_selection

        map_metric_key = {"Combined Score":"combined","Macro Score":"macro_score","Asset Score":"asset_score"}[map_metric]

        # Build the dataframe to display on the map
        if map_period_type == "Specific quarter" and map_quarter:
            ts_df_map = get_timeseries_df()
            ts_q = ts_df_map[ts_df_map["quarter"] == map_quarter].copy()
            ts_q = ts_q[ts_q["msa"].isin(filtered["msa"].tolist())].copy()
            ts_q["combined"] = (ts_q["macro_score"] + ts_q["asset_score"]) / 2
            ts_q["tier"] = ts_q.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)
            map_df = ts_q
            period_label = f"**{map_quarter}**"
        else:
            map_df = filtered.copy()
            if "combined" not in map_df.columns:
                map_df["combined"] = (map_df["macro_score"] + map_df["asset_score"]) / 2
            period_label = "**current scores** (Q1 2026)"

        zoom_label = f" · Zoomed to **{zoom_state}**" if zoom_state else ""
        st.caption(f"Showing {period_label}{zoom_label}. Color = conviction tier. Hover for details.")

        # Show MSAs in selected state
        if zoom_state:
            state_msas_list = [msa for msa, st in MSA_STATE.items() if st == zoom_state and msa in map_df["msa"].values]
            if state_msas_list:
                st.markdown(f"**MSAs tracked in {zoom_state}:** {', '.join(state_msas_list)}")
            else:
                st.info(f"No tracked MSAs in {zoom_state}.")

        fig_map = make_us_map(map_df, metric=map_metric_key, zoom_state=zoom_state)
        st.plotly_chart(fig_map, use_container_width=True)

    # ── Tab 3: Heat Map ───────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-title">Heat Map — Market Rankings Over Time</div>', unsafe_allow_html=True)
        st.caption("Inspired by the BlackRock Asset Return Map. Each column is a quarter; cities are ranked best to worst within each period. Darker = stronger score.")

        ts_df = get_timeseries_df()
        ts_filtered = ts_df[ts_df["msa"].isin(filtered["msa"].tolist())]
        ts_filtered = filter_quarters_by_period(ts_filtered, time_filter)

        hm_col1, hm_col2, hm_col3 = st.columns([3, 1, 1])
        with hm_col1:
            hm_metric = st.radio("Score to display",
                                 ["Macro Score", "Asset Score", "Combined Score"],
                                 horizontal=True, label_visibility="collapsed")
        with hm_col2:
            top_n = st.selectbox("Show top", [10, 15, 20, 30, len(filtered)],
                                 index=1, format_func=lambda x: f"Top {x}" if x != len(filtered) else "All")
        with hm_col3:
            hm_period = st.selectbox("Period", ["All (5 years)","2021","2022","2023","2024","2025","2026"],
                                     index=0, key="hm_period")
            ts_filtered = filter_quarters_by_period(ts_filtered, hm_period)

        metric_map = {"Macro Score": "macro_score", "Asset Score": "asset_score", "Combined Score": "combined"}
        metric_key = metric_map[hm_metric]

        fig_hm = make_blackrock_heatmap(ts_filtered, metric_key, top_n=int(top_n))
        st.plotly_chart(fig_hm, use_container_width=True)

    # ── Tab 4: Trajectories ───────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-title">MSA Trajectories — Movement Over Time</div>', unsafe_allow_html=True)
        st.caption("Select cities to see how they have moved across the scatter plot over time. Diamond = most recent quarter. Hover over each point to see the quarter.")

        traj_col1, traj_col2 = st.columns([3,1])
        with traj_col1:
            default_cities = ["Houston","Nashville","Chicago","Tampa-St. Petersburg","Detroit"]
            avail_defaults = [c for c in default_cities if c in all_msas]
            sel_cities = st.multiselect("Select markets to compare", sorted(all_msas),
                                        default=avail_defaults, max_selections=8)
        with traj_col2:
            traj_period = st.selectbox("Time period", ["All (5 years)","2021","2022","2023","2024","2025","2026"],
                                       index=0, key="traj_period")

        if sel_cities:
            ts_df = get_timeseries_df()
            ts_df_filt = filter_quarters_by_period(ts_df, traj_period)
            # Ensure quarters are sorted chronologically
            ts_df_filt = ts_df_filt.sort_values("quarter_idx")

            fig_traj = make_trajectory(ts_df_filt, sel_cities)
            st.plotly_chart(fig_traj, use_container_width=True)

            st.markdown('<div class="section-title">Combined Score by Quarter</div>', unsafe_allow_html=True)
            ts_sel = ts_df_filt[ts_df_filt["msa"].isin(sel_cities)][["msa","quarter","quarter_idx","combined"]]
            # Sort quarters chronologically before pivoting
            quarter_order = ts_df_filt["quarter"].drop_duplicates().sort_values().tolist()
            # Use proper chronological sort via quarter_idx
            q_sorted = ts_df_filt[["quarter","quarter_idx"]].drop_duplicates().sort_values("quarter_idx")["quarter"].tolist()
            ts_pivot = ts_sel.pivot_table(index="msa", columns="quarter", values="combined").round(2)
            ts_pivot = ts_pivot.reindex(columns=[c for c in q_sorted if c in ts_pivot.columns])
            st.dataframe(ts_pivot, use_container_width=True)
        else:
            st.info("Select at least one market above.")

    # ── Tab 5: Rankings ───────────────────────────────────────────────────────
    with tab5:
        st.markdown('<div class="section-title">MSA Rankings — sorted by combined score</div>', unsafe_allow_html=True)
        ranked = filtered[["msa","macro_score","asset_score","tier"]].copy()
        ranked["combined"] = ((ranked["macro_score"] + ranked["asset_score"]) / 2).round(2)
        ranked = ranked.sort_values("combined", ascending=False).reset_index(drop=True)
        ranked.index += 1
        ranked.columns = ["MSA","Macro Score","Asset Score","Tier","Combined (0–5)"]
        ranked["Macro Score"] = ranked["Macro Score"].round(2)
        ranked["Asset Score"] = ranked["Asset Score"].round(2)

        def color_tier(val):
            colors = {
                "High Conviction": "background-color:#E1F5EE;color:#0F6E56;font-weight:600",
                "Strong Asset":    "background-color:#E6F1FB;color:#185FA5;font-weight:600",
                "Strong Macro":    "background-color:#FAEEDA;color:#854F0B;font-weight:600",
                "Monitor":         "background-color:#F1EFE8;color:#5F5E5A;font-weight:600",
            }
            return colors.get(val,"")

        styled = ranked.style.map(color_tier, subset=["Tier"])
        st.dataframe(styled, use_container_width=True, height=580)
        csv = ranked.to_csv(index=True).encode("utf-8")
        st.download_button("Download Rankings CSV", csv, "daki_rankings.csv", "text/csv")

    # ── Tab 6: Executive Summary ──────────────────────────────────────────────
    with tab6:
        st.markdown('<div class="section-title">Executive Summary — Exportable Report</div>', unsafe_allow_html=True)
        st.caption("One-page summary ready to share with your IC or investors.")

        col_a, col_b = st.columns([2,1])
        with col_a:
            report_quarter = st.selectbox("Report quarter", QUARTERS, index=len(QUARTERS)-1)
        with col_b:
            report_tier = st.multiselect("Include tiers", list(TIER_COLORS.keys()),
                                         default=list(TIER_COLORS.keys()))

        report_df = filtered[filtered["tier"].isin(report_tier)].copy()
        report_df["combined"] = (report_df["macro_score"] + report_df["asset_score"]) / 2

        # Preview
        st.markdown("#### Preview")
        prev_col1, prev_col2 = st.columns(2)
        with prev_col1:
            st.markdown("**Market breakdown**")
            for tier, color in TIER_COLORS.items():
                count = len(report_df[report_df["tier"]==tier])
                st.markdown(
                    f'<span class="tier-badge {TIER_CLASS[tier]}">{tier}</span>'
                    f'<span style="margin-left:8px;font-size:13px;color:#555">{count} markets</span>',
                    unsafe_allow_html=True)
                st.markdown("")
        with prev_col2:
            st.markdown("**Top 5 markets**")
            top5 = report_df.nlargest(5, "combined")[["msa","combined","tier"]]
            for _, r in top5.iterrows():
                cls = TIER_CLASS.get(r["tier"],"")
                st.markdown(
                    f'**{r["msa"]}** — {r["combined"]:.2f} '
                    f'<span class="tier-badge {cls}" style="font-size:10px">{r["tier"]}</span>',
                    unsafe_allow_html=True)

        st.divider()
        html_report = make_executive_summary(report_df, report_quarter, logo_b64)
        st.download_button(
            label="Download Executive Summary (HTML)",
            data=html_report.encode("utf-8"),
            file_name=f"daki_executive_summary_{report_quarter.replace(' ','_')}.html",
            mime="text/html",
            type="primary",
        )
        st.caption("Opens in any browser. Print to PDF from there for a clean one-pager (File → Print → Save as PDF).")

    # ── Tab 7: Methodology ────────────────────────────────────────────────────
    with tab7:
        st.markdown('<div class="section-title">Daki Score — Scoring Methodology</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="max-width:900px">
        <p style="color:#A8D5CC;font-size:14px;line-height:1.7;margin-bottom:24px">
        The Daki Score is a two-dimensional framework for evaluating US industrial real estate markets.
        Each MSA receives two independent scores — a <strong>Macro Score</strong> and an <strong>Asset Class Score</strong> —
        which together determine its position on the conviction scatter plot.
        </p>
        </div>
        """, unsafe_allow_html=True)

        # How scores work
        col_how1, col_how2 = st.columns(2)
        with col_how1:
            st.markdown("""
            <div style="background:#1A2E2A;border:1px solid #2A4A44;border-radius:8px;padding:20px 24px;height:100%">
            <div style="font-size:13px;font-weight:600;color:#1D9E75;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:12px">How It Works</div>
            <p style="color:#A8D5CC;font-size:13px;line-height:1.7">
            Each variable is scored on a <strong>normalized 0–1 scale</strong> based on its observed range across all tracked MSAs.
            Variables are then multiplied by their assigned weight and summed to produce a final score between <strong>0 and 5</strong>.
            </p>
            <p style="color:#A8D5CC;font-size:13px;line-height:1.7;margin-top:10px">
            The <strong>Combined Score</strong> is the simple average of Macro and Asset scores (0–5).
            Quadrant classification uses adjustable midline thresholds — default 3.0 for Macro and 3.25 for Asset.
            </p>
            </div>
            """, unsafe_allow_html=True)
        with col_how2:
            st.markdown("""
            <div style="background:#1A2E2A;border:1px solid #2A4A44;border-radius:8px;padding:20px 24px;height:100%">
            <div style="font-size:13px;font-weight:600;color:#1D9E75;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:12px">Quadrant Logic</div>
            <div style="margin-bottom:10px"><span style="background:#E1F5EE22;color:#1D9E75;padding:3px 10px;border-radius:10px;font-size:12px;font-weight:600">High Conviction</span>
            <span style="color:#A8D5CC;font-size:13px;margin-left:8px">Strong macro + strong asset fundamentals → deploy</span></div>
            <div style="margin-bottom:10px"><span style="background:#E6F1FB22;color:#378ADD;padding:3px 10px;border-radius:10px;font-size:12px;font-weight:600">Strong Asset</span>
            <span style="color:#A8D5CC;font-size:13px;margin-left:8px">Great industrial fundamentals, macro still developing</span></div>
            <div style="margin-bottom:10px"><span style="background:#FAEEDA22;color:#BA7517;padding:3px 10px;border-radius:10px;font-size:12px;font-weight:600">Strong Macro</span>
            <span style="color:#A8D5CC;font-size:13px;margin-left:8px">Strong MSA, wait for asset cycle to turn</span></div>
            <div><span style="background:#88878022;color:#888780;padding:3px 10px;border-radius:10px;font-size:12px;font-weight:600">Monitor</span>
            <span style="color:#A8D5CC;font-size:13px;margin-left:8px">Neither score above threshold — watch only</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # Macro variables table
        col_m, col_a = st.columns(2)
        with col_m:
            st.markdown('<div class="section-title">Macro Score Variables (Y-axis)</div>', unsafe_allow_html=True)
            st.caption("MSA-level economic fundamentals — applies across all asset classes. Updated annually.")
            macro_rows = ""
            for v in MACRO_VARS:
                source = {
                    "pop_growth":      "US Census Bureau",
                    "employment":      "Bureau of Labor Statistics (BLS)",
                    "education":       "Census ACS",
                    "avg_salary":      "BLS QCEW",
                    "gdp_per_capita":  "Bureau of Economic Analysis (BEA)",
                    "households":      "Census ACS",
                    "household_spend": "BLS Consumer Expenditure Survey",
                    "pct_renters":     "Census ACS",
                    "ecommerce_index": "US Census E-Commerce Report",
                }.get(v["key"], "—")
                bar_w = int(v["weight"] * 500)
                macro_rows += f"""
                <tr>
                  <td style="padding:8px 10px;color:#A8D5CC;font-size:13px">{v['name']}</td>
                  <td style="padding:8px 10px;text-align:center">
                    <div style="display:flex;align-items:center;gap:6px">
                      <div style="width:{bar_w}px;height:6px;background:#1D9E75;border-radius:3px;min-width:4px"></div>
                      <span style="color:#1D9E75;font-weight:600;font-size:12px">{v['weight']:.0%}</span>
                    </div>
                  </td>
                  <td style="padding:8px 10px;color:#6b9e95;font-size:11px">{source}</td>
                </tr>"""
            st.markdown(f"""
            <table style="width:100%;border-collapse:collapse;font-size:13px">
              <thead><tr style="border-bottom:1px solid #2A4A44">
                <th style="padding:8px 10px;text-align:left;color:#6b9e95;font-size:11px;text-transform:uppercase;letter-spacing:0.05em">Variable</th>
                <th style="padding:8px 10px;text-align:left;color:#6b9e95;font-size:11px;text-transform:uppercase;letter-spacing:0.05em">Weight</th>
                <th style="padding:8px 10px;text-align:left;color:#6b9e95;font-size:11px;text-transform:uppercase;letter-spacing:0.05em">Source</th>
              </tr></thead>
              <tbody>{macro_rows}</tbody>
            </table>
            """, unsafe_allow_html=True)

        with col_a:
            st.markdown('<div class="section-title">Asset Class Score Variables (X-axis)</div>', unsafe_allow_html=True)
            st.caption("Industrial Small Bay specific fundamentals. Updated quarterly via Green Street.")
            asset_rows = ""
            for v in ASSET_VARS:
                source = {
                    "rent_growth": "Green Street Advisors / CoStar",
                    "occupancy":   "Green Street Advisors",
                    "pipeline":    "Green Street / Yardi Matrix",
                    "cap_rate":    "Green Street Advisors",
                    "rent_psf":    "CoStar / CompStak",
                    "sale_psf":    "CoStar / Real Capital Analytics",
                }.get(v["key"], "—")
                bar_w = int(v["weight"] * 500)
                asset_rows += f"""
                <tr>
                  <td style="padding:8px 10px;color:#A8D5CC;font-size:13px">{v['name']}</td>
                  <td style="padding:8px 10px;text-align:center">
                    <div style="display:flex;align-items:center;gap:6px">
                      <div style="width:{bar_w}px;height:6px;background:#378ADD;border-radius:3px;min-width:4px"></div>
                      <span style="color:#378ADD;font-weight:600;font-size:12px">{v['weight']:.0%}</span>
                    </div>
                  </td>
                  <td style="padding:8px 10px;color:#6b9e95;font-size:11px">{source}</td>
                </tr>"""
            st.markdown(f"""
            <table style="width:100%;border-collapse:collapse;font-size:13px">
              <thead><tr style="border-bottom:1px solid #2A4A44">
                <th style="padding:8px 10px;text-align:left;color:#6b9e95;font-size:11px;text-transform:uppercase;letter-spacing:0.05em">Variable</th>
                <th style="padding:8px 10px;text-align:left;color:#6b9e95;font-size:11px;text-transform:uppercase;letter-spacing:0.05em">Weight</th>
                <th style="padding:8px 10px;text-align:left;color:#6b9e95;font-size:11px;text-transform:uppercase;letter-spacing:0.05em">Source</th>
              </tr></thead>
              <tbody>{asset_rows}</tbody>
            </table>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # Update cadence
        st.markdown('<div class="section-title">Data Update Cadence</div>', unsafe_allow_html=True)
        cadence_cols = st.columns(3)
        cadences = [
            ("Quarterly", "#1D9E75", "Asset Class Score variables — rent growth, occupancy, pipeline, cap rates, rent PSF, sale PSF. Source: Green Street Advisors export."),
            ("Annually", "#378ADD", "Macro Score variables — population, employment, GDP, salaries, households. Source: Census Bureau, BLS, BEA annual releases."),
            ("Deal-level", "#BA7517", "Replacement cost ratio and yield-on-cost spread tracked separately for each active deal. Source: RSMeans, CoStar land comps."),
        ]
        for col, (freq, color, desc) in zip(cadence_cols, cadences):
            col.markdown(f"""
            <div style="background:#1A2E2A;border:1px solid #2A4A44;border-top:3px solid {color};border-radius:8px;padding:16px 18px">
              <div style="font-size:16px;font-weight:700;color:{color};margin-bottom:8px">{freq}</div>
              <div style="font-size:12px;color:#A8D5CC;line-height:1.6">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#1A2E2A;border:1px solid #1D9E75;border-radius:8px;padding:16px 20px;max-width:900px">
          <div style="font-size:12px;font-weight:600;color:#1D9E75;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px">Data Source</div>
          <div style="font-size:13px;color:#A8D5CC;line-height:1.6">
          Scores are computed from <strong>Green Street Advisors</strong> Industrial market data (2025).
          Macro Score is derived from Desirability Index, Demand Growth, % College Degree, Median Household Income, and E-Commerce Penetration.
          Asset Class Score is derived from RevPAF Growth, Supply Barriers, Supply Growth, and Market Grade.
          Variable weights are subject to refinement as the methodology is calibrated against deal performance.
          </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
