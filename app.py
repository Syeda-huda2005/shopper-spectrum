"""
🛒 Shopverse  
“Where every choice meets innovation.”
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="| Shopverse -Your universe of smart shopping.",
    page_icon="🛒", layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #060b18 !important; }
.main .block-container { padding: 1.5rem 2rem 3rem 2rem !important; max-width: 1400px !important; }

@keyframes gradientShift {
  0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%}
}
@keyframes fadeInUp {
  from{opacity:0;transform:translateY(24px)} to{opacity:1;transform:translateY(0)}
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.6} }
@keyframes countUp { from{opacity:0;transform:scale(0.85)} to{opacity:1;transform:scale(1)} }

.hero-wrapper {
  background: linear-gradient(-45deg,#0d1b3e,#0a0f2e,#1a0a3e,#0d2040,#060b18);
  background-size:400% 400%; animation:gradientShift 8s ease infinite;
  border-radius:24px; padding:3rem 3rem 2.5rem; margin-bottom:1.5rem;
  border:1px solid rgba(99,102,241,0.3); position:relative; overflow:hidden;
}
.hero-wrapper::before {
  content:''; position:absolute; top:0;left:0;right:0;bottom:0;
  background:radial-gradient(ellipse at 20% 50%,rgba(99,102,241,0.15) 0%,transparent 60%),
             radial-gradient(ellipse at 80% 20%,rgba(34,211,238,0.1) 0%,transparent 50%);
  pointer-events:none;
}
.hero-badge {
  display:inline-flex;align-items:center;gap:8px;
  background:rgba(99,102,241,0.15);border:1px solid rgba(99,102,241,0.4);
  border-radius:50px;padding:5px 16px;font-size:0.72rem;font-weight:600;
  color:#a5b4fc;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:1rem;
}
.hero-title {
  font-size:3.2rem;font-weight:900;line-height:1.1;
  background:linear-gradient(135deg,#ffffff 0%,#a5b4fc 40%,#22d3ee 70%,#f472b6 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin:0 0 0.8rem 0;animation:fadeInUp 0.7s ease both;
}
.hero-sub { font-size:1.05rem;color:#94a3b8;line-height:1.7;max-width:620px; }
.hero-sub span { color:#a5b4fc;font-weight:600; }
.hero-tags { display:flex;flex-wrap:wrap;gap:8px;margin-top:1.5rem; }
.hero-tag {
  background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
  border-radius:8px;padding:5px 12px;font-size:0.75rem;color:#64748b;
}
.hero-tag span { color:#94a3b8; }

.kpi-grid { display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:1.5rem; }
.kpi-card {
  background:linear-gradient(135deg,#0f1729,#111827);border:1px solid #1e293b;
  border-radius:16px;padding:1.2rem;text-align:center;position:relative;overflow:hidden;
  transition:all 0.3s;cursor:default;animation:countUp 0.5s ease both;
}
.kpi-card:hover { transform:translateY(-4px);border-color:#334155;box-shadow:0 20px 40px rgba(0,0,0,0.4); }
.kpi-card::before { content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:16px 16px 0 0; }
.kpi-card:nth-child(1)::before{background:linear-gradient(90deg,#6366f1,#818cf8);}
.kpi-card:nth-child(2)::before{background:linear-gradient(90deg,#22d3ee,#67e8f9);}
.kpi-card:nth-child(3)::before{background:linear-gradient(90deg,#f472b6,#fb7185);}
.kpi-card:nth-child(4)::before{background:linear-gradient(90deg,#facc15,#fde68a);}
.kpi-card:nth-child(5)::before{background:linear-gradient(90deg,#4ade80,#86efac);}
.kpi-val { font-size:1.8rem;font-weight:800;color:#f1f5f9;line-height:1;margin:0.4rem 0 0.2rem; }
.kpi-lbl { font-size:0.68rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.08em; }
.kpi-delta { font-size:0.72rem;color:#4ade80;font-weight:600;margin-top:0.3rem; }

.section-eyebrow { font-size:0.68rem;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.2rem; }
.section-title { font-size:1.4rem;font-weight:700;color:#f1f5f9;margin:0; }
.section-sub { font-size:0.83rem;color:#64748b;margin-top:0.2rem;margin-bottom:1rem; }

.filter-bar {
  background:#0f1729;border:1px solid #1e293b;border-radius:14px;
  padding:1rem 1.2rem;margin-bottom:1.2rem;
}
.filter-label { font-size:0.68rem;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem; }

.insight-row { display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:1rem 0; }
.insight-card {
  background:#0f1729;border:1px solid #1e293b;border-radius:14px;padding:1.1rem;
  display:flex;align-items:flex-start;gap:12px;transition:all 0.25s;
}
.insight-card:hover { border-color:#334155;transform:translateX(4px); }
.insight-icon { width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0; }
.insight-title { font-size:0.72rem;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:0.06em; }
.insight-val { font-size:1.05rem;font-weight:700;color:#f1f5f9;margin:0.2rem 0; }
.insight-desc { font-size:0.75rem;color:#475569;line-height:1.5; }

.rec-item {
  background:linear-gradient(135deg,#0f1729,#0a1020);border:1px solid #1e293b;
  border-radius:12px;padding:0.9rem 1.1rem;margin:0.4rem 0;
  display:flex;align-items:center;gap:12px;transition:all 0.25s;
}
.rec-item:hover { border-color:#6366f1;transform:translateX(6px); }
.rec-rank { width:32px;height:32px;border-radius:8px;background:rgba(99,102,241,0.15);
  color:#6366f1;font-weight:800;font-size:0.8rem;display:flex;align-items:center;justify-content:center;flex-shrink:0; }
.rec-name { font-size:0.88rem;font-weight:600;color:#f1f5f9;margin-bottom:4px; }
.rec-bar { height:4px;border-radius:2px;background:#1e293b;margin-top:4px; }
.rec-fill { height:100%;border-radius:2px;background:linear-gradient(90deg,#6366f1,#22d3ee); }
.rec-score { font-size:0.73rem;color:#22d3ee;font-weight:600; }

.pred-box {
  background:linear-gradient(135deg,#0f1729,#0a1020);border-radius:18px;
  padding:1.8rem;text-align:center;border:1px solid #1e293b;
}
.pred-seg { font-size:1.8rem;font-weight:900;margin:0.4rem 0; }

section[data-testid="stSidebar"] { background:#060b18 !important;border-right:1px solid #0f1729 !important; }
.stNumberInput>div>div>input,.stTextInput>div>div>input {
  background:#0f1729 !important;border:1px solid #1e293b !important;
  color:#f1f5f9 !important;border-radius:10px !important;
}
.stSelectbox>div>div { background:#0f1729 !important;border:1px solid #1e293b !important;border-radius:10px !important; }
div[data-testid="stButton"]>button {
  background:linear-gradient(135deg,#6366f1,#4f46e5) !important;color:white !important;
  border:none !important;border-radius:12px !important;padding:0.65rem 1.8rem !important;
  font-weight:700 !important;width:100% !important;transition:all 0.25s !important;
}
div[data-testid="stButton"]>button:hover {
  background:linear-gradient(135deg,#818cf8,#6366f1) !important;
  transform:translateY(-2px) !important;box-shadow:0 8px 25px rgba(99,102,241,0.5) !important;
}
.stSlider>div>div>div { background:#6366f1 !important; }
hr { border-color:#1e293b !important; }
.stTabs [data-baseweb="tab"] { color:#64748b !important;font-weight:600 !important; }
.stTabs [aria-selected="true"] { color:#6366f1 !important; }
div[data-testid="stMetric"] { background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:0.8rem; }
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

# ── Session State Init (drives the interactive/live features) ────────────────
if "shortlist" not in st.session_state: st.session_state.shortlist=[]
if "scenario_history" not in st.session_state: st.session_state.scenario_history=[]
if "live_mode" not in st.session_state: st.session_state.live_mode=False

COLOR_MAP={
    "High-Value 🏆":"#4ade80","Regular 🔄":"#6366f1",
    "Occasional 💤":"#facc15","At-Risk ⚠️":"#f87171",
    "High-Value":"#4ade80","Regular":"#6366f1",
    "Occasional":"#facc15","At-Risk":"#f87171",
}
SEG_INFO={
    "High-Value 🏆":{"icon":"👑","pill_bg":"#052e16","pill_color":"#4ade80","cta":"Retain & Upsell","strategy":"<strong>VIP Treatment:</strong> Exclusive early access, personal account manager, loyalty multipliers, premium bundles & private sale invites."},
    "Regular 🔄":{"icon":"🔄","pill_bg":"#1e1b4b","pill_color":"#818cf8","cta":"Grow & Expand","strategy":"<strong>Growth Play:</strong> Cross-sell complementary categories, seasonal campaigns, referral rewards & subscription nudges."},
    "Occasional 💤":{"icon":"💡","pill_bg":"#422006","pill_color":"#fbbf24","cta":"Activate & Engage","strategy":"<strong>Re-Engage:</strong> Flash sale alerts, limited-time discount codes, reminders & loyalty point bonuses."},
    "At-Risk ⚠️":{"icon":"🚨","pill_bg":"#450a0a","pill_color":"#f87171","cta":"Rescue & Recover","strategy":"<strong>Win-Back:</strong> Personalised 'We miss you' email, steep discount, churn survey + free shipping."},
    "High-Value":{"icon":"👑","pill_bg":"#052e16","pill_color":"#4ade80","cta":"Retain & Upsell","strategy":"<strong>VIP Treatment:</strong> Exclusive early access, personal account manager, loyalty multipliers."},
    "Regular":{"icon":"🔄","pill_bg":"#1e1b4b","pill_color":"#818cf8","cta":"Grow & Expand","strategy":"<strong>Growth Play:</strong> Cross-sell complementary categories, seasonal campaigns & referral rewards."},
    "Occasional":{"icon":"💡","pill_bg":"#422006","pill_color":"#fbbf24","cta":"Activate & Engage","strategy":"<strong>Re-Engage:</strong> Flash sale alerts, discount codes & loyalty bonuses."},
    "At-Risk":{"icon":"🚨","pill_bg":"#450a0a","pill_color":"#f87171","cta":"Rescue & Recover","strategy":"<strong>Win-Back:</strong> Personalised email, steep discount & churn survey."},
}

PLOT_BASE=dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#0a0f1e",
               font=dict(color="#94a3b8",family="Inter"),
               margin=dict(t=40,b=30,l=20,r=20),
               xaxis=dict(gridcolor="#0f1729",zeroline=False),
               yaxis=dict(gridcolor="#0f1729",zeroline=False))

all_segments=rfm["Segment"].unique().tolist()

def animated_kpi_grid(cards):
    """Renders a KPI grid with a brief count-up animation on first paint.
    `cards` is a list of dicts: icon, value, label, delta, delta_color"""
    ph=st.empty()
    steps=8
    for s in range(1,steps+1):
        frac=s/steps
        html='<div class="kpi-grid">'
        for c in cards:
            val=c["value"]
            if isinstance(val,(int,float,np.integer,np.floating)) and not isinstance(val,str):
                shown=val*frac
                if c.get("fmt")=="money":
                    disp=f"£{shown:,.0f}"
                elif c.get("fmt")=="x":
                    disp=f"{shown:.1f}x"
                else:
                    disp=f"{shown:,.0f}"
            else:
                disp=val
            dcolor=c.get("delta_color","#4ade80")
            html+=f"""<div class="kpi-card"><div style="font-size:1.4rem;">{c['icon']}</div>
