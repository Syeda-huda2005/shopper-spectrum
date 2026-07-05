"""
Shopverse  
“Where every choice meets innovation.” 
Customer Segmentation & Product Recommendation Engine
From Insight to Impact: Turning Every Customer Into Your Most Profitable Relationship
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Shopper Spectrum | AI-Powered Retail Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Ultra Premium CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif !important; }

/* ── Background ── */
.stApp { background: #060b18 !important; }
.main .block-container { padding: 1.5rem 2rem 3rem 2rem !important; max-width: 1400px !important; }

/* ── Animated Hero ── */
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(99,102,241,0.4); }
    50%       { box-shadow: 0 0 0 15px rgba(99,102,241,0); }
}
@keyframes shimmer {
    0%   { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-8px); }
}
@keyframes countUp {
    from { opacity: 0; transform: scale(0.5); }
    to   { opacity: 1; transform: scale(1); }
}

.hero-wrapper {
    background: linear-gradient(-45deg, #0d1b3e, #0a0f2e, #1a0a3e, #0d2040, #060b18);
    background-size: 400% 400%;
    animation: gradientShift 8s ease infinite;
    border-radius: 24px;
    padding: 3.5rem 3rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(99,102,241,0.3);
    position: relative;
    overflow: hidden;
}
.hero-wrapper::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(99,102,241,0.15) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(34,211,238,0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 60% 80%, rgba(244,114,182,0.08) 0%, transparent 50%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 50px;
    padding: 6px 18px;
    font-size: 0.75rem; font-weight: 600;
    color: #a5b4fc; letter-spacing: 0.1em; text-transform: uppercase;
    margin-bottom: 1.2rem;
    animation: fadeInUp 0.6s ease both;
}
.hero-title {
    font-size: 3.8rem; font-weight: 900; line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 40%, #22d3ee 70%, #f472b6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 1rem 0;
    animation: fadeInUp 0.7s ease 0.1s both;
}
.hero-sub {
    font-size: 1.2rem; color: #94a3b8; font-weight: 400; line-height: 1.7;
    max-width: 650px;
    animation: fadeInUp 0.8s ease 0.2s both;
}
.hero-sub span { color: #a5b4fc; font-weight: 600; }
.hero-tags {
    display: flex; flex-wrap: wrap; gap: 10px; margin-top: 1.8rem;
    animation: fadeInUp 0.9s ease 0.3s both;
}
.hero-tag {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px; padding: 6px 14px;
    font-size: 0.78rem; color: #64748b; font-weight: 500;
}
.hero-tag span { color: #94a3b8; }

/* ── KPI Cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 2rem; }
.kpi-card {
    background: linear-gradient(135deg, #0f1729 0%, #111827 100%);
    border: 1px solid #1e293b;
    border-radius: 16px; padding: 1.4rem 1.2rem;
    text-align: center; position: relative; overflow: hidden;
    transition: all 0.3s ease;
    animation: countUp 0.6s ease both;
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    border-radius: 16px 16px 0 0;
}
.kpi-card:nth-child(1)::before { background: linear-gradient(90deg, #6366f1, #818cf8); }
.kpi-card:nth-child(2)::before { background: linear-gradient(90deg, #22d3ee, #67e8f9); }
.kpi-card:nth-child(3)::before { background: linear-gradient(90deg, #f472b6, #fb7185); }
.kpi-card:nth-child(4)::before { background: linear-gradient(90deg, #facc15, #fde68a); }
.kpi-card:nth-child(5)::before { background: linear-gradient(90deg, #4ade80, #86efac); }
.kpi-card:hover { transform: translateY(-4px); border-color: #334155; box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
.kpi-icon { font-size: 1.6rem; margin-bottom: 0.5rem; }
.kpi-val { font-size: 2rem; font-weight: 800; color: #f1f5f9; line-height: 1; margin-bottom: 0.3rem; }
.kpi-lbl { font-size: 0.72rem; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; }
.kpi-delta { font-size: 0.75rem; color: #4ade80; font-weight: 600; margin-top: 0.4rem; }

/* ── Section Headers ── */
.section-wrap { margin: 2rem 0 1rem 0; }
.section-eyebrow { font-size: 0.7rem; font-weight: 700; color: #6366f1; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.3rem; }
.section-title { font-size: 1.5rem; font-weight: 700; color: #f1f5f9; margin: 0; }
.section-sub { font-size: 0.88rem; color: #64748b; margin-top: 0.3rem; }

/* ── Insight Cards ── */
.insight-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 1.5rem 0; }
.insight-card {
    background: #0f1729; border: 1px solid #1e293b;
    border-radius: 14px; padding: 1.2rem;
    display: flex; align-items: flex-start; gap: 14px;
    transition: all 0.25s;
}
.insight-card:hover { border-color: #334155; transform: translateX(4px); }
.insight-icon-wrap {
    width: 44px; height: 44px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; flex-shrink: 0;
}
.insight-content .insight-title { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
.insight-content .insight-val { font-size: 1.15rem; font-weight: 700; color: #f1f5f9; margin: 0.2rem 0; }
.insight-content .insight-desc { font-size: 0.78rem; color: #475569; line-height: 1.5; }

/* ── Segment Cards ── */
.seg-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.seg-card {
    background: #0f1729; border-radius: 16px; padding: 1.4rem;
    border: 1px solid #1e293b; position: relative; overflow: hidden;
    transition: all 0.3s;
}
.seg-card:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,0,0,0.4); }
.seg-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; }
.seg-name { font-size: 1rem; font-weight: 700; color: #f1f5f9; }
.seg-count { font-size: 0.78rem; color: #64748b; margin-top: 2px; }
.seg-badge-pill {
    padding: 4px 12px; border-radius: 50px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.05em;
}
.seg-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 1rem; }
.seg-metric { text-align: center; background: rgba(255,255,255,0.03); border-radius: 10px; padding: 0.6rem; }
.seg-metric-val { font-size: 1rem; font-weight: 700; color: #f1f5f9; }
.seg-metric-lbl { font-size: 0.65rem; color: #475569; text-transform: uppercase; letter-spacing: 0.06em; }
.seg-strategy { background: rgba(255,255,255,0.03); border-radius: 10px; padding: 0.8rem; font-size: 0.78rem; color: #94a3b8; line-height: 1.6; }
.seg-strategy strong { color: #a5b4fc; }

/* ── Rec Cards ── */
.rec-item {
    background: linear-gradient(135deg, #0f1729, #0a1020);
    border: 1px solid #1e293b; border-radius: 12px;
    padding: 1rem 1.2rem; margin: 0.5rem 0;
    display: flex; align-items: center; gap: 14px;
    transition: all 0.25s;
}
.rec-item:hover { border-color: #6366f1; transform: translateX(6px); background: linear-gradient(135deg, #141f3a, #0f1729); }
.rec-rank-badge {
    width: 36px; height: 36px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 0.85rem; flex-shrink: 0;
}
.rec-info { flex: 1; }
.rec-name { font-size: 0.9rem; font-weight: 600; color: #f1f5f9; margin-bottom: 2px; }
.rec-score-bar { height: 4px; border-radius: 2px; background: #1e293b; margin-top: 6px; }
.rec-score-fill { height: 100%; border-radius: 2px; background: linear-gradient(90deg, #6366f1, #22d3ee); }
.rec-score-val { font-size: 0.75rem; color: #22d3ee; font-weight: 600; }

/* ── Prediction Result ── */
.pred-result {
    background: linear-gradient(135deg, #0f1729, #0a1020);
    border-radius: 18px; padding: 2rem; text-align: center;
    border: 1px solid #1e293b; position: relative; overflow: hidden;
}
.pred-segment { font-size: 2rem; font-weight: 900; margin: 0.5rem 0; }
.pred-advice { font-size: 0.9rem; color: #94a3b8; line-height: 1.7; max-width: 350px; margin: 0 auto; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #060b18 !important;
    border-right: 1px solid #0f1729 !important;
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem; }

/* ── Inputs ── */
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: #0f1729 !important; border: 1px solid #1e293b !important;
    color: #f1f5f9 !important; border-radius: 10px !important;
    font-size: 0.9rem !important;
}
.stSelectbox > div > div {
    background: #0f1729 !important; border: 1px solid #1e293b !important;
    border-radius: 10px !important; color: #f1f5f9 !important;
}
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 0.7rem 2rem !important;
    font-weight: 700 !important; font-size: 0.95rem !important;
    width: 100% !important; transition: all 0.25s !important;
    letter-spacing: 0.02em !important;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #818cf8, #6366f1) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.5) !important;
}
.stSlider > div > div > div { background: #6366f1 !important; }
div[data-testid="stTab"] button { color: #64748b !important; font-weight: 600 !important; }
div[data-testid="stTab"] button[aria-selected="true"] { color: #6366f1 !important; border-bottom-color: #6366f1 !important; }
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
hr { border-color: #1e293b !important; }
</style>
""", unsafe_allow_html=True)

