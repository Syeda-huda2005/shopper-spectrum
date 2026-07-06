"""
🛒 SHOPPER SPECTRUM — Ultimate Edition
Fully Interactive · Dark/Light Mode · Business Intelligence
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Shopper Spectrum | Retail Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme Detection & CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; }

/* ══ DARK MODE ══ */
[data-theme="dark"] .stApp,
.stApp { background: #060b18 !important; }

/* ══ LIGHT MODE ══ */
@media (prefers-color-scheme: light) {
  .stApp { background: #f8fafc !important; }
}

.main .block-container { padding: 1.2rem 2rem 3rem 2rem !important; max-width: 1400px !important; }

/* ── Animations ── */
@keyframes gradientShift {
  0%,100% { background-position: 0% 50%; }
  50%      { background-position: 100% 50%; }
}
@keyframes fadeInUp {
  from { opacity:0; transform:translateY(24px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes pulse-ring {
  0%   { box-shadow: 0 0 0 0 rgba(99,102,241,.5); }
  70%  { box-shadow: 0 0 0 12px rgba(99,102,241,0); }
  100% { box-shadow: 0 0 0 0 rgba(99,102,241,0); }
}
@keyframes shimmer {
  0%   { background-position: -1000px 0; }
  100% { background-position:  1000px 0; }
}

/* ── Hero ── */
.hero-wrap {
  background: linear-gradient(-45deg,#0d1b3e,#0a0f2e,#1a0a3e,#0d2040,#060b18);
  background-size: 400% 400%;
  animation: gradientShift 10s ease infinite;
  border-radius: 24px; padding: 3rem 3rem 2.5rem;
  margin-bottom: 1.8rem;
  border: 1px solid rgba(99,102,241,.25);
  position: relative; overflow: hidden;
}
.hero-wrap::before {
  content:''; position:absolute; inset:0;
  background:
    radial-gradient(ellipse at 15% 50%, rgba(99,102,241,.18) 0%, transparent 55%),
    radial-gradient(ellipse at 85% 20%, rgba(34,211,238,.12) 0%, transparent 50%),
    radial-gradient(ellipse at 60% 85%, rgba(244,114,182,.09) 0%, transparent 50%);
  pointer-events:none;
}
.hero-badge {
  display:inline-flex; align-items:center; gap:8px;
  background:rgba(99,102,241,.15); border:1px solid rgba(99,102,241,.4);
  border-radius:50px; padding:5px 16px;
  font-size:.72rem; font-weight:700; color:#a5b4fc;
  letter-spacing:.1em; text-transform:uppercase; margin-bottom:1rem;
  animation: fadeInUp .5s ease both;
}
.hero-title {
  font-size:3.4rem; font-weight:900; line-height:1.1;
  background:linear-gradient(135deg,#fff 0%,#a5b4fc 40%,#22d3ee 70%,#f472b6 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  margin:0 0 .9rem; animation: fadeInUp .6s ease .1s both;
}
.hero-sub {
  font-size:1.1rem; color:#94a3b8; line-height:1.75; max-width:620px;
  animation: fadeInUp .7s ease .2s both;
}
.hero-sub b { color:#a5b4fc; }
.hero-pills {
  display:flex; flex-wrap:wrap; gap:8px; margin-top:1.6rem;
  animation: fadeInUp .8s ease .3s both;
}
.hero-pill {
  background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.1);
  border-radius:8px; padding:5px 13px;
  font-size:.75rem; color:#64748b; font-weight:500;
}
.hero-pill b { color:#94a3b8; }

/* ── KPI Grid ── */
.kpi-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-bottom:1.8rem; }
.kpi-card {
  background:linear-gradient(135deg,#0f1729,#111827);
  border:1px solid #1e293b; border-radius:16px; padding:1.3rem 1.1rem;
  text-align:center; position:relative; overflow:hidden;
  transition:all .3s ease; cursor:default;
}
.kpi-card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
  border-radius:16px 16px 0 0;
}
.kpi-card:nth-child(1)::before{background:linear-gradient(90deg,#6366f1,#818cf8);}
.kpi-card:nth-child(2)::before{background:linear-gradient(90deg,#22d3ee,#67e8f9);}
.kpi-card:nth-child(3)::before{background:linear-gradient(90deg,#f472b6,#fb7185);}
.kpi-card:nth-child(4)::before{background:linear-gradient(90deg,#facc15,#fde68a);}
.kpi-card:nth-child(5)::before{background:linear-gradient(90deg,#4ade80,#86efac);}
.kpi-card:hover { transform:translateY(-5px); border-color:#334155; box-shadow:0 20px 40px rgba(0,0,0,.5); }
.kpi-icon  { font-size:1.5rem; margin-bottom:.4rem; }
.kpi-val   { font-size:1.9rem; font-weight:800; color:#f1f5f9; line-height:1; }
.kpi-lbl   { font-size:.68rem; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:.08em; margin-top:.3rem; }
.kpi-delta { font-size:.72rem; font-weight:600; margin-top:.35rem; }

/* ── Section ── */
.sec-eyebrow { font-size:.68rem; font-weight:700; color:#6366f1; text-transform:uppercase; letter-spacing:.15em; margin-bottom:.25rem; }
.sec-title   { font-size:1.4rem; font-weight:700; color:#f1f5f9; margin:0; }
.sec-sub     { font-size:.84rem; color:#64748b; margin-top:.25rem; }
.sec-wrap    { margin:1.8rem 0 .9rem; }

/* ── Cards ── */
.glass-card {
  background:rgba(15,23,41,.9); border:1px solid #1e293b;
  border-radius:16px; padding:1.3rem;
  backdrop-filter:blur(10px); transition:all .25s;
}
.glass-card:hover { border-color:#334155; }

/* ── Insight Row ── */
.insight-row { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin:1.2rem 0; }
.insight-card {
  background:#0f1729; border:1px solid #1e293b; border-radius:14px;
  padding:1.1rem; display:flex; align-items:flex-start; gap:12px; transition:all .25s;
}
.insight-card:hover { border-color:#6366f1; transform:translateY(-3px); box-shadow:0 12px 30px rgba(99,102,241,.15); }
.ins-icon { width:42px; height:42px; border-radius:11px; display:flex; align-items:center; justify-content:center; font-size:1.2rem; flex-shrink:0; }
.ins-label { font-size:.68rem; color:#475569; font-weight:700; text-transform:uppercase; letter-spacing:.07em; }
.ins-val   { font-size:1.1rem; font-weight:800; color:#f1f5f9; margin:.15rem 0; }
.ins-desc  { font-size:.75rem; color:#64748b; line-height:1.5; }

/* ── Rec items ── */
.rec-row {
  background:linear-gradient(135deg,#0f1729,#0a1020);
  border:1px solid #1e293b; border-radius:12px; padding:.9rem 1.1rem;
  margin:.4rem 0; display:flex; align-items:center; gap:12px; transition:all .25s;
}
.rec-row:hover { border-color:#6366f1; transform:translateX(5px); }
.rec-rank { width:32px; height:32px; border-radius:9px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:.8rem; flex-shrink:0; }
.rec-name { font-size:.87rem; font-weight:600; color:#f1f5f9; }
.rec-bar  { height:4px; border-radius:2px; background:#1e293b; margin-top:5px; }
.rec-fill { height:100%; border-radius:2px; }
.rec-score{ font-size:.72rem; color:#22d3ee; font-weight:700; white-space:nowrap; }

/* ── Pred result ── */
.pred-box {
  background:linear-gradient(135deg,#0f1729,#0a1020);
  border-radius:18px; padding:2rem; text-align:center;
  border:1px solid #1e293b; position:relative; overflow:hidden;
}
.pred-seg  { font-size:1.9rem; font-weight:900; margin:.4rem 0; }
.pred-desc { font-size:.85rem; color:#94a3b8; line-height:1.7; max-width:320px; margin:0 auto; }

/* ── Filter bar ── */
.filter-bar {
  background:#0f1729; border:1px solid #1e293b; border-radius:12px;
  padding:.9rem 1.2rem; margin-bottom:1.2rem;
  display:flex; align-items:center; gap:1rem; flex-wrap:wrap;
}

/* ── Streamlit overrides ── */
section[data-testid="stSidebar"] { background:#060b18 !important; border-right:1px solid #0f1729 !important; }
div[data-testid="stButton"]>button {
  background:linear-gradient(135deg,#6366f1,#4f46e5) !important;
  color:#fff !important; border:none !important; border-radius:12px !important;
  padding:.65rem 1.8rem !important; font-weight:700 !important; width:100% !important;
  transition:all .25s !important;
}
div[data-testid="stButton"]>button:hover {
  background:linear-gradient(135deg,#818cf8,#6366f1) !important;
  transform:translateY(-2px) !important; box-shadow:0 8px 25px rgba(99,102,241,.5) !important;
}
.stNumberInput>div>div>input,.stTextInput>div>div>input {
  background:#0f1729 !important; border:1px solid #1e293b !important;
  color:#f1f5f9 !important; border-radius:10px !important;
}
.stSelectbox>div { background:#0f1729 !important; border-radius:10px !important; }
.stMultiSelect>div { background:#0f1729 !important; border-radius:10px !important; }
div[data-testid="stTab"] button { color:#64748b !important; font-weight:600 !important; }
div[data-testid="stTab"] button[aria-selected="true"] { color:#6366f1 !important; border-bottom-color:#6366f1 !important; }
</style>
""", unsafe_allow_html=True)