<div class="kpi-val">{disp}</div><div class="kpi-lbl">{c['label']}</div>
<div class="kpi-delta" style="color:{dcolor};">{c['delta']}</div></div>"""
        html+="</div>"
        ph.markdown(html,unsafe_allow_html=True)
        if s<steps: time.sleep(0.02)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:1rem 0 1.2rem;">
  <div style="font-size:2.2rem;margin-bottom:0.4rem;">🛒</div>
  <div style="font-size:1rem;font-weight:800;color:#f1f5f9;">Shopper Spectrum</div>
  <div style="font-size:0.7rem;color:#475569;margin-top:2px;">AI-Powered Retail Intelligence</div>
</div>""",unsafe_allow_html=True)

    page=st.radio("",["🏠  Command Centre","🎯  Product Recommender","👥  Segment Explorer","🔮  Live Predictor","📊  RFM Deep Dive"],label_visibility="collapsed")

    st.markdown("---")

    # Global Segment Filter
    st.markdown('<div style="font-size:0.68rem;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">🎛️ Global Segment Filter</div>',unsafe_allow_html=True)
    selected_segs=st.multiselect("Filter segments",all_segments,default=all_segments,label_visibility="collapsed")
    if not selected_segs:
        selected_segs=all_segments

    # Global RFM range filters (apply everywhere via rfm_filtered)
    with st.expander("🎚️ Advanced RFM Filters"):
        g_r=st.slider("Recency ≤ (days)",0,int(rfm["Recency"].max()),int(rfm["Recency"].max()),key="g_r")
        g_f=st.slider("Frequency ≥",1,int(rfm["Frequency"].max()),1,key="g_f")
        g_m=st.slider("Monetary ≥ (£)",0,int(rfm["Monetary"].max()),0,key="g_m")

    rfm_filtered=rfm[
        (rfm["Segment"].isin(selected_segs)) &
        (rfm["Recency"]<=g_r) & (rfm["Frequency"]>=g_f) & (rfm["Monetary"]>=g_m)
    ]

    st.session_state.live_mode=st.toggle("⚡ Live Animated Stats",value=st.session_state.live_mode,help="Animate KPI counters as they load")

    st.markdown("---")
    st.markdown(f"""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:1rem;">
  <div style="font-size:0.68rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.8rem;">📈 Model Stats</div>
  <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;"><span style="font-size:0.75rem;color:#64748b;">Silhouette</span><span style="font-size:0.75rem;font-weight:700;color:#4ade80;">0.6162</span></div>
  <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;"><span style="font-size:0.75rem;color:#64748b;">Clusters</span><span style="font-size:0.75rem;font-weight:700;color:#a5b4fc;">4</span></div>
  <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;"><span style="font-size:0.75rem;color:#64748b;">Customers</span><span style="font-size:0.75rem;font-weight:700;color:#a5b4fc;">{len(rfm_filtered):,}</span></div>
  <div style="display:flex;justify-content:space-between;"><span style="font-size:0.75rem;color:#64748b;">Showing</span><span style="font-size:0.75rem;font-weight:700;color:#22d3ee;">{len(selected_segs)} segments</span></div>
</div>""",unsafe_allow_html=True)

    if st.session_state.shortlist:
        with st.expander(f"❤️ Shortlist ({len(st.session_state.shortlist)})"):
            for p in st.session_state.shortlist:
                st.markdown(f"<div style='font-size:0.72rem;color:#94a3b8;padding:2px 0;'>• {p[:40]}</div>",unsafe_allow_html=True)
            if st.button("Clear shortlist",key="clear_shortlist"):
                st.session_state.shortlist=[]
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — COMMAND CENTRE
# ══════════════════════════════════════════════════════════════════════════════
if "Command" in page:
    st.markdown("""
<div class="hero-wrapper">
  <div class="hero-badge">⚡ AI-Powered · Real-Time · E-Commerce Analytics</div>
  <h1 class="hero-title">Know Your Customer.<br>Grow Your Revenue.</h1>
  <p class="hero-sub">Shopper Spectrum transforms raw transaction data into <span>actionable intelligence</span> — segmenting customers, predicting behaviour & recommending products that convert.</p>
  <div class="hero-tags">
    <div class="hero-tag">📦 <span>541,909</span> Transactions</div>
    <div class="hero-tag">👥 <span>4,338</span> Customers</div>
    <div class="hero-tag">🌍 <span>37</span> Countries</div>
    <div class="hero-tag">🤖 <span>KMeans + Cosine Similarity</span></div>
  </div>
</div>""",unsafe_allow_html=True)

    # Live KPIs based on filter
    seg_counts=rfm_filtered["Segment"].value_counts()
    total=len(rfm_filtered)
    hv=seg_counts.get("High-Value 🏆",seg_counts.get("High-Value",0))
    ar=seg_counts.get("At-Risk ⚠️",seg_counts.get("At-Risk",0))
    avg_m=rfm_filtered["Monetary"].mean() if total>0 else 0
    avg_f=rfm_filtered["Frequency"].mean() if total>0 else 0
    avg_r=rfm_filtered["Recency"].mean() if total>0 else 0

    kpi_cards=[
        {"icon":"👥","value":total,"label":"Customers (Filtered)","delta":f"↑ {total/len(rfm)*100:.0f}% of base","fmt":"n"},
        {"icon":"👑","value":hv,"label":"High-Value VIPs","delta":"↑ Top Revenue Drivers","fmt":"n"},
        {"icon":"⚠️","value":ar,"label":"At-Risk Customers","delta":"↓ Need Win-Back","delta_color":"#f87171","fmt":"n"},
        {"icon":"💷","value":avg_m,"label":"Avg Spend (LTV)","delta":"↑ Per Customer","fmt":"money"},
        {"icon":"🔁","value":avg_f,"label":"Avg Frequency","delta":f"Avg Recency: {avg_r:.0f}d","fmt":"x"},
    ]
    if st.session_state.live_mode:
        animated_kpi_grid(kpi_cards)
    else:
        st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card"><div style="font-size:1.4rem;">👥</div><div class="kpi-val">{total:,}</div><div class="kpi-lbl">Customers (Filtered)</div><div class="kpi-delta">↑ {total/len(rfm)*100:.0f}% of base</div></div>
  <div class="kpi-card"><div style="font-size:1.4rem;">👑</div><div class="kpi-val">{hv}</div><div class="kpi-lbl">High-Value VIPs</div><div class="kpi-delta">↑ Top Revenue Drivers</div></div>
  <div class="kpi-card"><div style="font-size:1.4rem;">⚠️</div><div class="kpi-val">{ar}</div><div class="kpi-lbl">At-Risk Customers</div><div class="kpi-delta" style="color:#f87171;">↓ Need Win-Back</div></div>
  <div class="kpi-card"><div style="font-size:1.4rem;">💷</div><div class="kpi-val">£{avg_m:,.0f}</div><div class="kpi-lbl">Avg Spend (LTV)</div><div class="kpi-delta">↑ Per Customer</div></div>
  <div class="kpi-card"><div style="font-size:1.4rem;">🔁</div><div class="kpi-val">{avg_f:.1f}x</div><div class="kpi-lbl">Avg Frequency</div><div class="kpi-delta">Avg Recency: {avg_r:.0f}d</div></div>