# ── Load Models ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    with open("models/kmeans_model.pkl", "rb") as f: kmeans = pickle.load(f)
    with open("models/scaler.pkl", "rb") as f: scaler = pickle.load(f)
    with open("models/cluster_label_map.pkl", "rb") as f: cluster_label_map = pickle.load(f)
    item_sim_df = pd.read_pickle("models/item_sim_df.pkl")
    rfm = pd.read_csv("models/rfm_segmented.csv")
    return kmeans, scaler, cluster_label_map, item_sim_df, rfm

kmeans, scaler, cluster_label_map, item_sim_df, rfm = load_models()

COLOR_MAP = {
    "High-Value 🏆": "#4ade80",
    "Regular 🔄":    "#6366f1",
    "Occasional 💤": "#facc15",
    "At-Risk ⚠️":   "#f87171",
}
SEG_INFO = {
    "High-Value 🏆": {
        "pill_bg": "#052e16", "pill_color": "#4ade80",
        "icon": "👑", "icon_bg": "#052e16",
        "strategy": "<strong>VIP Treatment:</strong> Exclusive early access, personal account manager, loyalty multipliers, premium bundles & private sale invites.",
        "cta": "Retain & Upsell"
    },
    "Regular 🔄": {
        "pill_bg": "#1e1b4b", "pill_color": "#818cf8",
        "icon": "🔄", "icon_bg": "#1e1b4b",
        "strategy": "<strong>Growth Play:</strong> Cross-sell complementary categories, seasonal campaigns, referral rewards & subscription nudges.",
        "cta": "Grow & Expand"
    },
    "Occasional 💤": {
        "pill_bg": "#422006", "pill_color": "#fbbf24",
        "icon": "💡", "icon_bg": "#422006",
        "strategy": "<strong>Re-Engage:</strong> Flash sale alerts, limited-time discount codes, 'You left something behind' reminders & loyalty point bonuses.",
        "cta": "Activate & Engage"
    },
    "At-Risk ⚠️": {
        "pill_bg": "#450a0a", "pill_color": "#f87171",
        "icon": "🚨", "icon_bg": "#450a0a",
        "strategy": "<strong>Win-Back:</strong> Personalised 'We miss you' email, steep one-time discount, churn survey + free shipping offer.",
        "cta": "Rescue & Recover"
    },
}

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0a0f1e",
    font=dict(color="#94a3b8", family="Inter"),
    margin=dict(t=30, b=30, l=20, r=20),
    xaxis=dict(gridcolor="#0f1729", showgrid=True, zeroline=False),
    yaxis=dict(gridcolor="#0f1729", showgrid=True, zeroline=False),
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:1rem 0 1.5rem;">
  <div style="font-size:2.5rem;margin-bottom:0.5rem;">🛒</div>
  <div style="font-size:1.1rem;font-weight:800;color:#f1f5f9;">Shopper Spectrum</div>
  <div style="font-size:0.72rem;color:#475569;margin-top:3px;">AI-Powered Retail Intelligence</div>