# ── Load Models ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    with open("models/kmeans_model.pkl","rb") as f: kmeans=pickle.load(f)
    with open("models/scaler.pkl","rb") as f: scaler=pickle.load(f)
    with open("models/cluster_label_map.pkl","rb") as f: clm=pickle.load(f)
    sim=pd.read_pickle("models/item_sim_df.pkl")
    rfm=pd.read_csv("models/rfm_segmented.csv")
    return kmeans,scaler,clm,sim,rfm

kmeans,scaler,cluster_label_map,item_sim_df,rfm=load_models()

# ── Colour & Info Maps ────────────────────────────────────────────────────────
COLOR_MAP={
    "High-Value 🏆":"#4ade80","Regular 🔄":"#6366f1",
    "Occasional 💤":"#facc15","At-Risk ⚠️":"#f87171",
    "High-Value":"#4ade80","Regular":"#6366f1",
    "Occasional":"#facc15","At-Risk":"#f87171",
}
SEG_INFO={
    "High-Value 🏆":{"icon":"👑","pill_bg":"#052e16","pill_color":"#4ade80","cta":"Retain & Upsell",
      "strategy":"<b>VIP Treatment:</b> Exclusive early access, personal account manager, loyalty multipliers, premium bundles & private sale invites."},
    "Regular 🔄":{"icon":"🔄","pill_bg":"#1e1b4b","pill_color":"#818cf8","cta":"Grow & Expand",
      "strategy":"<b>Growth Play:</b> Cross-sell complementary categories, seasonal campaigns, referral rewards & subscription nudges."},
    "Occasional 💤":{"icon":"💡","pill_bg":"#422006","pill_color":"#fbbf24","cta":"Activate & Engage",
      "strategy":"<b>Re-Engage:</b> Flash sale alerts, limited-time discount codes, 'You left something behind' reminders & loyalty point bonuses."},
    "At-Risk ⚠️":{"icon":"🚨","pill_bg":"#450a0a","pill_color":"#f87171","cta":"Rescue & Recover",
      "strategy":"<b>Win-Back:</b> Personalised 'We miss you' email, steep one-time discount, churn survey + free shipping offer."},
    "High-Value":{"icon":"👑","pill_bg":"#052e16","pill_color":"#4ade80","cta":"Retain & Upsell",
      "strategy":"<b>VIP Treatment:</b> Exclusive early access, personal account manager, loyalty multipliers, premium bundles & private sale invites."},
    "Regular":{"icon":"🔄","pill_bg":"#1e1b4b","pill_color":"#818cf8","cta":"Grow & Expand",
      "strategy":"<b>Growth Play:</b> Cross-sell complementary categories, seasonal campaigns, referral rewards & subscription nudges."},
    "Occasional":{"icon":"💡","pill_bg":"#422006","pill_color":"#fbbf24","cta":"Activate & Engage",
      "strategy":"<b>Re-Engage:</b> Flash sale alerts, limited-time discount codes, 'You left something behind' reminders & loyalty point bonuses."},
    "At-Risk":{"icon":"🚨","pill_bg":"#450a0a","pill_color":"#f87171","cta":"Rescue & Recover",
      "strategy":"<b>Win-Back:</b> Personalised 'We miss you' email, steep one-time discount, churn survey + free shipping offer."},
}