</div>""",unsafe_allow_html=True)

    # Chart Controls
    st.markdown('<div class="filter-bar">',unsafe_allow_html=True)
    cc1,cc2,cc3=st.columns(3)
    with cc1:
        chart_type=st.selectbox("📊 Chart Style",["Donut","Bar","Treemap"],key="cc1")
    with cc2:
        color_metric=st.selectbox("🎨 Color By",["Segment","Recency Group","Frequency Group"],key="cc2")
    with cc3:
        monetary_cap=st.slider("💷 Monetary Cap (£)",500,50000,10000,500,key="cc3")
    st.markdown('</div>',unsafe_allow_html=True)

    col1,col2=st.columns([1,1.1])

    with col1:
        st.markdown('<div class="section-eyebrow">✦ Segment Distribution</div><div class="section-title">Customer Breakdown</div>',unsafe_allow_html=True)
        seg_df=rfm_filtered["Segment"].value_counts().reset_index()
        seg_df.columns=["Segment","Count"]

        if chart_type=="Donut":
            fig=px.pie(seg_df,values="Count",names="Segment",hole=0.6,
                       color="Segment",color_discrete_map=COLOR_MAP,template="plotly_dark")
            fig.update_traces(textinfo="percent+label",textfont_color="white",
                              hovertemplate="<b>%{label}</b><br>%{value} customers (%{percent})<extra></extra>")
            fig.update_layout(**PLOT_BASE,height=320,showlegend=False,
                              annotations=[dict(text=f"<b>{total:,}</b>",x=0.5,y=0.5,font_size=18,font_color="#f1f5f9",showarrow=False)])
        elif chart_type=="Bar":
            fig=px.bar(seg_df,x="Segment",y="Count",color="Segment",
                       color_discrete_map=COLOR_MAP,template="plotly_dark",
                       text="Count",labels={"Count":"Customers"})
            fig.update_traces(textposition="outside",textfont_color="#94a3b8",
                              hovertemplate="<b>%{x}</b><br>%{y} customers<extra></extra>")
            fig.update_layout(**PLOT_BASE,height=320,showlegend=False)
        else:
            fig=px.treemap(seg_df,path=["Segment"],values="Count",
                           color="Count",color_continuous_scale=["#1e293b","#6366f1","#22d3ee"],
                           template="plotly_dark")
            fig.update_layout(**PLOT_BASE,height=320)
        st.plotly_chart(fig,use_container_width=True)

        st.markdown('<div class="filter-label">🔎 Drill Down — pick a segment to inspect</div>',unsafe_allow_html=True)
        drill_seg=st.selectbox("Drill into segment",["(none)"]+seg_df["Segment"].tolist(),key="drill_seg",label_visibility="collapsed")
        if drill_seg!="(none)":
            dd=rfm_filtered[rfm_filtered["Segment"]==drill_seg]
            c=COLOR_MAP.get(drill_seg,"#6366f1")
            st.markdown(f"""
<div style="background:#0f1729;border:1px solid {c}55;border-radius:12px;padding:0.9rem;margin-top:0.4rem;">
  <div style="font-size:0.8rem;font-weight:700;color:{c};margin-bottom:0.5rem;">{drill_seg} — {len(dd):,} customers</div>
  <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#94a3b8;">
    <span>Avg Recency: <b>{dd['Recency'].mean():.0f}d</b></span>
    <span>Avg Frequency: <b>{dd['Frequency'].mean():.1f}x</b></span>
    <span>Avg Spend: <b>£{dd['Monetary'].mean():,.0f}</b></span>
    <span>Revenue Share: <b>{dd['Monetary'].sum()/rfm_filtered['Monetary'].sum()*100 if rfm_filtered['Monetary'].sum() else 0:.1f}%</b></span>
  </div>
</div>""",unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-eyebrow">✦ Customer Map</div><div class="section-title">RFM Scatter Explorer</div>',unsafe_allow_html=True)
        rfm_s=rfm_filtered[rfm_filtered["Monetary"]<=monetary_cap].copy()
        if drill_seg!="(none)":
            rfm_s=rfm_s[rfm_s["Segment"]==drill_seg]
        rfm_s["Size"]=np.sqrt(rfm_s["Monetary"].clip(1))

        if color_metric=="Recency Group":
            rfm_s["Color Group"]=pd.cut(rfm_s["Recency"],bins=[0,30,90,180,730],labels=["<30d","30-90d","90-180d","180d+"])
            color_col="Color Group"
            cmap=None
        elif color_metric=="Frequency Group":
            rfm_s["Color Group"]=pd.cut(rfm_s["Frequency"],bins=[0,2,5,15,500],labels=["1-2","3-5","6-15","15+"])
            color_col="Color Group"
            cmap=None
        else:
            color_col="Segment"
            cmap=COLOR_MAP

        fig2=px.scatter(rfm_s,x="Recency",y="Frequency",size="Size",color=color_col,
                        color_discrete_map=cmap,opacity=0.7,template="plotly_dark",
                        hover_data={"Monetary":":.0f","Size":False,"CustomerID":True},
                        labels={"Recency":"Recency (days)","Frequency":"Orders"},size_max=25)
        fig2.update_layout(**PLOT_BASE,height=320,
                           legend=dict(orientation="h",yanchor="bottom",y=1.02,font=dict(size=9),bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig2,use_container_width=True)

    # Key Insights
    st.markdown("""
<div style="margin:1.5rem 0 0.8rem;">
  <div class="section-eyebrow">✦ Business Intelligence</div>
  <div class="section-title">Key Findings</div>
</div>
<div class="insight-row">
  <div class="insight-card">
    <div class="insight-icon" style="background:#1e1b4b;">🇬🇧</div>
    <div><div class="insight-title">Market Dominance</div><div class="insight-val">91.4% UK</div><div class="insight-desc">United Kingdom leads all transaction volume — critical focus market for every campaign.</div></div>
  </div>
  <div class="insight-card">
    <div class="insight-icon" style="background:#052e16;">📈</div>
    <div><div class="insight-title">Revenue Peak</div><div class="insight-val">Q4 Surge 2.3×</div><div class="insight-desc">November drives 2.3× average monthly revenue — Black Friday & Christmas effect.</div></div>
  </div>
  <div class="insight-card">
    <div class="insight-icon" style="background:#422006;">🕐</div>
    <div><div class="insight-title">Golden Hours</div><div class="insight-val">9 AM – 12 PM</div><div class="insight-desc">Tues–Thurs mornings have highest transaction density — ideal for flash sales & push alerts.</div></div>
  </div>