</div>
""", unsafe_allow_html=True)

    page = st.radio("", ["🏠  Command Centre", "🎯  Product Recommender", "👥  Segment Explorer", "🔮  Live Predictor"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:1rem;">
  <div style="font-size:0.7rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.8rem;">Model Performance</div>
  <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
    <span style="font-size:0.78rem;color:#64748b;">Silhouette Score</span>
    <span style="font-size:0.78rem;font-weight:700;color:#4ade80;">0.6162</span>
  </div>
  <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
    <span style="font-size:0.78rem;color:#64748b;">Clusters (k)</span>
    <span style="font-size:0.78rem;font-weight:700;color:#a5b4fc;">4</span>
  </div>
  <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
    <span style="font-size:0.78rem;color:#64748b;">Algorithm</span>
    <span style="font-size:0.78rem;font-weight:700;color:#a5b4fc;">KMeans</span>
  </div>
  <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
    <span style="font-size:0.78rem;color:#64748b;">Recommender</span>
    <span style="font-size:0.78rem;font-weight:700;color:#a5b4fc;">Cosine Sim.</span>
  </div>
  <div style="display:flex;justify-content:space-between;">
    <span style="font-size:0.78rem;color:#64748b;">Products</span>
    <span style="font-size:0.78rem;font-weight:700;color:#a5b4fc;">500 items</span>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="margin-top:1.5rem;text-align:center;">
  <div style="font-size:0.68rem;color:#1e293b;">Built with Pandas · Scikit-learn · Plotly · Streamlit</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — COMMAND CENTRE
# ══════════════════════════════════════════════════════════════════════════════
if "Command" in page:

    # Hero
    st.markdown("""
