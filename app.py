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
logo_img         = f'<img src="data:image/png;base64,{logo_b64}" style="height:56px;object-fit:contain;" />' if logo_b64 else '<span style="font-size:22px;font-weight:700;color:white;letter-spacing:0.05em;">DAKI CAPITAL</span>'
logo_img_sidebar = f'<img src="data:image/png;base64,{logo_b64}" style="height:46px;object-fit:contain;max-width:180px;" />' if logo_b64 else '<span style="font-size:18px;font-weight:700;color:white;">DAKI CAPITAL</span>'

# ── Brand CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

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
    flex: 1; background: #ffffff; border: 1px solid #e8ede9;
    border-radius: 8px; padding: 12px 16px; border-top: 3px solid #0D4F45;
}}
.kpi-val {{ font-size: 24px; font-weight: 700; color: #0D4F45; }}
.kpi-lbl {{ font-size: 11px; color: #6b7c75; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.05em; }}
.kpi-card.green {{ border-top-color: #1D9E75; }} .kpi-card.blue {{ border-top-color: #378ADD; }}
.kpi-card.amber {{ border-top-color: #BA7517; }} .kpi-card.gray  {{ border-top-color: #888780; }}

.tier-badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
.tier-alta    {{ background: #E1F5EE; color: #0F6E56; }}
.tier-asset   {{ background: #E6F1FB; color: #185FA5; }}
.tier-macro   {{ background: #FAEEDA; color: #854F0B; }}
.tier-monitor {{ background: #F1EFE8; color: #5F5E5A; }}

.stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 2px solid #e0e8e5; }}
.stTabs [data-baseweb="tab"] {{ padding: 8px 18px; font-size: 13px; font-weight: 500; color: #6b7c75; border-radius: 6px 6px 0 0; }}
.stTabs [aria-selected="true"] {{ background: #0D4F45 !important; color: #ffffff !important; }}

.section-title {{
    font-size: 14px; font-weight: 600; color: #0D4F45;
    border-left: 3px solid #1D9E75; padding-left: 10px; margin-bottom: 12px;
}}
[data-testid="metric-container"] {{
    background: #f7faf9; border: 1px solid #e0e8e5; border-radius: 8px; padding: 10px 14px;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1rem; }}
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

def assign_tier(macro, asset, macro_mid=3.0, asset_mid=3.25):
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

QUARTERS = ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026"]

def get_base_df(macro_mid=3.0, asset_mid=3.25):
    df = pd.DataFrame(BASE_DATA)
    df["tier"] = df.apply(lambda r: assign_tier(r["macro_score"], r["asset_score"], macro_mid, asset_mid), axis=1)
    return df

def get_timeseries_df():
    rows = []
    random.seed(42)
    for city in BASE_DATA:
        m, a = city["macro_score"], city["asset_score"]
        for i, q in enumerate(QUARTERS):
            ms  = round(max(0.1, min(4.99, m + random.uniform(-0.15, 0.15) * i)), 2)
            as_ = round(max(0.1, min(4.99, a + random.uniform(-0.2, 0.25) * i)), 2)
            rows.append({"msa": city["msa"], "short": city["short"],
                         "quarter": q, "macro_score": ms, "asset_score": as_,
                         "combined": round((ms + as_) / 2, 2)})
    return pd.DataFrame(rows)

# ── Charts ────────────────────────────────────────────────────────────────────
def make_scatter(df, macro_mid, asset_mid):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=macro_mid, x1=5.3, y0=asset_mid, y1=5.5, fillcolor="rgba(29,158,117,0.07)", line_width=0)
    fig.add_shape(type="rect", x0=0, x1=macro_mid, y0=asset_mid, y1=5.5, fillcolor="rgba(55,138,221,0.06)", line_width=0)
    fig.add_shape(type="rect", x0=macro_mid, x1=5.3, y0=0, y1=asset_mid, fillcolor="rgba(186,117,23,0.06)", line_width=0)
    for x0,x1,y0,y1 in [(macro_mid,macro_mid,0,5.5),(0,5.3,asset_mid,asset_mid)]:
        fig.add_shape(type="line",x0=x0,x1=x1,y0=y0,y1=y1,line=dict(color="rgba(13,79,69,0.25)",width=1,dash="dash"))
    for txt,x,y in [("High Conviction ↗",macro_mid+0.08,5.35),("Strong Asset",0.08,5.35),
                    ("Strong Macro",macro_mid+0.08,0.15),("Monitor",0.08,0.15)]:
        fig.add_annotation(text=txt,x=x,y=y,showarrow=False,font=dict(size=10,color="rgba(13,79,69,0.45)"),xanchor="left")
    for tier, grp in df.groupby("tier"):
        fig.add_trace(go.Scatter(
            x=grp["macro_score"], y=grp["asset_score"],
            mode="markers+text", name=tier,
            text=grp["short"], textposition="top center", textfont=dict(size=9, color="#333"),
            marker=dict(size=11, color=TIER_COLORS[tier], opacity=0.9, line=dict(width=1.5, color="white")),
            customdata=grp[["msa","macro_score","asset_score","tier"]].values,
            hovertemplate="<b>%{customdata[0]}</b><br>Macro: %{customdata[1]:.2f}  |  Asset: %{customdata[2]:.2f}<br>Tier: %{customdata[3]}<extra></extra>"
        ))
    fig.update_layout(
        xaxis=dict(title="Daki Macro Score", range=[0,5.3], showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False, title_font=dict(size=12,color="#0D4F45")),
        yaxis=dict(title="Daki Asset Class Score", range=[0,5.5], showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False, title_font=dict(size=12,color="#0D4F45")),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1, font=dict(size=11)),
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
    quarters = QUARTERS

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
        plot_bgcolor="#f7faf9",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=80, t=40, b=20),
        height=top_n * cell_h + 80,
        xaxis=dict(
            side="top",
            tickfont=dict(size=13, color="#0D4F45"),
            showgrid=False, zeroline=False,
        ),
        yaxis=dict(
            tickfont=dict(size=12, color="#555"),
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
    fig.add_shape(type="line",x0=3,x1=3,y0=0,y1=5.5,line=dict(color="rgba(13,79,69,0.2)",dash="dash",width=1))
    fig.add_shape(type="line",x0=0,x1=5.3,y0=3.25,y1=3.25,line=dict(color="rgba(13,79,69,0.2)",dash="dash",width=1))
    fig.update_layout(
        xaxis=dict(title="Daki Macro Score", range=[0,5.3], showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False),
        yaxis=dict(title="Daki Asset Class Score", range=[0,5.5], showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(size=11)),
        margin=dict(l=40,r=20,t=20,b=40), height=460,
        font=dict(family="Inter, sans-serif"),
    )
    return fig

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

        macro_range = st.slider("Macro Score range", 0.0, 5.0, (0.0, 5.0), 0.1)
        asset_range = st.slider("Asset Score range", 0.0, 5.0, (0.0, 5.0), 0.1)

        st.markdown("---")
        st.markdown("**THRESHOLDS**")
        macro_mid = st.slider("Macro midline", 0.0, 5.0, 3.0, 0.05)
        asset_mid = st.slider("Asset midline", 0.0, 5.0, 3.25, 0.05)

    return uploaded, sheet_url, tiers, selected_msas, quarter_filter, macro_range, asset_range, macro_mid, asset_mid

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    all_msas = [d["msa"] for d in BASE_DATA]
    uploaded, sheet_url, tiers, selected_msas, quarter_filter, macro_range, asset_range, macro_mid, asset_mid = render_sidebar(all_msas)

    # Header
    st.markdown(f"""
    <div class="daki-header">
        {logo_img}
        <div>
            <div style="font-size:13px;color:rgba(255,255,255,0.65);letter-spacing:0.04em;margin-top:4px;">Industrial · Small Bay · MSA Selection Framework</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    tab1, tab2, tab3, tab4 = st.tabs(["Scatter Plot", "Heat Map", "Trajectories", "Rankings"])

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
                for tier, cls in TIER_CLASS.items():
                    st.markdown(f'<span class="tier-badge {cls}">{tier}</span> ', unsafe_allow_html=True)
                st.markdown("")
                st.caption("Top-right = High Conviction\nBottom-left = Monitor")

    # ── Tab 2: Heat Map ───────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-title">Heat Map — Market Rankings Over Time</div>', unsafe_allow_html=True)
        st.caption("Inspired by the BlackRock Asset Return Map. Each column is a quarter; cities are ranked best to worst within each period. Darker = stronger score.")

        ts_df = get_timeseries_df()
        ts_filtered = ts_df[ts_df["msa"].isin(filtered["msa"].tolist())]

        hm_col1, hm_col2 = st.columns([3, 1])
        with hm_col1:
            hm_metric = st.radio("Score to display",
                                 ["Macro Score", "Asset Score", "Combined Score"],
                                 horizontal=True, label_visibility="collapsed")
        with hm_col2:
            top_n = st.selectbox("Show top", [10, 15, 20, 30, len(filtered)],
                                 index=1, format_func=lambda x: f"Top {x}" if x != len(filtered) else "All")

        metric_map = {"Macro Score": "macro_score", "Asset Score": "asset_score", "Combined Score": "combined"}
        metric_key = metric_map[hm_metric]

        fig_hm = make_blackrock_heatmap(ts_filtered, metric_key, top_n=int(top_n))
        st.plotly_chart(fig_hm, use_container_width=True)

    # ── Tab 3: Trajectories ───────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-title">MSA Trajectories — Movement Over Time</div>', unsafe_allow_html=True)
        st.caption("Select cities to see how they have moved across the scatter plot over time. Diamond = most recent quarter. Hover over each point to see the quarter.")
        default_cities = ["Houston","Nashville","Chicago","Tampa","Detroit"]
        sel_cities = st.multiselect("Select markets to compare", sorted(all_msas),
                                    default=default_cities, max_selections=8)
        if sel_cities:
            ts_df = get_timeseries_df()
            fig_traj = make_trajectory(ts_df, sel_cities)
            st.plotly_chart(fig_traj, use_container_width=True)
            st.markdown('<div class="section-title">Score by Quarter</div>', unsafe_allow_html=True)
            ts_sel = ts_df[ts_df["msa"].isin(sel_cities)][["msa","quarter","macro_score","asset_score","combined"]]
            ts_pivot = ts_sel.pivot_table(index="msa", columns="quarter", values="combined").round(2)
            st.dataframe(ts_pivot, use_container_width=True)
        else:
            st.info("Select at least one market above.")

    # ── Tab 4: Rankings ───────────────────────────────────────────────────────
    with tab4:
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

if __name__ == "__main__":
    main()