</div>""",unsafe_allow_html=True)

    # Spend distribution with interactive bin control
    st.markdown('<div style="margin:1.5rem 0 0.5rem;"><div class="section-eyebrow">✦ Revenue Analysis</div><div class="section-title">Spend Distribution by Segment</div></div>',unsafe_allow_html=True)
    bc1,bc2=st.columns([3,1])
    with bc2:
        n_bins=st.slider("Histogram bins",10,100,40,key="bins")
        show_violin=st.toggle("Violin overlay",value=False)

    rfm_cap=rfm_filtered[rfm_filtered["Monetary"]<=rfm_filtered["Monetary"].quantile(0.95)]
    if show_violin:
        fig_spend=px.violin(rfm_cap,x="Segment",y="Monetary",color="Segment",
                            color_discrete_map=COLOR_MAP,box=True,template="plotly_dark",
                            labels={"Monetary":"Total Spend (£)","Segment":""})
    else:
        fig_spend=px.box(rfm_cap,x="Segment",y="Monetary",color="Segment",
                         color_discrete_map=COLOR_MAP,template="plotly_dark",points="outliers",
                         labels={"Monetary":"Total Spend (£)","Segment":""})
    fig_spend.update_layout(**PLOT_BASE,height=300,showlegend=False)
    with bc1:
        st.plotly_chart(fig_spend,use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRODUCT RECOMMENDER
# ══════════════════════════════════════════════════════════════════════════════
elif "Recommender" in page:
    st.markdown("""
<div class="hero-wrapper">
  <div class="hero-badge">🤖 Item-Based Collaborative Filtering · Cosine Similarity</div>
  <h1 class="hero-title" style="font-size:2.6rem;">Product Recommendation<br>Engine</h1>
  <p class="hero-sub">Select any product, control the filters, and discover what customers who bought it also purchased — <span>powered by Cosine Similarity</span> across 500 top products.</p>
</div>""",unsafe_allow_html=True)

    col_l,col_r=st.columns([1.2,1])

    with col_l:
        all_products=sorted(item_sim_df.index.tolist())
        default_idx=all_products.index("WHITE HANGING HEART T-LIGHT HOLDER") if "WHITE HANGING HEART T-LIGHT HOLDER" in all_products else 0

        st.markdown('<div class="section-eyebrow">✦ Configure</div><div class="section-title">Find Similar Products</div><div class="section-sub">Use the controls below to customise your recommendations</div>',unsafe_allow_html=True)

        # Search filter
        search_term=st.text_input("🔍 Search products",placeholder="Type to filter product list...",key="prod_search")

        # Live "category" filter — first word of product name acts as a cheap tag
        first_words=sorted(set(p.split()[0] for p in all_products if p.split()))
        cat_filter=st.multiselect("🏷️ Filter by starting keyword (live)",first_words,default=[],key="cat_filter")

        filtered_prods=all_products
        if search_term:
            filtered_prods=[p for p in filtered_prods if search_term.upper() in p.upper()]
        if cat_filter:
            filtered_prods=[p for p in filtered_prods if p.split()[0] in cat_filter]

        if filtered_prods:
            selected=st.selectbox(f"Select product ({len(filtered_prods)} match)",filtered_prods,key="prod_select")
        else:
            st.warning("No products match your search/filter.")
            selected=all_products[0]

        c1,c2=st.columns(2)
        with c1: top_n=st.slider("# Recommendations",3,15,5,key="topn")
        with c2: sim_threshold=st.slider("Min similarity",0.0,0.9,0.0,0.05,key="simth")

        show_chart=st.toggle("Similarity bar chart",True,key="showchart")
        show_network=st.toggle("Similarity heatmap",False,key="shownet")
        auto_update=st.toggle("⚡ Live update (no button needed)",True,key="auto_update")

        run_now=auto_update or st.button("🚀  Generate Recommendations",key="genrec")

        if run_now:
            similar=item_sim_df[selected].drop(selected)
            similar=similar[similar>=sim_threshold].sort_values(ascending=False).head(top_n)

            if len(similar)==0:
                st.warning("No products found above similarity threshold. Try lowering it.")
            else:
                st.markdown(f"""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:1rem;margin:0.8rem 0;">
  <div style="font-size:0.68rem;color:#475569;font-weight:700;text-transform:uppercase;">Selected Product</div>
  <div style="font-size:0.95rem;font-weight:700;color:#a5b4fc;margin-top:0.3rem;">{selected}</div>
  <div style="font-size:0.75rem;color:#475569;margin-top:0.2rem;">{len(similar)} recommendations · min similarity {sim_threshold:.2f}</div>
</div>""",unsafe_allow_html=True)

                colors=["#facc15","#94a3b8","#fb923c","#6366f1","#22d3ee","#4ade80","#f472b6","#818cf8","#67e8f9","#86efac","#fca5a5","#c4b5fd","#6ee7b7","#fde68a","#bfdbfe"]
                for rank,(prod,score) in enumerate(similar.items(),1):
                    fill=int(score*100)
                    c=colors[rank-1] if rank<=len(colors) else "#6366f1"
                    short=prod[:50]+"…" if len(prod)>50 else prod
                    rrow1,rrow2=st.columns([6,1])
                    with rrow1:
                        st.markdown(f"""
<div class="rec-item">
  <div class="rec-rank" style="color:{c};">#{rank}</div>
  <div style="flex:1;">
    <div class="rec-name">{short}</div>
    <div class="rec-bar"><div class="rec-fill" style="width:{fill}%;background:linear-gradient(90deg,{c},{c}88);"></div></div>
  </div>
  <div class="rec-score">{score:.4f}</div>
</div>""",unsafe_allow_html=True)
                    with rrow2:
                        is_fav=prod in st.session_state.shortlist
                        if st.button("💔" if is_fav else "🤍",key=f"fav_{rank}_{prod}"):
                            if is_fav:
                                st.session_state.shortlist.remove(prod)
                            else:
                                st.session_state.shortlist.append(prod)
                            st.rerun()

                if show_chart:
                    fig=go.Figure(go.Bar(
                        x=similar.values[::-1],
                        y=[p[:35]+"…" if len(p)>35 else p for p in similar.index[::-1]],
                        orientation="h",
                        marker=dict(color=similar.values[::-1],colorscale=[[0,"#334155"],[0.5,"#6366f1"],[1,"#22d3ee"]],showscale=False),
                        text=[f"{v:.3f}" for v in similar.values[::-1]],
                        textposition="outside",textfont=dict(color="#94a3b8",size=10),
                        hovertemplate="<b>%{y}</b><br>Similarity: %{x:.4f}<extra></extra>"
                    ))
                    fig.update_layout(**PLOT_BASE,height=max(220,len(similar)*45),
                                      xaxis_title="Cosine Similarity",
                                      title=dict(text="Similarity Scores",font=dict(size=13,color="#f1f5f9"),x=0))
                    st.plotly_chart(fig,use_container_width=True)

                if show_network:
                    top_prods_heat=[selected]+similar.index.tolist()
                    sim_sub=item_sim_df.loc[top_prods_heat,top_prods_heat]
                    short_labels=[p[:25]+"…" if len(p)>25 else p for p in top_prods_heat]
                    fig_h=go.Figure(go.Heatmap(
                        z=sim_sub.values,x=short_labels,y=short_labels,
                        colorscale="RdYlGn",zmid=0.5,
                        hovertemplate="<b>%{y}</b> × <b>%{x}</b><br>Similarity: %{z:.3f}<extra></extra>"
                    ))
                    fig_h.update_layout(**PLOT_BASE,height=400,
                                        title=dict(text="Product Similarity Heatmap",font=dict(size=13,color="#f1f5f9"),x=0))
                    st.plotly_chart(fig_h,use_container_width=True)

    with col_r:
        st.markdown('<div class="section-eyebrow">✦ Algorithm</div><div class="section-title">How It Works</div>',unsafe_allow_html=True)
        for num,color,title,desc in [
            ("01","#6366f1","Build Purchase Matrix","Create a Customer × Product matrix tracking units bought per product."),
            ("02","#22d3ee","Cosine Similarity","Calculate pairwise similarity between product vectors — co-purchased items score higher."),
            ("03","#f472b6","Rank & Filter","Return top-N items above your similarity threshold, ranked highest first."),
        ]:
            with st.expander(f"{num} · {title}"):
                st.markdown(f'<div style="font-size:0.78rem;color:#94a3b8;line-height:1.6;">{desc}</div>',unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-eyebrow">✦ Explore</div><div class="section-title">Compare Two Products</div><div class="section-sub">See how similar any two products are</div>',unsafe_allow_html=True)
        pa=st.selectbox("Product A",all_products,index=0,key="pa")
        pb=st.selectbox("Product B",all_products,index=1,key="pb")
        if pa!=pb and pa in item_sim_df.index and pb in item_sim_df.index:
            score=item_sim_df.loc[pa,pb]
            pct=int(score*100)
            color="#4ade80" if score>0.5 else "#facc15" if score>0.2 else "#f87171"
            st.markdown(f"""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:1.2rem;text-align:center;margin-top:0.5rem;">
  <div style="font-size:0.68rem;color:#475569;font-weight:700;text-transform:uppercase;margin-bottom:0.5rem;">Similarity Score</div>
  <div style="font-size:2.5rem;font-weight:900;color:{color};">{score:.4f}</div>
  <div style="background:#1e293b;border-radius:6px;height:8px;margin:0.8rem 0;overflow:hidden;">
    <div style="width:{pct}%;height:100%;background:{color};border-radius:6px;"></div>
  </div>
  <div style="font-size:0.78rem;color:#64748b;">{"High similarity — frequently co-purchased" if score>0.5 else "Moderate similarity" if score>0.2 else "Low similarity — rarely bought together"}</div>