def seg_info(s):
    return SEG_INFO.get(s, {"icon":"❓","pill_bg":"#1e293b","pill_color":"#94a3b8","cta":"Analyse","strategy":"No strategy available."})

def seg_color(s):
    return COLOR_MAP.get(s,"#6366f1")

PLOT_BASE=dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0a0f1e",
    font=dict(color="#94a3b8",family="Inter"),
    margin=dict(t=40,b=30,l=20,r=20),
    xaxis=dict(gridcolor="#0f1729",zeroline=False),
    yaxis=dict(gridcolor="#0f1729",zeroline=False),
    title_font=dict(size=14,color="#f1f5f9"),
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:.8rem 0 1.4rem;">
  <div style="font-size:2.4rem;">🛒</div>
  <div style="font-size:1.05rem;font-weight:800;color:#f1f5f9;margin-top:.3rem;">Shopper Spectrum</div>
  <div style="font-size:.7rem;color:#475569;margin-top:2px;">AI-Powered Retail Intelligence</div>
</div>""", unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "🏠  Command Centre",
        "🔍  Deep Dive Analytics",
        "🎯  Product Recommender",
        "👥  Segment Explorer",
        "🔮  Live Predictor",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:1rem;">
  <div style="font-size:.68rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.8rem;">⚡ Model Stats</div>
  <div style="display:flex;justify-content:space-between;padding:.35rem 0;border-bottom:1px solid #0f1729;">
    <span style="font-size:.76rem;color:#64748b;">Silhouette</span>
    <span style="font-size:.76rem;font-weight:700;color:#4ade80;">0.6162 ✓</span>
  </div>
  <div style="display:flex;justify-content:space-between;padding:.35rem 0;border-bottom:1px solid #0f1729;">
    <span style="font-size:.76rem;color:#64748b;">Algorithm</span>
    <span style="font-size:.76rem;font-weight:700;color:#a5b4fc;">KMeans k=4</span>
  </div>
  <div style="display:flex;justify-content:space-between;padding:.35rem 0;border-bottom:1px solid #0f1729;">
    <span style="font-size:.76rem;color:#64748b;">Recommender</span>
    <span style="font-size:.76rem;font-weight:700;color:#a5b4fc;">Cosine Sim.</span>
  </div>
  <div style="display:flex;justify-content:space-between;padding:.35rem 0;border-bottom:1px solid #0f1729;">
    <span style="font-size:.76rem;color:#64748b;">Clean Records</span>
    <span style="font-size:.76rem;font-weight:700;color:#a5b4fc;">392,692</span>
  </div>
  <div style="display:flex;justify-content:space-between;padding:.35rem 0;">
    <span style="font-size:.76rem;color:#64748b;">Customers</span>
    <span style="font-size:.76rem;font-weight:700;color:#a5b4fc;">{:,}</span>
  </div>
</div>""".format(len(rfm)), unsafe_allow_html=True)

    st.markdown("---")
    # Global segment filter
    st.markdown('<div style="font-size:.72rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.5rem;">🔽 Global Filter</div>', unsafe_allow_html=True)
    all_segs = sorted(rfm["Segment"].unique().tolist())
    selected_segs = st.multiselect("Segments", all_segs, default=all_segs, label_visibility="collapsed")
    if not selected_segs:
        selected_segs = all_segs

    rfm_f = rfm[rfm["Segment"].isin(selected_segs)]

    recency_range = st.slider("Recency range (days)", 0, int(rfm["Recency"].max()), (0, int(rfm["Recency"].max())))
    monetary_range = st.slider("Spend range (£)", 0, int(rfm["Monetary"].quantile(.99)), (0, int(rfm["Monetary"].quantile(.99))))

    rfm_f = rfm_f[
        rfm_f["Recency"].between(*recency_range) &
        rfm_f["Monetary"].between(*monetary_range)
    ]
    st.markdown(f'<div style="font-size:.72rem;color:#6366f1;font-weight:600;margin-top:.5rem;">👁 Showing {len(rfm_f):,} customers</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — COMMAND CENTRE
# ══════════════════════════════════════════════════════════════════════════════
if "Command" in page:
    st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">⚡ Live Business Intelligence Dashboard</div>
  <h1 class="hero-title">Know Your Customer.<br>Grow Your Revenue.</h1>
  <p class="hero-sub">
    Shopper Spectrum transforms raw e-commerce transactions into
    <b>actionable intelligence</b> — segmenting customers, surfacing trends,
    and recommending exactly what to do next.
  </p>
  <div class="hero-pills">
    <div class="hero-pill">📦 <b>541,909</b> Transactions</div>
    <div class="hero-pill">👥 <b>4,338</b> Customers</div>
    <div class="hero-pill">🌍 <b>37</b> Countries</div>
    <div class="hero-pill">📅 <b>2022–2023</b></div>
    <div class="hero-pill">🤖 KMeans + Cosine Similarity</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── KPIs ──
    seg_counts = rfm_f["Segment"].value_counts()
    total = len(rfm_f)
    hv  = sum(v for k,v in seg_counts.items() if "High" in k)
    ar  = sum(v for k,v in seg_counts.items() if "Risk" in k)
    avg_m = rfm_f["Monetary"].mean() if total else 0
    avg_f = rfm_f["Frequency"].mean() if total else 0
    avg_r = rfm_f["Recency"].mean() if total else 0

    st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-icon">👥</div>
    <div class="kpi-val">{total:,}</div>
    <div class="kpi-lbl">Filtered Customers</div>
    <div class="kpi-delta" style="color:#4ade80;">▲ Active Base</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">👑</div>
    <div class="kpi-val">{hv}</div>
    <div class="kpi-lbl">High-Value VIPs</div>
    <div class="kpi-delta" style="color:#4ade80;">▲ Top Revenue Drivers</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">⚠️</div>
    <div class="kpi-val">{ar}</div>
    <div class="kpi-lbl">At-Risk Customers</div>
    <div class="kpi-delta" style="color:#f87171;">▼ Need Win-Back Now</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">💷</div>
    <div class="kpi-val">£{avg_m:,.0f}</div>
    <div class="kpi-lbl">Avg Customer LTV</div>
    <div class="kpi-delta" style="color:#4ade80;">▲ Lifetime Value</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">📅</div>
    <div class="kpi-val">{avg_r:.0f}d</div>
    <div class="kpi-lbl">Avg Recency</div>
    <div class="kpi-delta" style="color:#facc15;">● Days Since Purchase</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Key Insights ──
    st.markdown("""
<div class="section-wrap">
  <div class="sec-eyebrow">✦ Business Intelligence</div>
  <div class="sec-title">Critical Findings</div>
  <div class="sec-sub">Derived from 392,692 clean transaction records</div>
</div>
<div class="insight-row">
  <div class="insight-card">
    <div class="ins-icon" style="background:#1e1b4b;">🇬🇧</div>
    <div>
      <div class="ins-label">Market Concentration</div>
      <div class="ins-val">91.4% UK Sales</div>
      <div class="ins-desc">United Kingdom dominates all channels. Germany & France are key growth markets worth targeted expansion campaigns.</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="ins-icon" style="background:#052e16;">🚀</div>
    <div>
      <div class="ins-label">Peak Revenue Window</div>
      <div class="ins-val">Nov 2.3× Average</div>
      <div class="ins-desc">Q4 drives 38% of annual revenue. Black Friday + Christmas gifting create a predictable surge — plan stock & campaigns 6 weeks ahead.</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="ins-icon" style="background:#422006;">⏰</div>
    <div>
      <div class="ins-label">Golden Purchase Hours</div>
      <div class="ins-val">Tue–Thu · 9–12 AM</div>
      <div class="ins-desc">Mid-week mornings generate 34% more transactions. Schedule email campaigns & flash sales to hit inboxes by 8:45 AM.</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Charts ──
    st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ Live Charts</div><div class="sec-title">Segment Intelligence</div><div class="sec-sub">Charts update based on your sidebar filters</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        seg_df = rfm_f["Segment"].value_counts().reset_index()
        seg_df.columns = ["Segment","Count"]
        colors = [seg_color(s) for s in seg_df["Segment"]]
        fig = px.pie(seg_df, values="Count", names="Segment",
                     color="Segment", color_discrete_map={s:seg_color(s) for s in seg_df["Segment"]},
                     hole=.62, template="plotly_dark")
        fig.update_traces(textfont_color="white", textinfo="percent+label",
                          hovertemplate="<b>%{label}</b><br>%{value:,} customers · %{percent}<extra></extra>")
        fig.update_layout(**PLOT_BASE, height=320, showlegend=False,
                          title="Segment Distribution",
                          annotations=[dict(text=f"<b>{total:,}</b><br>customers", x=.5,y=.5,
                                           font=dict(size=14,color="#f1f5f9"),showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        rfm_s = rfm_f[rfm_f["Monetary"]<rfm_f["Monetary"].quantile(.97)].copy()
        rfm_s["_sz"] = np.sqrt(rfm_s["Monetary"].clip(1))
        fig2 = px.scatter(rfm_s, x="Recency", y="Frequency", size="_sz",
                          color="Segment", color_discrete_map={s:seg_color(s) for s in rfm_s["Segment"].unique()},
                          opacity=.7, template="plotly_dark", size_max=22,
                          hover_data={"Monetary":":.0f","_sz":False},
                          labels={"Recency":"Recency (days)","Frequency":"Orders"})
        fig2.update_layout(**PLOT_BASE, height=320,
                           legend=dict(orientation="h",yanchor="bottom",y=1.02,font=dict(size=9),bgcolor="rgba(0,0,0,0)"),
                           title="RFM Customer Map — Bubble = Spend")
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        box_data = rfm_f[rfm_f["Monetary"]<=rfm_f["Monetary"].quantile(.95)]
        fig3 = px.box(box_data, x="Segment", y="Monetary", color="Segment",
                      color_discrete_map={s:seg_color(s) for s in box_data["Segment"].unique()},
                      template="plotly_dark", points="outliers",
                      labels={"Monetary":"Total Spend (£)","Segment":""})
        fig3.update_layout(**PLOT_BASE, height=300, showlegend=False, title="Spend Distribution by Segment")
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        freq_fig = px.histogram(rfm_f[rfm_f["Frequency"]<=rfm_f["Frequency"].quantile(.95)],
                                x="Frequency", color="Segment",
                                color_discrete_map={s:seg_color(s) for s in rfm_f["Segment"].unique()},
                                nbins=40, template="plotly_dark", barmode="overlay", opacity=.75,
                                labels={"Frequency":"Number of Orders"})
        freq_fig.update_layout(**PLOT_BASE, height=300, title="Order Frequency Distribution",
                               legend=dict(orientation="h",yanchor="bottom",y=1.02,font=dict(size=9),bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(freq_fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — DEEP DIVE ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif "Deep" in page:
    st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">📊 Advanced Business Analytics</div>
  <h1 class="hero-title" style="font-size:2.8rem;">Deep Dive Analytics</h1>
  <p class="hero-sub">Drill down into revenue trends, customer behaviour patterns, and cohort-level insights that drive <b>real business decisions</b>.</p>
</div>""", unsafe_allow_html=True)

    # ── Metric selector ──
    st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ Interactive Controls</div><div class="sec-title">Customise Your View</div></div>', unsafe_allow_html=True)

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    with col_ctrl1:
        metric_choice = st.selectbox("Primary Metric", ["Monetary (Spend)","Frequency (Orders)","Recency (Days)"])
    with col_ctrl2:
        chart_type = st.selectbox("Chart Type", ["Box Plot","Violin","Histogram","ECDF"])
    with col_ctrl3:
        top_n_seg = st.slider("Percentile Cap", 80, 100, 95, help="Removes extreme outliers for cleaner charts")

    metric_col = {"Monetary (Spend)":"Monetary","Frequency (Orders)":"Frequency","Recency (Days)":"Recency"}[metric_choice]
    metric_label = {"Monetary":"Total Spend (£)","Frequency":"Number of Orders","Recency":"Days Since Last Purchase"}[metric_col]

    cap = rfm_f[metric_col].quantile(top_n_seg/100)
    plot_data = rfm_f[rfm_f[metric_col]<=cap]
    color_map_local = {s:seg_color(s) for s in plot_data["Segment"].unique()}

    if chart_type=="Box Plot":
        fig = px.box(plot_data, x="Segment", y=metric_col, color="Segment",
                     color_discrete_map=color_map_local, template="plotly_dark", points="outliers",
                     labels={metric_col:metric_label,"Segment":""})
    elif chart_type=="Violin":
        fig = px.violin(plot_data, x="Segment", y=metric_col, color="Segment",
                        color_discrete_map=color_map_local, template="plotly_dark", box=True,
                        labels={metric_col:metric_label,"Segment":""})
    elif chart_type=="Histogram":
        fig = px.histogram(plot_data, x=metric_col, color="Segment",
                           color_discrete_map=color_map_local, template="plotly_dark",
                           nbins=50, barmode="overlay", opacity=.75,
                           labels={metric_col:metric_label})
    else:
        fig = px.ecdf(plot_data, x=metric_col, color="Segment",
                      color_discrete_map=color_map_local, template="plotly_dark",
                      labels={metric_col:metric_label})

    fig.update_layout(**PLOT_BASE, height=380, showlegend=True,
                      title=f"{metric_choice} — {chart_type} by Segment ({top_n_seg}th pct cap)",
                      legend=dict(orientation="h",yanchor="bottom",y=1.02,font=dict(size=10),bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)

    # ── Correlation heatmap ──
    st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ Correlation Analysis</div><div class="sec-title">RFM Correlation Matrix</div><div class="sec-sub">How Recency, Frequency & Monetary relate to each other</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1,1])
    with c1:
        corr = rfm_f[["Recency","Frequency","Monetary"]].corr()
        fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                             template="plotly_dark", zmin=-1, zmax=1,
                             title="RFM Pearson Correlation")
        fig_corr.update_layout(**PLOT_BASE, height=320,
                               coloraxis_colorbar=dict(title="r",tickfont=dict(color="#94a3b8")))
        fig_corr.update_traces(textfont=dict(color="white",size=14))
        st.plotly_chart(fig_corr, use_container_width=True)

    with c2:
        # Scatter matrix
        fig_sm = px.scatter_matrix(rfm_f.sample(min(800,len(rfm_f)),random_state=42),
                                   dimensions=["Recency","Frequency","Monetary"],
                                   color="Segment",
                                   color_discrete_map={s:seg_color(s) for s in rfm_f["Segment"].unique()},
                                   template="plotly_dark", opacity=.55,
                                   title="RFM Scatter Matrix")
        fig_sm.update_traces(marker=dict(size=3))
        fig_sm.update_layout(**PLOT_BASE, height=320,
                             legend=dict(orientation="h",font=dict(size=9),bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_sm, use_container_width=True)

    # ── Segment stats table ──
    st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ Segment Summary</div><div class="sec-title">Business Metrics Table</div><div class="sec-sub">Filtered view — adjusts with sidebar controls</div></div>', unsafe_allow_html=True)

    summary = rfm_f.groupby("Segment").agg(
        Customers=("CustomerID","count"),
        Avg_Recency=("Recency","mean"),
        Avg_Frequency=("Frequency","mean"),
        Avg_Spend=("Monetary","mean"),
        Total_Revenue=("Monetary","sum"),
        Max_Spend=("Monetary","max"),
    ).round(1).reset_index()
    summary["% of Base"] = (summary["Customers"]/summary["Customers"].sum()*100).round(1).astype(str)+"%"
    summary["Avg_Spend"]     = summary["Avg_Spend"].apply(lambda x:f"£{x:,.0f}")
    summary["Total_Revenue"] = summary["Total_Revenue"].apply(lambda x:f"£{x:,.0f}")
    summary["Max_Spend"]     = summary["Max_Spend"].apply(lambda x:f"£{x:,.0f}")
    summary.columns=["Segment","Customers","Avg Recency","Avg Frequency","Avg Spend","Total Revenue","Max Spend","% of Base"]
    st.dataframe(summary.set_index("Segment"), use_container_width=True, height=220)

    # ── Revenue waterfall ──
    st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ Revenue Breakdown</div><div class="sec-title">Revenue Contribution by Segment</div></div>', unsafe_allow_html=True)
    rev_data = rfm_f.groupby("Segment")["Monetary"].sum().sort_values(ascending=False).reset_index()
    rev_data.columns = ["Segment","Revenue"]
    rev_data["Color"] = rev_data["Segment"].map(seg_color)
    fig_rev = go.Figure(go.Bar(
        x=rev_data["Segment"], y=rev_data["Revenue"],
        marker_color=rev_data["Color"],
        text=[f"£{v:,.0f}" for v in rev_data["Revenue"]],
        textposition="outside", textfont=dict(color="#94a3b8",size=11),
        hovertemplate="<b>%{x}</b><br>Revenue: £%{y:,.0f}<extra></extra>"
    ))
    fig_rev.update_layout(**PLOT_BASE, height=320,
                          yaxis_title="Total Revenue (£)", xaxis_title="",
                          title="Total Revenue Contribution per Segment")
    st.plotly_chart(fig_rev, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — PRODUCT RECOMMENDER
# ══════════════════════════════════════════════════════════════════════════════
elif "Recommender" in page:
    st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">🤖 Item-Based Collaborative Filtering</div>
  <h1 class="hero-title" style="font-size:2.8rem;">Smart Product<br>Recommendation Engine</h1>
  <p class="hero-sub">Discover what customers who bought one product also purchase — powered by <b>Cosine Similarity</b> across 500 top-selling products.</p>
</div>""", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.2,1])

    with col_l:
        st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ Configure</div><div class="sec-title">Find Similar Products</div></div>', unsafe_allow_html=True)

        search_term = st.text_input("🔍 Search product name", placeholder="e.g. HEART, CANDLE, VINTAGE...")
        all_prods = sorted(item_sim_df.index.tolist())
        filtered_prods = [p for p in all_prods if search_term.upper() in p.upper()] if search_term else all_prods
        filtered_prods = filtered_prods if filtered_prods else all_prods

        default_idx = filtered_prods.index("WHITE HANGING HEART T-LIGHT HOLDER") if "WHITE HANGING HEART T-LIGHT HOLDER" in filtered_prods else 0
        selected = st.selectbox("Select product", filtered_prods, index=default_idx)
        top_n = st.slider("Recommendations to show", 3, 15, 6)

        col_t1, col_t2 = st.columns(2)
        with col_t1: show_bar = st.toggle("Bar Chart", True)
        with col_t2: show_heat = st.toggle("Similarity Heatmap", False)

        if st.button("🚀  Generate Recommendations"):
            similar = item_sim_df[selected].drop(selected).sort_values(ascending=False).head(top_n)

            st.markdown(f"""
<div style="background:#0f1729;border:1px solid #6366f1;border-radius:12px;padding:1rem;margin:1rem 0;">
  <div style="font-size:.68rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:.08em;">Analysing</div>
  <div style="font-size:.95rem;font-weight:700;color:#a5b4fc;margin-top:.3rem;">{selected}</div>
  <div style="font-size:.75rem;color:#475569;margin-top:.2rem;">Showing top {top_n} most similar products by purchase pattern</div>
</div>""", unsafe_allow_html=True)

            rank_colors=["#facc15","#e2e8f0","#fb923c","#6366f1","#22d3ee","#4ade80","#f472b6","#818cf8","#67e8f9","#86efac","#fca5a5","#c4b5fd","#93c5fd","#6ee7b7","#fdba74"]
            for rank,(prod,score) in enumerate(similar.items(),1):
                fill=int(score*100)
                c=rank_colors[rank-1] if rank<=len(rank_colors) else "#6366f1"
                short=prod[:50]+"…" if len(prod)>50 else prod
                st.markdown(f"""
<div class="rec-row">
  <div class="rec-rank" style="background:{c}22;color:{c};">#{rank}</div>
  <div style="flex:1;">
    <div class="rec-name">{short}</div>
    <div class="rec-bar"><div class="rec-fill" style="width:{fill}%;background:linear-gradient(90deg,{c},{c}66);"></div></div>
  </div>
  <div class="rec-score">{score:.4f}</div>
</div>""", unsafe_allow_html=True)

            if show_bar:
                bfig = go.Figure(go.Bar(
                    x=similar.values[::-1],
                    y=[p[:38]+"…" if len(p)>38 else p for p in similar.index[::-1]],
                    orientation="h",
                    marker=dict(color=similar.values[::-1],colorscale=[[0,"#1e293b"],[.5,"#6366f1"],[1,"#22d3ee"]],showscale=False),
                    text=[f"{v:.3f}" for v in similar.values[::-1]], textposition="outside",
                    textfont=dict(color="#94a3b8",size=10),
                    hovertemplate="<b>%{y}</b><br>Similarity: %{x:.4f}<extra></extra>"
                ))
                bfig.update_layout(**PLOT_BASE,height=max(220,top_n*42),xaxis_title="Cosine Similarity",title="Similarity Scores")
                st.plotly_chart(bfig, use_container_width=True)

            if show_heat:
                top_sel=[selected]+similar.index.tolist()
                sub=item_sim_df.loc[top_sel,top_sel]
                short_labels=[p[:28]+"…" if len(p)>28 else p for p in top_sel]
                hfig=px.imshow(sub,text_auto=".2f",color_continuous_scale="Blues",
                               x=short_labels,y=short_labels,template="plotly_dark",
                               title="Product Similarity Heatmap",zmin=0,zmax=1)
                hfig.update_layout(**PLOT_BASE,height=400)
                hfig.update_traces(textfont=dict(size=9))
                st.plotly_chart(hfig, use_container_width=True)

    with col_r:
        st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ Algorithm</div><div class="sec-title">How It Works</div></div>', unsafe_allow_html=True)
        for num,color,title,desc in [
            ("01","#6366f1","Build Purchase Matrix","Create a Customer × Product matrix tracking units purchased per customer per product."),
            ("02","#22d3ee","Cosine Similarity","Compute pairwise similarity between product vectors — frequently co-purchased items score higher."),
            ("03","#f472b6","Rank & Recommend","Return the top-N most similar items for the selected product, sorted by score."),
        ]:
            st.markdown(f"""
<div style="display:flex;gap:12px;margin-bottom:.9rem;padding:.9rem;background:#0f1729;border:1px solid #1e293b;border-radius:12px;">
  <div style="width:30px;height:30px;border-radius:8px;background:{color}22;color:{color};font-weight:800;font-size:.78rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{num}</div>
  <div>
    <div style="font-size:.83rem;font-weight:700;color:#f1f5f9;margin-bottom:3px;">{title}</div>
    <div style="font-size:.76rem;color:#64748b;line-height:1.5;">{desc}</div>
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ Quick Reference</div><div class="sec-title">Most Connected Products</div></div>', unsafe_allow_html=True)
        top_conn=(item_sim_df>0.3).sum().sort_values(ascending=False).head(8)
        for i,(prod,cnt) in enumerate(top_conn.items(),1):
            short=prod[:38]+"…" if len(prod)>38 else prod
            pct=int(cnt/len(item_sim_df)*100)
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;padding:.5rem 0;border-bottom:1px solid #0f1729;">
  <div style="font-size:.72rem;font-weight:700;color:#475569;width:18px;">#{i}</div>
  <div style="flex:1;font-size:.78rem;color:#94a3b8;">{short}</div>
  <div style="font-size:.7rem;color:#6366f1;font-weight:700;">{pct}%</div>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — SEGMENT EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
elif "Explorer" in page:
    st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">📊 RFM · KMeans · Behavioural Segmentation</div>
  <h1 class="hero-title" style="font-size:2.8rem;">Segment Explorer</h1>
  <p class="hero-sub">Deep-dive into each behavioural segment — understand who they are, what they spend, and the <b>exact marketing strategy</b> to apply.</p>
</div>""", unsafe_allow_html=True)

    seg_tabs = st.tabs([s for s in sorted(rfm_f["Segment"].unique())])

    for tab, seg in zip(seg_tabs, sorted(rfm_f["Segment"].unique())):
        with tab:
            info=seg_info(seg)
            sdata=rfm_f[rfm_f["Segment"]==seg]
            count=len(sdata)
            color=seg_color(seg)

            if count==0:
                st.info("No customers in this segment with current filters.")
                continue

            c1,c2=st.columns([1,1.6])
            with c1:
                st.markdown(f"""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:16px;padding:1.5rem;">
  <div style="font-size:2.8rem;margin-bottom:.7rem;">{info['icon']}</div>
  <div style="font-size:1.4rem;font-weight:800;color:#f1f5f9;margin-bottom:.4rem;">{seg}</div>
  <div style="display:inline-block;background:{info['pill_bg']};color:{info['pill_color']};border:1px solid {info['pill_color']}44;border-radius:50px;padding:3px 14px;font-size:.72rem;font-weight:700;margin-bottom:1.1rem;">{info['cta']}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:1rem;">
    <div style="background:#060b18;border-radius:10px;padding:.7rem;text-align:center;">
      <div style="font-size:1.15rem;font-weight:800;color:{color};">{sdata['Recency'].mean():.0f}d</div>
      <div style="font-size:.62rem;color:#475569;text-transform:uppercase;letter-spacing:.06em;">Recency</div>
    </div>
    <div style="background:#060b18;border-radius:10px;padding:.7rem;text-align:center;">
      <div style="font-size:1.15rem;font-weight:800;color:{color};">{sdata['Frequency'].mean():.1f}x</div>
      <div style="font-size:.62rem;color:#475569;text-transform:uppercase;letter-spacing:.06em;">Frequency</div>
    </div>
    <div style="background:#060b18;border-radius:10px;padding:.7rem;text-align:center;">
      <div style="font-size:1.15rem;font-weight:800;color:{color};">£{sdata['Monetary'].mean():,.0f}</div>
      <div style="font-size:.62rem;color:#475569;text-transform:uppercase;letter-spacing:.06em;">Avg Spend</div>
    </div>
  </div>
  <div style="background:#060b18;border-radius:10px;padding:.9rem;font-size:.8rem;color:#94a3b8;line-height:1.7;">{info['strategy']}</div>
  <div style="margin-top:.9rem;display:flex;justify-content:space-between;font-size:.72rem;">
    <span style="color:#475569;">{count} customers</span>
    <span style="color:{color};font-weight:700;">{count/len(rfm_f)*100:.1f}% of filtered base</span>
  </div>
</div>""", unsafe_allow_html=True)

            with c2:
                sub_metric = st.selectbox(f"Chart metric — {seg}", ["Monetary","Frequency","Recency"], key=f"metric_{seg}")
                sub_chart  = st.selectbox(f"Chart type — {seg}",   ["Histogram","Box","Violin"], key=f"chart_{seg}")
                cap99 = sdata[sub_metric].quantile(.97)
                sd_cap = sdata[sdata[sub_metric]<=cap99]

                if sub_chart=="Histogram":
                    cf=px.histogram(sd_cap,x=sub_metric,nbins=35,template="plotly_dark",
                                    color_discrete_sequence=[color],opacity=.85,
                                    labels={sub_metric:sub_metric+" Distribution"})
                elif sub_chart=="Box":
                    cf=px.box(sd_cap,y=sub_metric,template="plotly_dark",
                              color_discrete_sequence=[color],points="outliers")
                else:
                    cf=px.violin(sd_cap,y=sub_metric,template="plotly_dark",
                                 color_discrete_sequence=[color],box=True)
                cf.update_layout(**PLOT_BASE,height=220,showlegend=False,title=f"{sub_metric} — {sub_chart}")
                st.plotly_chart(cf,use_container_width=True)

                sf=px.scatter(sd_cap,x="Recency",y="Frequency",
                              size=np.sqrt(sd_cap["Monetary"].clip(1)).values,
                              color_discrete_sequence=[color],opacity=.65,
                              template="plotly_dark",size_max=18,
                              hover_data={"Monetary":":.0f"},
                              labels={"Recency":"Days Since Purchase","Frequency":"Orders"})
                sf.update_layout(**PLOT_BASE,height=220,showlegend=False,title="Recency vs Frequency")
                st.plotly_chart(sf,use_container_width=True)

    # Full comparison
    st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ All Segments</div><div class="sec-title">Side-by-Side Comparison</div></div>', unsafe_allow_html=True)
    prof=rfm_f.groupby("Segment").agg(
        Customers=("CustomerID","count"),
        Avg_Recency=("Recency","mean"),
        Avg_Frequency=("Frequency","mean"),
        Avg_Spend=("Monetary","mean"),
        Total_Revenue=("Monetary","sum"),
    ).round(1).reset_index()
    prof["Share"]=( prof["Customers"]/prof["Customers"].sum()*100).round(1).astype(str)+"%"
    prof["Avg_Spend"]=prof["Avg_Spend"].apply(lambda x:f"£{x:,.0f}")
    prof["Total_Revenue"]=prof["Total_Revenue"].apply(lambda x:f"£{x:,.0f}")
    prof.columns=["Segment","Customers","Avg Recency","Avg Frequency","Avg Spend","Total Revenue","Share"]
    st.dataframe(prof.set_index("Segment"),use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — LIVE PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
elif "Predictor" in page:
    st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">🔮 Real-Time ML Prediction</div>
  <h1 class="hero-title" style="font-size:2.8rem;">Predict Any Customer's<br>Segment Instantly</h1>
  <p class="hero-sub">Enter <b>Recency, Frequency & Monetary</b> values and our trained KMeans model classifies the customer in milliseconds — with a full strategy playbook.</p>
</div>""", unsafe_allow_html=True)

    cl, cm, cr = st.columns([1.1,1.2,1])

    with cl:
        st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ Input Panel</div><div class="sec-title">Enter RFM Values</div></div>', unsafe_allow_html=True)
        recency   = st.number_input("📅 Recency — Days since last purchase", 1,730,45,help="Lower = more recent = better")
        frequency = st.number_input("🔁 Frequency — Total number of orders",  1,500,8, help="Higher = more loyal")
        monetary  = st.number_input("💷 Monetary — Total spend (£)", 1.,500000.,1200.,step=100.,help="Higher = more valuable")

        # Quick preset buttons
        st.markdown('<div style="font-size:.72rem;color:#64748b;font-weight:600;margin:.8rem 0 .4rem;text-transform:uppercase;letter-spacing:.08em;">Quick Presets</div>', unsafe_allow_html=True)
        p1,p2,p3,p4=st.columns(4)
        preset=None
        with p1:
            if st.button("VIP",key="p1"): preset=(7,50,15000)
        with p2:
            if st.button("Regular",key="p2"): preset=(30,12,2500)
        with p3:
            if st.button("Occasional",key="p3"): preset=(90,3,400)
        with p4:
            if st.button("At-Risk",key="p4"): preset=(300,1,200)

        if preset:
            recency,frequency,monetary=preset
            st.rerun()

        st.markdown("---")
        st.markdown("""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:1rem;">
  <div style="font-size:.7rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.8rem;">📖 RFM Reference Guide</div>
  <div style="font-size:.78rem;line-height:2.1;color:#64748b;">
    📅 <b style="color:#94a3b8;">Recency:</b> 1–30d → Champion<br>
    📅 <b style="color:#94a3b8;">Recency:</b> 31–90d → Active<br>
    📅 <b style="color:#94a3b8;">Recency:</b> 91d+ → At-Risk<br>
    🔁 <b style="color:#94a3b8;">Frequency:</b> 10+ → Loyal<br>
    💷 <b style="color:#94a3b8;">Monetary:</b> £1,000+ → High Value
  </div>
</div>""", unsafe_allow_html=True)

        predict_btn=st.button("🔮  Predict My Segment")

    with cm:
        st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ ML Output</div><div class="sec-title">Prediction Result</div></div>', unsafe_allow_html=True)

        if predict_btn:
            X_scaled=scaler.transform([[recency,frequency,monetary]])
            cluster_id=kmeans.predict(X_scaled)[0]
            segment=cluster_label_map[cluster_id]
            info=seg_info(segment)
            color=seg_color(segment)

            distances=kmeans.transform(X_scaled)[0]
            conf=max(0,min(100,int((1-distances.min()/(distances.max()+1e-9))*100)))

            st.markdown(f"""
<div class="pred-box">
  <div style="font-size:3rem;margin-bottom:.5rem;">{info['icon']}</div>
  <div style="font-size:.68rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:.1em;">Predicted Segment</div>
  <div class="pred-seg" style="color:{color};">{segment}</div>
  <div style="display:inline-block;background:{info['pill_bg']};color:{info['pill_color']};border:1px solid {info['pill_color']}44;border-radius:50px;padding:4px 16px;font-size:.72rem;font-weight:700;margin-bottom:1rem;">{info['cta']}</div>
  <div style="margin-bottom:1rem;">
    <div style="font-size:.68rem;color:#475569;margin-bottom:5px;text-transform:uppercase;letter-spacing:.07em;">Model Confidence</div>
    <div style="background:#0f1729;border-radius:6px;height:10px;overflow:hidden;">
      <div style="width:{conf}%;height:100%;background:linear-gradient(90deg,{color},{color}88);border-radius:6px;transition:width 1s ease;"></div>
    </div>
    <div style="font-size:.78rem;color:{color};font-weight:700;margin-top:4px;">{conf}%</div>
  </div>
  <div class="pred-desc">{info['strategy']}</div>
</div>""", unsafe_allow_html=True)

            st.markdown(f"""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:1rem;margin-top:.8rem;">
  <div style="font-size:.68rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.7rem;">Input Summary</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;text-align:center;">
    <div><div style="font-size:1rem;font-weight:800;color:#f1f5f9;">{recency}d</div><div style="font-size:.62rem;color:#475569;text-transform:uppercase;">Recency</div></div>
    <div><div style="font-size:1rem;font-weight:800;color:#f1f5f9;">{frequency}x</div><div style="font-size:.62rem;color:#475569;text-transform:uppercase;">Frequency</div></div>
    <div><div style="font-size:1rem;font-weight:800;color:#f1f5f9;">£{monetary:,.0f}</div><div style="font-size:.62rem;color:#475569;text-transform:uppercase;">Monetary</div></div>
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="background:#0f1729;border:2px dashed #1e293b;border-radius:16px;padding:3.5rem 2rem;text-align:center;">
  <div style="font-size:3rem;margin-bottom:1rem;opacity:.4;">🔮</div>
  <div style="font-size:.95rem;font-weight:600;color:#334155;">Enter values on the left<br>and click Predict</div>
  <div style="font-size:.78rem;color:#1e293b;margin-top:.5rem;">Or try a Quick Preset above</div>
</div>""", unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="sec-wrap"><div class="sec-eyebrow">✦ Benchmarks</div><div class="sec-title">Segment Averages</div></div>', unsafe_allow_html=True)
        prof=rfm.groupby("Segment")[["Recency","Frequency","Monetary"]].mean().round(1)
        for sn,row in prof.iterrows():
            c=seg_color(sn)
            active=predict_btn and "segment" in dir() and sn==segment
            st.markdown(f"""
<div style="background:#0f1729;border:{'2px solid '+c if active else '1px solid #1e293b'};border-radius:12px;padding:.85rem;margin-bottom:.5rem;transition:all .3s;">
  <div style="font-size:.83rem;font-weight:700;color:{c};margin-bottom:.4rem;">{sn}</div>
  <div style="display:flex;justify-content:space-between;font-size:.72rem;color:#64748b;">
    <span>R: <b style="color:#94a3b8;">{row['Recency']:.0f}d</b></span>
    <span>F: <b style="color:#94a3b8;">{row['Frequency']:.1f}x</b></span>
    <span>M: <b style="color:#94a3b8;">£{row['Monetary']:,.0f}</b></span>
  </div>
</div>""", unsafe_allow_html=True)

        if predict_btn and "segment" in dir():
            mms=MinMaxScaler()
            normed=pd.DataFrame(mms.fit_transform(prof),columns=prof.columns,index=prof.index)
            un=mms.transform([[recency,frequency,monetary]])[0]
            cats=["Recency","Frequency","Monetary"]
            rfig=go.Figure()
            for sn,row in normed.iterrows():
                c=seg_color(sn); v=row.tolist()+[row.tolist()[0]]
                rfig.add_trace(go.Scatterpolar(r=v,theta=cats+[cats[0]],name=sn,
                    line=dict(color=c,width=1.5),fill='toself',fillcolor=c,opacity=.1))
            uv=un.tolist()+[un[0]]
            rfig.add_trace(go.Scatterpolar(r=uv,theta=cats+[cats[0]],name="You",
                line=dict(color="#fff",width=2.5,dash="dot"),fill='toself',fillcolor="#fff",opacity=.07))
            rfig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                               polar=dict(bgcolor="#0a0f1e",radialaxis=dict(gridcolor="#1e293b"),angularaxis=dict(gridcolor="#1e293b")),
                               legend=dict(font=dict(color="#64748b",size=9),bgcolor="rgba(0,0,0,0)"),
                               margin=dict(t=25,b=10,l=10,r=10),height=290,
                               title=dict(text="RFM Radar vs All Segments",font=dict(size=12,color="#f1f5f9"),x=0))
            st.plotly_chart(rfig,use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;border-top:1px solid #0f1729;margin-top:3rem;">
  <div style="font-size:.68rem;color:#1e293b;font-weight:600;letter-spacing:.1em;text-transform:uppercase;">
    Shopper Spectrum · AI-Powered Retail Intelligence · Pandas · Scikit-learn · Plotly · Streamlit
  </div>
</div>""", unsafe_allow_html=True)