<div class="hero-wrapper">
  <div class="hero-badge">⚡ AI-Powered · Real-Time · E-Commerce Analytics</div>
  <h1 class="hero-title">Know Your Customer.<br>Grow Your Revenue.</h1>
  <p class="hero-sub">
    Shopper Spectrum transforms raw transaction data into
    <span>actionable intelligence</span> — segmenting customers,
    predicting behaviour, and recommending products that actually convert.
  </p>
  <div class="hero-tags">
    <div class="hero-tag">📦 <span>541,909</span> Transactions Analysed</div>
    <div class="hero-tag">👥 <span>4,338</span> Customers Profiled</div>
    <div class="hero-tag">🌍 <span>37</span> Countries</div>
    <div class="hero-tag">🤖 <span>KMeans + Cosine Similarity</span></div>
    <div class="hero-tag">📅 <span>2022–2023</span> Dataset</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # KPI Cards
    seg_counts = rfm["Segment"].value_counts()
    total = len(rfm)
    hv = seg_counts.get("High-Value 🏆", 0)
    ar = seg_counts.get("At-Risk ⚠️", 0)
    avg_m = rfm["Monetary"].mean()
    avg_f = rfm["Frequency"].mean()

    st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-icon">👥</div>
    <div class="kpi-val">{total:,}</div>
    <div class="kpi-lbl">Total Customers</div>
    <div class="kpi-delta">↑ Fully Profiled</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">👑</div>
    <div class="kpi-val">{hv}</div>
    <div class="kpi-lbl">High-Value VIPs</div>
    <div class="kpi-delta">↑ Top Revenue Drivers</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">⚠️</div>
    <div class="kpi-val">{ar}</div>
    <div class="kpi-lbl">At-Risk Customers</div>
    <div class="kpi-delta" style="color:#f87171;">↓ Need Win-Back</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">💷</div>
    <div class="kpi-val">£{avg_m:,.0f}</div>
    <div class="kpi-lbl">Avg. Customer LTV</div>
    <div class="kpi-delta">↑ Lifetime Value</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">🔁</div>
    <div class="kpi-val">{avg_f:.1f}x</div>
    <div class="kpi-lbl">Avg. Order Frequency</div>
    <div class="kpi-delta">↑ Per Customer</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Key Insights
    st.markdown("""
<div class="section-wrap">
  <div class="section-eyebrow">✦ Data Intelligence</div>
  <div class="section-title">Key Business Insights</div>
  <div class="section-sub">Critical findings from 392,692 clean transactions</div>
</div>
<div class="insight-row">
  <div class="insight-card">
    <div class="insight-icon-wrap" style="background:#1e1b4b;">🇬🇧</div>
    <div class="insight-content">
      <div class="insight-title">Market Dominance</div>
      <div class="insight-val">91.4% UK</div>
      <div class="insight-desc">United Kingdom accounts for the vast majority of transactions — a key focus market for any campaign.</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="insight-icon-wrap" style="background:#052e16;">📈</div>
    <div class="insight-content">
      <div class="insight-title">Peak Season</div>
      <div class="insight-val">Q4 Revenue Spike</div>
      <div class="insight-desc">November sees the highest revenue surge — Black Friday & Christmas shopping drives 2.3× average monthly revenue.</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="insight-icon-wrap" style="background:#422006;">🕐</div>
    <div class="insight-content">
      <div class="insight-title">Golden Hours</div>
      <div class="insight-val">9 AM – 12 PM</div>
      <div class="insight-desc">Tues–Thurs mornings generate the highest transaction density. Ideal window for flash sales & push notifications.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Charts Row
    st.markdown("""
<div class="section-wrap">
  <div class="section-eyebrow">✦ Visual Analytics</div>
  <div class="section-title">Customer Intelligence Dashboard</div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        # Donut chart
        seg_df = rfm["Segment"].value_counts().reset_index()
        seg_df.columns = ["Segment", "Count"]
        seg_df["Pct"] = (seg_df["Count"] / seg_df["Count"].sum() * 100).round(1)
        fig = px.pie(seg_df, values="Count", names="Segment",
                     color="Segment", color_discrete_map=COLOR_MAP,
                     hole=0.65, template="plotly_dark")
        fig.update_traces(textfont_size=12, textfont_color="white",
                          textinfo="percent+label",
                          hovertemplate="<b>%{label}</b><br>%{value} customers<br>%{percent}<extra></extra>")
        fig.update_layout(**PLOT_LAYOUT, height=340,
                          showlegend=False,
                          annotations=[dict(text=f"<b>{total:,}</b><br><span style='font-size:10px'>Customers</span>",
                                           x=0.5, y=0.5, font_size=16, font_color="#f1f5f9",
                                           showarrow=False)])
        fig.update_layout(title=dict(text="Segment Distribution", font=dict(size=14, color="#f1f5f9"), x=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # RFM scatter
        rfm_s = rfm[rfm["Monetary"] < rfm["Monetary"].quantile(0.97)].copy()
        rfm_s["Size"] = np.sqrt(rfm_s["Monetary"]).clip(4, 30)
        fig2 = px.scatter(rfm_s, x="Recency", y="Frequency",
                          size="Size", color="Segment",
                          color_discrete_map=COLOR_MAP, opacity=0.75,
                          template="plotly_dark",
                          hover_data={"Monetary": ":,.0f", "Size": False},
                          labels={"Recency": "Recency (days)", "Frequency": "Orders"})
        fig2.update_layout(**PLOT_LAYOUT, height=340,
                           legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                       font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
                           title=dict(text="RFM Customer Map", font=dict(size=14, color="#f1f5f9"), x=0))
        st.plotly_chart(fig2, use_container_width=True)

    # Monetary box plot
    rfm_c = rfm[rfm["Monetary"] <= rfm["Monetary"].quantile(0.95)]
    fig3 = px.box(rfm_c, x="Segment", y="Monetary", color="Segment",
                  color_discrete_map=COLOR_MAP, template="plotly_dark",
                  labels={"Monetary": "Total Spend (£)", "Segment": ""},
                  points="outliers")
    fig3.update_layout(**PLOT_LAYOUT, height=320, showlegend=False,
                       title=dict(text="Spend Distribution by Segment", font=dict(size=14, color="#f1f5f9"), x=0))
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRODUCT RECOMMENDER
# ══════════════════════════════════════════════════════════════════════════════
elif "Recommender" in page:
    st.markdown("""
<div class="hero-wrapper">
  <div class="hero-badge">🤖 Item-Based Collaborative Filtering</div>
  <h1 class="hero-title" style="font-size:2.8rem;">Product Recommendation<br>Engine</h1>
  <p class="hero-sub">Select any product and instantly discover what customers who bought it also purchased — powered by <span>Cosine Similarity</span> across 500 top products.</p>
</div>
""", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.1, 1])

    with col_l:
        all_products = sorted(item_sim_df.index.tolist())
        default_idx = all_products.index("WHITE HANGING HEART T-LIGHT HOLDER") if "WHITE HANGING HEART T-LIGHT HOLDER" in all_products else 0

        st.markdown('<div class="section-wrap"><div class="section-eyebrow">✦ Configure</div><div class="section-title">Find Similar Products</div></div>', unsafe_allow_html=True)

        selected = st.selectbox("Choose a product from the catalogue", all_products, index=default_idx)
        top_n = st.slider("Number of recommendations", 3, 10, 5)
        show_chart = st.toggle("Show similarity bar chart", value=True)

        if st.button("🚀  Generate Recommendations"):
            similar = item_sim_df[selected].drop(selected).sort_values(ascending=False).head(top_n)

            st.markdown(f"""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:14px;padding:1.2rem;margin:1rem 0;">
  <div style="font-size:0.7rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;">Selected Product</div>
  <div style="font-size:1rem;font-weight:700;color:#a5b4fc;margin-top:0.3rem;">{selected}</div>
</div>
""", unsafe_allow_html=True)

            rank_colors = ["#facc15","#94a3b8","#fb923c","#6366f1","#22d3ee","#4ade80","#f472b6","#818cf8","#67e8f9","#86efac"]
            for rank, (prod, score) in enumerate(similar.items(), 1):
                fill_pct = int(score * 100)
                color = rank_colors[rank-1] if rank <= len(rank_colors) else "#6366f1"
                st.markdown(f"""
<div class="rec-item">
  <div class="rec-rank-badge" style="background:rgba(99,102,241,0.15);color:{color};">#{rank}</div>
  <div class="rec-info">
    <div class="rec-name">{prod}</div>
    <div class="rec-score-bar"><div class="rec-score-fill" style="width:{fill_pct}%;background:linear-gradient(90deg,{color},{color}88);"></div></div>
  </div>
  <div class="rec-score-val">{score:.4f}</div>
</div>
""", unsafe_allow_html=True)

            if show_chart:
                fig = go.Figure(go.Bar(
                    x=similar.values[::-1], y=[p[:35]+"…" if len(p)>35 else p for p in similar.index[::-1]],
                    orientation="h", marker=dict(
                        color=similar.values[::-1],
                        colorscale=[[0,"#334155"],[0.5,"#6366f1"],[1,"#22d3ee"]],
                        showscale=False),
                    text=[f"{v:.3f}" for v in similar.values[::-1]],
                    textposition="outside", textfont=dict(color="#94a3b8", size=10),
                    hovertemplate="<b>%{y}</b><br>Similarity: %{x:.4f}<extra></extra>"
                ))
                fig.update_layout(**PLOT_LAYOUT, height=max(250, top_n*45),
                                  xaxis_title="Cosine Similarity",
                                  title=dict(text="Similarity Scores", font=dict(size=13, color="#f1f5f9"), x=0))
                st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("""
<div class="section-wrap"><div class="section-eyebrow">✦ How It Works</div><div class="section-title">The Algorithm</div></div>
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:14px;padding:1.4rem;margin-bottom:1rem;">
""", unsafe_allow_html=True)

        steps = [
            ("01", "#6366f1", "Build Purchase Matrix", "Create a Customer × Product matrix tracking how many units each customer bought of each product."),
            ("02", "#22d3ee", "Compute Cosine Similarity", "Calculate pairwise cosine similarity between all product vectors — products frequently bought together score higher."),
            ("03", "#f472b6", "Rank & Return", "For the selected product, return the top-N most similar items ranked by similarity score (0→1)."),
        ]
        for num, color, title, desc in steps:
            st.markdown(f"""
<div style="display:flex;gap:12px;margin-bottom:1rem;padding-bottom:1rem;border-bottom:1px solid #1e293b;">
  <div style="width:32px;height:32px;border-radius:8px;background:{color}22;color:{color};font-weight:800;font-size:0.8rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{num}</div>
  <div>
    <div style="font-size:0.85rem;font-weight:700;color:#f1f5f9;margin-bottom:3px;">{title}</div>
    <div style="font-size:0.78rem;color:#64748b;line-height:1.5;">{desc}</div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Top products quick list
        st.markdown('<div class="section-wrap"><div class="section-eyebrow">✦ Quick Reference</div><div class="section-title">Most Connected Products</div><div class="section-sub">Products with the most cross-product similarity links</div></div>', unsafe_allow_html=True)
        top_connected = (item_sim_df > 0.3).sum().sort_values(ascending=False).head(8)
        for i, (prod, cnt) in enumerate(top_connected.items(), 1):
            short = prod[:40]+"…" if len(prod)>40 else prod
            pct = int(cnt/len(item_sim_df)*100)
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;padding:0.6rem 0;border-bottom:1px solid #0f1729;">
  <div style="font-size:0.75rem;font-weight:700;color:#475569;width:20px;">#{i}</div>
  <div style="flex:1;font-size:0.8rem;color:#94a3b8;">{short}</div>
  <div style="font-size:0.72rem;color:#6366f1;font-weight:600;">{cnt} links</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — SEGMENT EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
elif "Explorer" in page:
    st.markdown("""
<div class="hero-wrapper">
  <div class="hero-badge">📊 RFM Analysis · KMeans Clustering</div>
  <h1 class="hero-title" style="font-size:2.8rem;">Customer Segment<br>Explorer</h1>
  <p class="hero-sub">Deep-dive into each of the <span>4 behavioural segments</span> — understand who they are, what they spend, and exactly how to market to them.</p>
</div>
""", unsafe_allow_html=True)

    # Segment selector tabs
    seg_names = list(SEG_INFO.keys())
    tabs = st.tabs([s for s in seg_names])

    for tab, seg in zip(tabs, seg_names):
        with tab:
            info = SEG_INFO[seg]
            seg_data = rfm[rfm["Segment"] == seg]
            count = len(seg_data)
            avg_r = seg_data["Recency"].mean()
            avg_f = seg_data["Frequency"].mean()
            avg_m = seg_data["Monetary"].mean()
            color = COLOR_MAP[seg]

            c1, c2 = st.columns([1, 1.5])
            with c1:
                st.markdown(f"""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:16px;padding:1.5rem;margin-bottom:1rem;">
  <div style="font-size:3rem;margin-bottom:0.8rem;">{info['icon']}</div>
  <div style="font-size:1.5rem;font-weight:800;color:#f1f5f9;margin-bottom:0.5rem;">{seg}</div>
  <div style="display:inline-block;background:{info['pill_bg']};color:{info['pill_color']};border:1px solid {info['pill_color']}44;border-radius:50px;padding:4px 14px;font-size:0.75rem;font-weight:700;margin-bottom:1.2rem;">{info['cta']}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:1.2rem;">
    <div style="background:#060b18;border-radius:10px;padding:0.8rem;text-align:center;">
      <div style="font-size:1.2rem;font-weight:800;color:{color};">{avg_r:.0f}d</div>
      <div style="font-size:0.65rem;color:#475569;text-transform:uppercase;letter-spacing:0.06em;">Recency</div>
    </div>
    <div style="background:#060b18;border-radius:10px;padding:0.8rem;text-align:center;">
      <div style="font-size:1.2rem;font-weight:800;color:{color};">{avg_f:.1f}x</div>
      <div style="font-size:0.65rem;color:#475569;text-transform:uppercase;letter-spacing:0.06em;">Frequency</div>
    </div>
    <div style="background:#060b18;border-radius:10px;padding:0.8rem;text-align:center;">
      <div style="font-size:1.2rem;font-weight:800;color:{color};">£{avg_m:,.0f}</div>
      <div style="font-size:0.65rem;color:#475569;text-transform:uppercase;letter-spacing:0.06em;">Avg Spend</div>
    </div>
  </div>
  <div style="background:#060b18;border-radius:10px;padding:1rem;font-size:0.82rem;color:#94a3b8;line-height:1.7;">{info['strategy']}</div>
  <div style="margin-top:1rem;text-align:center;font-size:0.78rem;color:#475569;">{count} customers · {count/len(rfm)*100:.1f}% of base</div>
</div>
""", unsafe_allow_html=True)

            with c2:
                # Histogram for this segment
                fig = go.Figure()
                fig.add_trace(go.Histogram(
                    x=seg_data["Monetary"].clip(upper=seg_data["Monetary"].quantile(0.95)),
                    nbinsx=40, name="Spend",
                    marker=dict(color=color, opacity=0.8),
                    hovertemplate="£%{x:,.0f}<br>%{y} customers<extra></extra>"
                ))
                fig.update_layout(**PLOT_LAYOUT, height=220,
                                  xaxis_title="Total Spend (£)", yaxis_title="Customers",
                                  title=dict(text="Spend Distribution", font=dict(size=13, color="#f1f5f9"), x=0),
                                  showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

                # Recency vs frequency scatter for this segment
                fig2 = px.scatter(
                    seg_data[seg_data["Monetary"] < seg_data["Monetary"].quantile(0.97)],
                    x="Recency", y="Frequency",
                    size=np.sqrt(seg_data[seg_data["Monetary"] < seg_data["Monetary"].quantile(0.97)]["Monetary"].clip(1)).values,
                    color_discrete_sequence=[color], opacity=0.65, template="plotly_dark",
                    labels={"Recency":"Days Since Last Purchase","Frequency":"Number of Orders"},
                    size_max=20
                )
                fig2.update_layout(**PLOT_LAYOUT, height=240,
                                   title=dict(text="Recency vs Frequency", font=dict(size=13, color="#f1f5f9"), x=0),
                                   showlegend=False)
                st.plotly_chart(fig2, use_container_width=True)

    # Full comparison table
    st.markdown('<div class="section-wrap"><div class="section-eyebrow">✦ Full Comparison</div><div class="section-title">All Segments at a Glance</div></div>', unsafe_allow_html=True)
    profile = rfm.groupby("Segment").agg(
        Customers=("CustomerID","count"),
        Avg_Recency=("Recency","mean"),
        Avg_Frequency=("Frequency","mean"),
        Avg_Monetary=("Monetary","mean"),
        Total_Revenue=("Monetary","sum"),
    ).round(1).reset_index()
    profile["% of Base"] = (profile["Customers"]/profile["Customers"].sum()*100).round(1).astype(str) + "%"
    profile["Avg_Monetary"] = profile["Avg_Monetary"].apply(lambda x: f"£{x:,.0f}")
    profile["Total_Revenue"] = profile["Total_Revenue"].apply(lambda x: f"£{x:,.0f}")
    profile.columns = ["Segment","Customers","Avg Recency (days)","Avg Frequency","Avg Spend","Total Revenue","% of Base"]
    st.dataframe(profile.set_index("Segment"), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — LIVE PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
elif "Predictor" in page:
    st.markdown("""
<div class="hero-wrapper">
  <div class="hero-badge">🔮 Real-Time Prediction Engine</div>
  <h1 class="hero-title" style="font-size:2.8rem;">Predict Any Customer's<br>Segment Instantly</h1>
  <p class="hero-sub">Enter a customer's <span>Recency, Frequency & Monetary</span> values and our trained KMeans model will classify them in milliseconds — with full strategy recommendations.</p>
</div>
""", unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1.2, 1.2, 1])

    with col_l:
        st.markdown('<div class="section-wrap"><div class="section-eyebrow">✦ Input</div><div class="section-title">Customer RFM Values</div></div>', unsafe_allow_html=True)

        recency   = st.number_input("📅 Recency — Days since last purchase", 1, 730, 45, help="Lower = more recent = better")
        frequency = st.number_input("🔁 Frequency — Total number of orders", 1, 500, 8, help="Higher = more loyal")
        monetary  = st.number_input("💷 Monetary — Total spend in £", 1.0, 500000.0, 1200.0, step=100.0, help="Higher = more valuable")

        st.markdown("---")
        st.markdown("""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:1rem;margin-bottom:1rem;">
  <div style="font-size:0.72rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.8rem;">RFM Quick Reference</div>
  <div style="font-size:0.78rem;color:#64748b;line-height:2;">
    📅 <b style="color:#94a3b8;">Recency:</b> 1–30 days = Champion<br>
    🔁 <b style="color:#94a3b8;">Frequency:</b> 10+ orders = Loyal<br>
    💷 <b style="color:#94a3b8;">Monetary:</b> £1,000+ = High Value
  </div>
</div>
""", unsafe_allow_html=True)
        predict_btn = st.button("🔮  Predict My Segment")

    with col_m:
        st.markdown('<div class="section-wrap"><div class="section-eyebrow">✦ Result</div><div class="section-title">Prediction Output</div></div>', unsafe_allow_html=True)

        if predict_btn:
            X_scaled = scaler.transform([[recency, frequency, monetary]])
            cluster_id = kmeans.predict(X_scaled)[0]
            segment = cluster_label_map[cluster_id]
            info = SEG_INFO[segment]
            color = COLOR_MAP[segment]

            # Confidence: distance to centroid
            distances = kmeans.transform(X_scaled)[0]
            closest = distances.min()
            confidence = max(0, min(100, int((1 - closest / (distances.max() + 1e-9)) * 100)))

            st.markdown(f"""
<div class="pred-result">
  <div style="font-size:3rem;margin-bottom:0.5rem;">{info['icon']}</div>
  <div style="font-size:0.72rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;">Predicted Segment</div>
  <div class="pred-segment" style="color:{color};">{segment}</div>
  <div style="display:inline-block;background:{info['pill_bg']};color:{info['pill_color']};border:1px solid {info['pill_color']}44;border-radius:50px;padding:4px 16px;font-size:0.75rem;font-weight:700;margin-bottom:1rem;">{info['cta']}</div>
  <div style="margin-bottom:1rem;">
    <div style="font-size:0.7rem;color:#475569;margin-bottom:5px;">MODEL CONFIDENCE</div>
    <div style="background:#0f1729;border-radius:6px;height:8px;overflow:hidden;">
      <div style="width:{confidence}%;height:100%;background:linear-gradient(90deg,{color},{color}88);border-radius:6px;"></div>
    </div>
    <div style="font-size:0.75rem;color:{color};font-weight:700;margin-top:4px;">{confidence}%</div>
  </div>
  <div class="pred-advice">{info['strategy']}</div>
</div>
""", unsafe_allow_html=True)

            # Input summary
            st.markdown(f"""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:1rem;margin-top:1rem;">
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;text-align:center;">
    <div><div style="font-size:1rem;font-weight:800;color:#f1f5f9;">{recency}d</div><div style="font-size:0.65rem;color:#475569;text-transform:uppercase;">Recency</div></div>
    <div><div style="font-size:1rem;font-weight:800;color:#f1f5f9;">{frequency}x</div><div style="font-size:0.65rem;color:#475569;text-transform:uppercase;">Frequency</div></div>
    <div><div style="font-size:1rem;font-weight:800;color:#f1f5f9;">£{monetary:,.0f}</div><div style="font-size:0.65rem;color:#475569;text-transform:uppercase;">Monetary</div></div>
  </div>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="background:#0f1729;border:1px dashed #1e293b;border-radius:16px;padding:3rem;text-align:center;color:#334155;">
  <div style="font-size:3rem;margin-bottom:1rem;">🔮</div>
  <div style="font-size:1rem;font-weight:600;color:#475569;">Enter values and click<br>Predict to see results</div>
</div>
""", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-wrap"><div class="section-eyebrow">✦ Context</div><div class="section-title">Segment Benchmarks</div></div>', unsafe_allow_html=True)
        profile = rfm.groupby("Segment")[["Recency","Frequency","Monetary"]].mean().round(1)
        for seg_name, row in profile.iterrows():
            c = COLOR_MAP.get(seg_name, "#6366f1")
            is_current = predict_btn and seg_name == segment
            border = f"2px solid {c}" if is_current else "1px solid #1e293b"
            bg = f"background:{SEG_INFO[seg_name]['pill_bg']};" if is_current else ""
            st.markdown(f"""
<div style="background:#0f1729;{bg}border:{border};border-radius:12px;padding:0.9rem;margin-bottom:0.6rem;transition:all 0.3s;">
  <div style="font-size:0.82rem;font-weight:700;color:{c};margin-bottom:0.5rem;">{seg_name}</div>
  <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#64748b;">
    <span>R: <b style="color:#94a3b8;">{row['Recency']:.0f}d</b></span>
    <span>F: <b style="color:#94a3b8;">{row['Frequency']:.1f}x</b></span>
    <span>M: <b style="color:#94a3b8;">£{row['Monetary']:,.0f}</b></span>
  </div>
</div>
""", unsafe_allow_html=True)

        if predict_btn:
            # Radar chart
            from sklearn.preprocessing import MinMaxScaler
            mms = MinMaxScaler()
            normed = pd.DataFrame(mms.fit_transform(profile), columns=profile.columns, index=profile.index)
            user_n = mms.transform([[recency, frequency, monetary]])[0]
            cats = ["Recency","Frequency","Monetary"]
            fig = go.Figure()
            for s, row in normed.iterrows():
                c = COLOR_MAP.get(s, "#6366f1")
                v = row.tolist() + [row.tolist()[0]]
                fig.add_trace(go.Scatterpolar(r=v, theta=cats+[cats[0]], name=s,
                    line=dict(color=c, width=1.5), fill='toself', fillcolor=c, opacity=0.08))
            uv = user_n.tolist() + [user_n[0]]
            fig.add_trace(go.Scatterpolar(r=uv, theta=cats+[cats[0]], name="You",
                line=dict(color="#ffffff", width=2.5, dash="dot"),
                fill='toself', fillcolor="#ffffff", opacity=0.06))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              polar=dict(bgcolor="#0a0f1e", radialaxis=dict(gridcolor="#1e293b"),
                                         angularaxis=dict(gridcolor="#1e293b")),
                              legend=dict(font=dict(color="#64748b", size=9), bgcolor="rgba(0,0,0,0)"),
                              margin=dict(t=20,b=10,l=10,r=10), height=280,
                              title=dict(text="RFM Radar vs Segments", font=dict(size=12, color="#f1f5f9"), x=0))
            st.plotly_chart(fig, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;border-top:1px solid #0f1729;margin-top:3rem;">
  <div style="font-size:0.72rem;color:#1e293b;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;">
    Shopper Spectrum · AI-Powered Retail Intelligence · Built with Pandas · Scikit-learn · Plotly · Streamlit
  </div>
</div>
""", unsafe_allow_html=True)