</div>""",unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-eyebrow">✦ Popular</div><div class="section-title">Most Linked Products</div>',unsafe_allow_html=True)
        link_thresh=st.slider("Link threshold",0.05,0.9,0.3,0.05,key="link_thresh")
        top_linked=(item_sim_df>link_thresh).sum().sort_values(ascending=False).head(6)
        for i,(prod,cnt) in enumerate(top_linked.items(),1):
            short=prod[:38]+"…" if len(prod)>38 else prod
            st.markdown(f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #0f1729;font-size:0.78rem;"><span style="color:#94a3b8;">#{i} {short}</span><span style="color:#6366f1;font-weight:600;">{cnt}</span></div>',unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — SEGMENT EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
elif "Explorer" in page:
    st.markdown("""
<div class="hero-wrapper">
  <div class="hero-badge">📊 RFM Analysis · KMeans · Interactive Drill-Down</div>
  <h1 class="hero-title" style="font-size:2.6rem;">Customer Segment<br>Explorer</h1>
  <p class="hero-sub">Deep-dive into each behavioural segment. Filter, drill-down, compare — understand <span>who they are</span> and exactly how to market to them.</p>
</div>""",unsafe_allow_html=True)

    seg_tabs=st.tabs([s for s in all_segments]+["📋 Full Comparison"])

    for i,seg in enumerate(all_segments):
        with seg_tabs[i]:
            info=SEG_INFO.get(seg,SEG_INFO.get("Regular",{}))
            seg_data_full=rfm[rfm["Segment"]==seg]
            color=COLOR_MAP.get(seg,"#6366f1")

            # Local live drill-down filters — narrows the segment view further
            fcol1,fcol2=st.columns(2)
            with fcol1:
                m_min=st.slider("Min spend within segment (£)",0,int(seg_data_full["Monetary"].max()),0,key=f"mmin_{seg}")
            with fcol2:
                f_min=st.slider("Min orders within segment",1,int(seg_data_full["Frequency"].max()),1,key=f"fmin_{seg}")
            seg_data=seg_data_full[(seg_data_full["Monetary"]>=m_min)&(seg_data_full["Frequency"]>=f_min)]

            count=len(seg_data)
            avg_r=seg_data["Recency"].mean() if count else 0
            avg_f=seg_data["Frequency"].mean() if count else 0
            avg_m=seg_data["Monetary"].mean() if count else 0

            ca,cb=st.columns([1,2])
            with ca:
                st.markdown(f"""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:16px;padding:1.4rem;">
  <div style="font-size:2.5rem;margin-bottom:0.6rem;">{info.get('icon','📊')}</div>
  <div style="font-size:1.3rem;font-weight:800;color:#f1f5f9;margin-bottom:0.4rem;">{seg}</div>
  <div style="display:inline-block;background:{info.get('pill_bg','#1e293b')};color:{info.get('pill_color',color)};border:1px solid {info.get('pill_color',color)}44;border-radius:50px;padding:3px 14px;font-size:0.72rem;font-weight:700;margin-bottom:1rem;">{info.get('cta','')}</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:1rem;">
    <div style="background:#060b18;border-radius:10px;padding:0.7rem;text-align:center;">
      <div style="font-size:1.1rem;font-weight:800;color:{color};">{avg_r:.0f}d</div>
      <div style="font-size:0.6rem;color:#475569;text-transform:uppercase;">Recency</div>
    </div>
    <div style="background:#060b18;border-radius:10px;padding:0.7rem;text-align:center;">
      <div style="font-size:1.1rem;font-weight:800;color:{color};">{avg_f:.1f}x</div>
      <div style="font-size:0.6rem;color:#475569;text-transform:uppercase;">Frequency</div>
    </div>
    <div style="background:#060b18;border-radius:10px;padding:0.7rem;text-align:center;">
      <div style="font-size:1.1rem;font-weight:800;color:{color};">£{avg_m:,.0f}</div>
      <div style="font-size:0.6rem;color:#475569;text-transform:uppercase;">Avg Spend</div>
    </div>
  </div>
  <div style="background:#060b18;border-radius:10px;padding:0.8rem;font-size:0.78rem;color:#94a3b8;line-height:1.7;">{info.get('strategy','')}</div>
  <div style="margin-top:0.8rem;font-size:0.72rem;color:#334155;text-align:center;">{count} customers match filters · {count/len(rfm)*100:.1f}% of total base</div>
</div>""",unsafe_allow_html=True)

            with cb:
                if count==0:
                    st.info("No customers match the local filters above — widen the sliders.")
                else:
                    # Interactive chart selector
                    chart_sel=st.radio("Visualise",["Spend Histogram","Recency vs Frequency","Frequency Distribution","Monetary CDF"],horizontal=True,key=f"chart_{seg}")
                    compare_overlay=st.toggle("Overlay another segment for comparison",value=False,key=f"cmp_{seg}")
                    overlay_seg=None
                    if compare_overlay:
                        overlay_seg=st.selectbox("Compare against",[s for s in all_segments if s!=seg],key=f"cmpsel_{seg}")

                    cap95=seg_data["Monetary"].quantile(0.95)
                    seg_cap=seg_data[seg_data["Monetary"]<=cap95]

                    if chart_sel=="Spend Histogram":
                        bins_seg=st.slider("Bins",5,80,35,key=f"bins_{seg}")
                        fig=px.histogram(seg_cap,x="Monetary",nbins=bins_seg,template="plotly_dark",
                                         color_discrete_sequence=[color],opacity=0.85,
                                         labels={"Monetary":"Total Spend (£)","count":"Customers"})
                        if overlay_seg:
                            ov=rfm[rfm["Segment"]==overlay_seg]
                            ov=ov[ov["Monetary"]<=ov["Monetary"].quantile(0.95)]
                            fig.add_trace(go.Histogram(x=ov["Monetary"],nbinsx=bins_seg,name=overlay_seg,
                                                        marker_color=COLOR_MAP.get(overlay_seg,"#94a3b8"),opacity=0.5))
                        fig.update_layout(**PLOT_BASE,height=280,showlegend=bool(overlay_seg),barmode="overlay",
                                          title=dict(text="Spend Distribution",font=dict(size=13,color="#f1f5f9"),x=0))
                        st.plotly_chart(fig,use_container_width=True)

                    elif chart_sel=="Recency vs Frequency":
                        fig=px.scatter(seg_cap,x="Recency",y="Frequency",
                                       size=np.sqrt(seg_cap["Monetary"].clip(1)).values,
                                       color_discrete_sequence=[color],opacity=0.65,
                                       template="plotly_dark",size_max=20,
                                       hover_data={"Monetary":":.0f"},
                                       labels={"Recency":"Days Since Last Purchase","Frequency":"# Orders"})
                        fig.update_layout(**PLOT_BASE,height=280,showlegend=False,
                                          title=dict(text="Recency vs Frequency (size = spend)",font=dict(size=13,color="#f1f5f9"),x=0))
                        st.plotly_chart(fig,use_container_width=True)

                    elif chart_sel=="Frequency Distribution":
                        freq_cap=seg_data[seg_data["Frequency"]<=seg_data["Frequency"].quantile(0.95)]
                        fig=px.histogram(freq_cap,x="Frequency",nbins=30,template="plotly_dark",
                                         color_discrete_sequence=[color],
                                         labels={"Frequency":"Number of Orders"})
                        fig.update_layout(**PLOT_BASE,height=280,showlegend=False,
                                          title=dict(text="Order Frequency Distribution",font=dict(size=13,color="#f1f5f9"),x=0))
                        st.plotly_chart(fig,use_container_width=True)

                    else:  # CDF
                        sorted_m=np.sort(seg_cap["Monetary"].values)
                        cdf=np.arange(1,len(sorted_m)+1)/len(sorted_m)
                        fig=go.Figure(go.Scatter(x=sorted_m,y=cdf,mode="lines",
                                                 line=dict(color=color,width=2.5),fill="tozeroy",fillcolor=f"{color}22",
                                                 hovertemplate="£%{x:,.0f}<br>%{y:.1%} of customers<extra></extra>"))
                        fig.update_layout(**PLOT_BASE,height=280,
                                          xaxis_title="Total Spend (£)",yaxis_title="Cumulative %",
                                          yaxis=dict(tickformat=".0%",gridcolor="#0f1729"),
                                          title=dict(text="Cumulative Spend Distribution",font=dict(size=13,color="#f1f5f9"),x=0))
                        st.plotly_chart(fig,use_container_width=True)

                    # RFM percentile context
                    st.markdown(f"""
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:0.5rem;">
  <div style="background:#0f1729;border-radius:10px;padding:0.8rem;text-align:center;">
    <div style="font-size:0.65rem;color:#475569;text-transform:uppercase;margin-bottom:4px;">Min Spend</div>
    <div style="font-size:0.95rem;font-weight:700;color:#f1f5f9;">£{seg_data['Monetary'].min():,.0f}</div>
  </div>
  <div style="background:#0f1729;border-radius:10px;padding:0.8rem;text-align:center;">
    <div style="font-size:0.65rem;color:#475569;text-transform:uppercase;margin-bottom:4px;">Median Spend</div>
    <div style="font-size:0.95rem;font-weight:700;color:{color};">£{seg_data['Monetary'].median():,.0f}</div>
  </div>
  <div style="background:#0f1729;border-radius:10px;padding:0.8rem;text-align:center;">
    <div style="font-size:0.65rem;color:#475569;text-transform:uppercase;margin-bottom:4px;">Max Spend</div>
    <div style="font-size:0.95rem;font-weight:700;color:#f1f5f9;">£{seg_data['Monetary'].max():,.0f}</div>
  </div>
</div>""",unsafe_allow_html=True)

    # Full Comparison Tab
    with seg_tabs[-1]:
        st.markdown('<div class="section-eyebrow">✦ Comparison</div><div class="section-title">All Segments Side-by-Side</div><div class="section-sub">Select metric to compare visually</div>',unsafe_allow_html=True)
        metric_sel=st.radio("Compare by",["Avg Spend","Avg Recency","Avg Frequency","Customer Count"],horizontal=True,key="comp_metric")
        metric_map={"Avg Spend":"Monetary","Avg Recency":"Recency","Avg Frequency":"Frequency","Customer Count":"CustomerID"}
        m=metric_map[metric_sel]
        if m=="CustomerID":
            comp=rfm.groupby("Segment")["CustomerID"].count().reset_index()
            comp.columns=["Segment","Value"]
        else:
            comp=rfm.groupby("Segment")[m].mean().reset_index()
            comp.columns=["Segment","Value"]

        fig_comp=px.bar(comp,x="Segment",y="Value",color="Segment",
                        color_discrete_map=COLOR_MAP,template="plotly_dark",
                        text=comp["Value"].apply(lambda x: f"£{x:,.0f}" if "Spend" in metric_sel else f"{x:,.1f}"),
                        labels={"Value":metric_sel,"Segment":""})
        fig_comp.update_traces(textposition="outside",textfont_color="#94a3b8")
        fig_comp.update_layout(**PLOT_BASE,height=320,showlegend=False,
                               title=dict(text=f"{metric_sel} by Segment",font=dict(size=14,color="#f1f5f9"),x=0))
        st.plotly_chart(fig_comp,use_container_width=True)

        profile=rfm.groupby("Segment").agg(
            Customers=("CustomerID","count"),
            Avg_Recency=("Recency","mean"),
            Avg_Frequency=("Frequency","mean"),
            Avg_Spend=("Monetary","mean"),
            Total_Revenue=("Monetary","sum"),
        ).round(1)
        profile["% of Base"]=(profile["Customers"]/profile["Customers"].sum()*100).round(1).astype(str)+"%"
        profile["Avg_Spend"]=profile["Avg_Spend"].apply(lambda x:f"£{x:,.0f}")
        profile["Total_Revenue"]=profile["Total_Revenue"].apply(lambda x:f"£{x:,.0f}")
        profile.columns=["Customers","Avg Recency","Avg Frequency","Avg Spend","Total Revenue","% of Base"]
        st.dataframe(profile,use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — LIVE PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
elif "Predictor" in page:
    st.markdown("""
<div class="hero-wrapper">
  <div class="hero-badge">🔮 Real-Time KMeans Prediction Engine</div>
  <h1 class="hero-title" style="font-size:2.6rem;">Predict Any Customer's<br>Segment Instantly</h1>
  <p class="hero-sub">Enter <span>Recency, Frequency & Monetary</span> values — or use the presets — and the model classifies them <span>live, as you type</span>, with full strategy recommendations.</p>
</div>""",unsafe_allow_html=True)

    # Presets
    st.markdown('<div class="section-eyebrow">✦ Quick Presets</div><div class="section-title">Try a Customer Profile</div><div class="section-sub">Click any preset to auto-fill the values</div>',unsafe_allow_html=True)
    presets={"🏆 Champion":(5,50,8000),"💰 Big Spender":(25,8,15000),"😴 Dormant":(300,1,120),"🔄 Loyal Regular":(20,20,2500),"⚠️ At Risk":(200,2,400),"🆕 New Customer":(10,1,85)}
    preset_cols=st.columns(len(presets))
    for col,(name,vals) in zip(preset_cols,presets.items()):
        with col:
            if st.button(name,key=f"pre_{name}"):
                st.session_state["preset_r"]=vals[0]
                st.session_state["preset_f"]=vals[1]
                st.session_state["preset_m"]=vals[2]

    st.markdown("---")
    col_l,col_m,col_r=st.columns([1.1,1.1,0.9])

    with col_l:
        st.markdown('<div class="section-eyebrow">✦ Input</div><div class="section-title">Customer RFM Values</div>',unsafe_allow_html=True)
        recency=st.number_input("📅 Recency (days since last purchase)",1,730,st.session_state.get("preset_r",45),help="Lower = more recent = better")
        frequency=st.number_input("🔁 Frequency (number of orders)",1,500,st.session_state.get("preset_f",8),help="Higher = more loyal")
        monetary=st.number_input("💷 Monetary (total spend £)",1.0,500000.0,float(st.session_state.get("preset_m",1200)),step=100.0,help="Higher = more valuable")

        st.markdown("""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:1rem;margin-top:0.8rem;">
  <div style="font-size:0.68rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.7rem;">RFM Benchmarks</div>
  <div style="font-size:0.78rem;color:#64748b;line-height:2.1;">
    📅 <b style="color:#94a3b8;">Recency:</b> &lt;30d = Champion · &gt;180d = At-Risk<br>
    🔁 <b style="color:#94a3b8;">Frequency:</b> 1-2 = Rare · 10+ = Loyal<br>
    💷 <b style="color:#94a3b8;">Monetary:</b> &lt;£500 = Low · £5,000+ = VIP
  </div>
</div>""",unsafe_allow_html=True)

        save_scenario=st.button("💾  Save This Scenario to History",key="predict_main")

    # Prediction now runs live on every rerun (i.e. on every input change) —
    # no button required to see the result.
    X_scaled=scaler.transform([[recency,frequency,monetary]])
    cluster_id=kmeans.predict(X_scaled)[0]
    segment=cluster_label_map[cluster_id]
    info=SEG_INFO.get(segment,SEG_INFO.get("Regular",{}))
    color=COLOR_MAP.get(segment,"#6366f1")
    distances=kmeans.transform(X_scaled)[0]
    confidence=max(0,min(100,int((1-distances.min()/(distances.max()+1e-9))*100)))

    if save_scenario:
        st.session_state.scenario_history.append({
            "Recency":recency,"Frequency":frequency,"Monetary":monetary,
            "Segment":segment,"Confidence":f"{confidence}%"
        })

    with col_m:
        st.markdown('<div class="section-eyebrow">✦ Live Result</div><div class="section-title">Prediction Output</div>',unsafe_allow_html=True)
        st.markdown(f"""
<div class="pred-box">
  <div style="font-size:2.8rem;margin-bottom:0.4rem;">{info.get('icon','📊')}</div>
  <div style="font-size:0.68rem;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;">Predicted Segment</div>
  <div class="pred-seg" style="color:{color};">{segment}</div>
  <div style="display:inline-block;background:{info.get('pill_bg','#1e293b')};color:{info.get('pill_color',color)};border:1px solid {info.get('pill_color',color)}44;border-radius:50px;padding:4px 16px;font-size:0.72rem;font-weight:700;margin-bottom:1rem;">{info.get('cta','')}</div>
  <div style="margin-bottom:1rem;">
    <div style="font-size:0.68rem;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:5px;">MODEL CONFIDENCE</div>
    <div style="background:#0f1729;border-radius:6px;height:10px;overflow:hidden;margin-bottom:4px;">
      <div style="width:{confidence}%;height:100%;background:linear-gradient(90deg,{color},{color}88);border-radius:6px;"></div>
    </div>
    <div style="font-size:0.8rem;color:{color};font-weight:700;">{confidence}% confident</div>
  </div>
  <div style="font-size:0.83rem;color:#94a3b8;line-height:1.7;max-width:320px;margin:0 auto;">{info.get('strategy','')}</div>
</div>""",unsafe_allow_html=True)

        st.markdown(f"""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:1rem;margin-top:0.8rem;">
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;text-align:center;">
    <div><div style="font-size:1rem;font-weight:800;color:#f1f5f9;">{recency}d</div><div style="font-size:0.62rem;color:#475569;text-transform:uppercase;">Recency</div></div>
    <div><div style="font-size:1rem;font-weight:800;color:#f1f5f9;">{frequency}x</div><div style="font-size:0.62rem;color:#475569;text-transform:uppercase;">Frequency</div></div>
    <div><div style="font-size:1rem;font-weight:800;color:#f1f5f9;">£{monetary:,.0f}</div><div style="font-size:0.62rem;color:#475569;text-transform:uppercase;">Monetary</div></div>
  </div>
</div>""",unsafe_allow_html=True)

        st.markdown("**Distance to each cluster centroid:**")
        max_dist=max(distances) if len(distances) else 1
        for cid,dist in enumerate(distances):
            seg_name=cluster_label_map.get(cid,"Unknown")
            c=COLOR_MAP.get(seg_name,"#6366f1")
            is_pred=cid==cluster_id
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;margin:4px 0;">
  <div style="width:90px;font-size:0.72rem;color:{'#f1f5f9' if is_pred else '#475569'};font-weight:{'700' if is_pred else '400'};">{seg_name[:12]}</div>
  <div style="flex:1;background:#0f1729;border-radius:4px;height:6px;overflow:hidden;">
    <div style="width:{min(100,int(dist/max_dist*100))}%;height:100%;background:{c};opacity:{'1' if is_pred else '0.3'};border-radius:4px;"></div>
  </div>
  <div style="font-size:0.72rem;color:{c};width:50px;text-align:right;font-weight:{'700' if is_pred else '400'};">{dist:.2f}</div>
</div>""",unsafe_allow_html=True)

        if st.session_state.scenario_history:
            st.markdown("---")
            st.markdown('<div class="section-eyebrow">✦ History</div><div class="section-title">Saved Scenarios</div>',unsafe_allow_html=True)
            hist_df=pd.DataFrame(st.session_state.scenario_history)
            st.dataframe(hist_df,use_container_width=True,height=min(220,44+32*len(hist_df)))
            if st.button("🗑️ Clear history",key="clear_hist"):
                st.session_state.scenario_history=[]
                st.rerun()

    with col_r:
        st.markdown('<div class="section-eyebrow">✦ Context</div><div class="section-title">Segment Benchmarks</div>',unsafe_allow_html=True)
        profile=rfm.groupby("Segment")[["Recency","Frequency","Monetary"]].mean().round(1)
        for seg_name,row in profile.iterrows():
            c=COLOR_MAP.get(seg_name,"#6366f1")
            is_current=seg_name==segment
            border=f"2px solid {c}" if is_current else "1px solid #1e293b"
            st.markdown(f"""
<div style="background:#0f1729;border:{border};border-radius:12px;padding:0.9rem;margin-bottom:0.5rem;">
  <div style="font-size:0.82rem;font-weight:700;color:{c};margin-bottom:0.4rem;">{seg_name}</div>
  <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#64748b;">
    <span>R: <b style="color:#94a3b8;">{row['Recency']:.0f}d</b></span>
    <span>F: <b style="color:#94a3b8;">{row['Frequency']:.1f}x</b></span>
    <span>M: <b style="color:#94a3b8;">£{row['Monetary']:,.0f}</b></span>
  </div>
</div>""",unsafe_allow_html=True)

        from sklearn.preprocessing import MinMaxScaler
        mms=MinMaxScaler()
        normed=pd.DataFrame(mms.fit_transform(profile),columns=profile.columns,index=profile.index)
        user_n=mms.transform([[recency,frequency,monetary]])[0]
        cats=["Recency","Frequency","Monetary"]
        fig=go.Figure()
        for s,row in normed.iterrows():
            c=COLOR_MAP.get(s,"#6366f1")
            v=row.tolist()+[row.tolist()[0]]
            fig.add_trace(go.Scatterpolar(r=v,theta=cats+[cats[0]],name=s,
                line=dict(color=c,width=1.5),fill='toself',fillcolor=c,opacity=0.08))
        uv=user_n.tolist()+[user_n[0]]
        fig.add_trace(go.Scatterpolar(r=uv,theta=cats+[cats[0]],name="You ◉",
            line=dict(color="#ffffff",width=2.5,dash="dot"),fill='toself',fillcolor="#ffffff",opacity=0.07))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                          polar=dict(bgcolor="#0a0f1e",
                                     radialaxis=dict(gridcolor="#1e293b",tickfont=dict(size=8)),
                                     angularaxis=dict(gridcolor="#1e293b")),
                          legend=dict(font=dict(color="#64748b",size=8),bgcolor="rgba(0,0,0,0)"),
                          margin=dict(t=20,b=10,l=10,r=10),height=280,
                          title=dict(text="Your RFM vs Segments (live)",font=dict(size=12,color="#f1f5f9"),x=0))
        st.plotly_chart(fig,use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — RFM DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
elif "Deep Dive" in page:
    st.markdown("""
<div class="hero-wrapper">
  <div class="hero-badge">📊 Interactive RFM Analysis · Filter · Drill-Down · Export</div>
  <h1 class="hero-title" style="font-size:2.6rem;">RFM Deep Dive<br>Analytics</h1>
  <p class="hero-sub">Explore the full RFM dataset interactively. Filter by any dimension, visualise distributions, and identify your most valuable customer cohorts.</p>
</div>""",unsafe_allow_html=True)

    # Interactive filters
    st.markdown('<div class="filter-bar">',unsafe_allow_html=True)
    st.markdown('<div class="filter-label">🎛️ Interactive Filters</div>',unsafe_allow_html=True)
    f1,f2,f3,f4=st.columns(4)
    with f1:
        r_range=st.slider("Recency (days)",int(rfm["Recency"].min()),int(rfm["Recency"].max()),(0,int(rfm["Recency"].max())),key="r_range")
    with f2:
        f_range=st.slider("Frequency (orders)",int(rfm["Frequency"].min()),int(rfm["Frequency"].max()),(1,int(rfm["Frequency"].max())),key="f_range")
    with f3:
        m_range=st.slider("Monetary (£)",int(rfm["Monetary"].min()),min(int(rfm["Monetary"].max()),50000),(0,10000),key="m_range")
    with f4:
        seg_filter=st.multiselect("Segments",all_segments,default=all_segments,key="dd_seg")
    st.markdown('</div>',unsafe_allow_html=True)

    rfm_dd=rfm[
        (rfm["Recency"]>=r_range[0])&(rfm["Recency"]<=r_range[1])&
        (rfm["Frequency"]>=f_range[0])&(rfm["Frequency"]<=f_range[1])&
        (rfm["Monetary"]>=m_range[0])&(rfm["Monetary"]<=m_range[1])&
        (rfm["Segment"].isin(seg_filter if seg_filter else all_segments))
    ]

    top_row=st.columns([3,1])
    with top_row[0]:
        st.markdown(f"""
<div style="background:#0f1729;border:1px solid #1e293b;border-radius:12px;padding:0.8rem 1.2rem;margin-bottom:1rem;display:flex;align-items:center;gap:2rem;">
  <div><span style="font-size:1.4rem;font-weight:800;color:#6366f1;">{len(rfm_dd):,}</span> <span style="font-size:0.78rem;color:#64748b;">customers match your filters</span></div>
  <div><span style="font-size:1rem;font-weight:700;color:#4ade80;">£{rfm_dd['Monetary'].sum():,.0f}</span> <span style="font-size:0.78rem;color:#64748b;">total revenue</span></div>
  <div><span style="font-size:1rem;font-weight:700;color:#22d3ee;">{rfm_dd['Frequency'].sum():,}</span> <span style="font-size:0.78rem;color:#64748b;">total orders</span></div>
  <div><span style="font-size:1rem;font-weight:700;color:#facc15;">{rfm_dd['Recency'].mean():.0f}d</span> <span style="font-size:0.78rem;color:#64748b;">avg recency</span></div>
</div>""",unsafe_allow_html=True)
    with top_row[1]:
        st.download_button("⬇️ Export CSV",rfm_dd.to_csv(index=False).encode("utf-8"),
                           file_name="rfm_filtered.csv",mime="text/csv",key="dd_export")

    tab1,tab2,tab3,tab4,tab5=st.tabs(["📊 Distributions","🗺️ 3D Explorer","📈 Correlations","📋 Data Table","⚖️ Cohort Compare"])

    with tab1:
        d1,d2,d3=st.columns(3)
        for col,metric,color_hex in [(d1,"Recency","#6366f1"),(d2,"Frequency","#22d3ee"),(d3,"Monetary","#f472b6")]:
            with col:
                cap=rfm_dd[metric].quantile(0.95)
                data=rfm_dd[rfm_dd[metric]<=cap][metric]
                fig=px.histogram(data,nbins=40,template="plotly_dark",
                                 color_discrete_sequence=[color_hex],
                                 labels={metric:metric,"count":"Customers"})
                fig.add_vline(x=data.mean(),line_color="#facc15",line_dash="dash",
                              annotation_text=f"Mean: {data.mean():.0f}",
                              annotation_font_color="#facc15",annotation_font_size=10)
                fig.update_layout(**PLOT_BASE,height=240,showlegend=False,
                                  title=dict(text=metric,font=dict(size=13,color="#f1f5f9"),x=0))
                st.plotly_chart(fig,use_container_width=True)

    with tab2:
        from sklearn.decomposition import PCA
        if len(rfm_dd)>3:
            pca=PCA(n_components=3,random_state=42)
            from sklearn.preprocessing import StandardScaler as SS
            ss=SS()
            coords=pca.fit_transform(ss.fit_transform(rfm_dd[["Recency","Frequency","Monetary"]]))
            rfm_3d=rfm_dd.copy()
            rfm_3d["PC1"]=coords[:,0]; rfm_3d["PC2"]=coords[:,1]; rfm_3d["PC3"]=coords[:,2]
            fig3d=px.scatter_3d(rfm_3d,x="PC1",y="PC2",z="PC3",color="Segment",
                                color_discrete_map=COLOR_MAP,opacity=0.65,template="plotly_dark",
                                hover_data={"Monetary":":.0f","Recency":True,"Frequency":True})
            fig3d.update_traces(marker=dict(size=2.5))
            fig3d.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                scene=dict(bgcolor="#0a0f1e",
                                           xaxis=dict(gridcolor="#1e293b",backgroundcolor="#0a0f1e"),
                                           yaxis=dict(gridcolor="#1e293b",backgroundcolor="#0a0f1e"),
                                           zaxis=dict(gridcolor="#1e293b",backgroundcolor="#0a0f1e")),
                                height=500,margin=dict(t=20,b=10,l=10,r=10),
                                legend=dict(font=dict(color="#94a3b8",size=10),bgcolor="rgba(0,0,0,0)"),
                                title=dict(text=f"3D PCA — {pca.explained_variance_ratio_.sum()*100:.0f}% variance explained",
                                           font=dict(size=13,color="#f1f5f9"),x=0))
            st.plotly_chart(fig3d,use_container_width=True)
        else:
            st.info("Widen your filters — need more than 3 customers for a 3D PCA view.")

    with tab3:
        c1,c2=st.columns(2)
        with c1:
            x_ax=st.selectbox("X Axis",["Recency","Frequency","Monetary"],index=0,key="corr_x")
        with c2:
            y_ax=st.selectbox("Y Axis",["Recency","Frequency","Monetary"],index=2,key="corr_y")
        rfm_corr=rfm_dd[rfm_dd["Monetary"]<=rfm_dd["Monetary"].quantile(0.95)]
        fig_corr=px.scatter(rfm_corr,x=x_ax,y=y_ax,color="Segment",
                            color_discrete_map=COLOR_MAP,opacity=0.6,template="plotly_dark",
                            trendline="ols",trendline_scope="overall",
                            trendline_color_override="#ffffff",
                            hover_data={"Monetary":":.0f"})
        fig_corr.update_layout(**PLOT_BASE,height=380,
                               legend=dict(orientation="h",yanchor="bottom",y=1.02,font=dict(size=9),bgcolor="rgba(0,0,0,0)"),
                               title=dict(text=f"{x_ax} vs {y_ax} — with trend line",font=dict(size=13,color="#f1f5f9"),x=0))
        st.plotly_chart(fig_corr,use_container_width=True)
        corr_val=rfm_dd[[x_ax,y_ax]].corr().iloc[0,1]
        st.markdown(f'<div style="text-align:center;font-size:0.85rem;color:#64748b;">Pearson Correlation: <b style="color:{"#4ade80" if abs(corr_val)>0.5 else "#facc15" if abs(corr_val)>0.2 else "#f87171"};">{corr_val:.4f}</b></div>',unsafe_allow_html=True)

    with tab4:
        st.dataframe(
            rfm_dd[["CustomerID","Segment","Recency","Frequency","Monetary"]].sort_values("Monetary",ascending=False).head(200),
            use_container_width=True, height=400
        )
        st.markdown(f'<div style="font-size:0.75rem;color:#475569;margin-top:0.5rem;">Showing top 200 by spend · {len(rfm_dd):,} total customers match filters</div>',unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="section-sub">Define two cohorts from the current filtered pool and compare them side-by-side.</div>',unsafe_allow_html=True)
        cohA,cohB=st.columns(2)
        with cohA:
            st.markdown("**Cohort A**")
            segA=st.multiselect("Segments A",all_segments,default=all_segments[:1],key="cohA_seg")
            mA=st.slider("Min spend A (£)",0,int(rfm_dd["Monetary"].max() or 1),0,key="cohA_m")
        with cohB:
            st.markdown("**Cohort B**")
            segB=st.multiselect("Segments B",all_segments,default=all_segments[-1:],key="cohB_seg")
            mB=st.slider("Min spend B (£)",0,int(rfm_dd["Monetary"].max() or 1),0,key="cohB_m")

        A=rfm_dd[(rfm_dd["Segment"].isin(segA))&(rfm_dd["Monetary"]>=mA)]
        B=rfm_dd[(rfm_dd["Segment"].isin(segB))&(rfm_dd["Monetary"]>=mB)]

        comp_tbl=pd.DataFrame({
            "Cohort A":[len(A),f"£{A['Monetary'].mean():,.0f}" if len(A) else "-",f"{A['Frequency'].mean():.1f}x" if len(A) else "-",f"{A['Recency'].mean():.0f}d" if len(A) else "-",f"£{A['Monetary'].sum():,.0f}" if len(A) else "£0"],
            "Cohort B":[len(B),f"£{B['Monetary'].mean():,.0f}" if len(B) else "-",f"{B['Frequency'].mean():.1f}x" if len(B) else "-",f"{B['Recency'].mean():.0f}d" if len(B) else "-",f"£{B['Monetary'].sum():,.0f}" if len(B) else "£0"],
        },index=["Customers","Avg Spend","Avg Frequency","Avg Recency","Total Revenue"])
        st.dataframe(comp_tbl,use_container_width=True)

        if len(A) and len(B):
            fig_cmp=go.Figure()
            fig_cmp.add_trace(go.Bar(name="Cohort A",x=["Recency","Frequency","Monetary"],
                                      y=[A["Recency"].mean(),A["Frequency"].mean(),A["Monetary"].mean()/10],
                                      marker_color="#6366f1"))
            fig_cmp.add_trace(go.Bar(name="Cohort B",x=["Recency","Frequency","Monetary"],
                                      y=[B["Recency"].mean(),B["Frequency"].mean(),B["Monetary"].mean()/10],
                                      marker_color="#f472b6"))
            fig_cmp.update_layout(**PLOT_BASE,height=300,barmode="group",
                                  title=dict(text="Cohort A vs B (Monetary shown ÷10 for scale)",font=dict(size=13,color="#f1f5f9"),x=0),
                                  legend=dict(font=dict(color="#94a3b8",size=10),bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_cmp,use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 0.5rem;border-top:1px solid #0f1729;margin-top:2rem;">
  <div style="font-size:0.68rem;color:#1e293b;letter-spacing:0.08em;text-transform:uppercase;">
    Shopper Spectrum · AI-Powered Retail Intelligence · Pandas · Scikit-learn · Plotly · Streamlit
  </div>
</div>""",unsafe_allow_html=True)
