"""
🛒 Shopper Spectrum — Streamlit Application
Customer Segmentation + Product Recommendation Engine
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Shopper Spectrum",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background: #0f172a; }

    .hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-size: 2.4rem; font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #22d3ee, #f472b6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-sub { color: #94a3b8; font-size: 1rem; margin-top: 0.3rem; }

    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        text-align: center;
    }
    .metric-val { font-size: 2rem; font-weight: 700; color: #6366f1; }
    .metric-lbl { font-size: 0.8rem; color: #94a3b8; margin-top: 0.2rem; }

    .rec-card {
        background: linear-gradient(135deg, #1e293b, #162032);
        border: 1px solid #334155;
        border-left: 4px solid #6366f1;
        border-radius: 10px;
        padding: 0.85rem 1.2rem;
        margin: 0.4rem 0;
    }
    .rec-rank { color: #6366f1; font-weight: 700; font-size: 1.1rem; }
    .rec-name { color: #f1f5f9; font-weight: 500; margin-top: 0.1rem; }
    .rec-score { color: #22d3ee; font-size: 0.85rem; }

    .seg-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        margin: 0.5rem 0;
    }
    .seg-high   { background: #1a2f1a; color: #4ade80; border: 1px solid #4ade80; }
    .seg-regular{ background: #1a1f35; color: #6366f1; border: 1px solid #6366f1; }
    .seg-occasional { background: #2a1f0f; color: #facc15; border: 1px solid #facc15; }
    .seg-atrisk { background: #2a0f0f; color: #f87171; border: 1px solid #f87171; }

    .section-header {
        font-size: 1.3rem; font-weight: 600; color: #f1f5f9;
        border-bottom: 2px solid #334155;
        padding-bottom: 0.5rem; margin: 1.5rem 0 1rem 0;
    }
    .info-box {
        background: #1e293b; border: 1px solid #334155;
        border-radius: 10px; padding: 1rem 1.2rem;
        color: #94a3b8; font-size: 0.88rem; line-height: 1.6;
    }
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white; border: none; border-radius: 8px;
        padding: 0.6rem 1.8rem; font-weight: 600;
        width: 100%; transition: all 0.2s;
    }
    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #818cf8, #6366f1);
        transform: translateY(-1px); box-shadow: 0 4px 15px rgba(99,102,241,0.4);
    }
    .stNumberInput > div > div > input {
        background: #1e293b; border: 1px solid #334155;
        color: #f1f5f9; border-radius: 8px;
    }
    .stTextInput > div > div > input {
        background: #1e293b; border: 1px solid #334155;
        color: #f1f5f9; border-radius: 8px;
    }
    .stSelectbox > div { background: #1e293b; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ── Load Models ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    with open("models/kmeans_model.pkl", "rb") as f:
        kmeans = pickle.load(f)
    with open("models/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("models/cluster_label_map.pkl", "rb") as f:
        cluster_label_map = pickle.load(f)
    item_sim_df = pd.read_pickle("models/item_sim_df.pkl")
    rfm = pd.read_csv("models/rfm_segmented.csv")
    return kmeans, scaler, cluster_label_map, item_sim_df, rfm

kmeans, scaler, cluster_label_map, item_sim_df, rfm = load_models()

SEGMENT_STYLES = {
    "High-Value 🏆": ("seg-high",   "#4ade80", "🏆 Premium customer. Reward with exclusive offers & loyalty perks."),
    "Regular 🔄":    ("seg-regular","#6366f1", "🔄 Consistent buyer. Upsell with bundles and seasonal campaigns."),
    "Occasional 💤": ("seg-occasional","#facc15","💤 Infrequent buyer. Re-engage with limited-time deals."),
    "At-Risk ⚠️":   ("seg-atrisk", "#f87171", "⚠️ Churning customer. Trigger win-back campaigns immediately."),
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛒 Shopper Spectrum")
    st.markdown("---")
    page = st.radio("Navigate", ["🏠 Overview", "🎯 Product Recommender", "👥 Customer Segmentation"])
    st.markdown("---")
    st.markdown("""
<div class="info-box">
<b>📌 About</b><br><br>
<b>Model:</b> KMeans (k=4)<br>
<b>Silhouette:</b> 0.6162<br>
<b>Similarity:</b> Cosine<br>
<b>Products:</b> 500 top items<br>
<b>Customers:</b> 4,338
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown("""
<div class="hero-card">
  <div class="hero-title">🛒 Shopper Spectrum</div>
  <div class="hero-sub">Customer Segmentation &amp; Product Recommendation Engine · E-Commerce Analytics</div>
</div>
""", unsafe_allow_html=True)

    # KPI row
    seg_counts = rfm["Segment"].value_counts()
    total_customers = len(rfm)
    high_value = seg_counts.get("High-Value 🏆", 0)
    at_risk = seg_counts.get("At-Risk ⚠️", 0)
    avg_monetary = rfm["Monetary"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, val, lbl in [
        (c1, f"{total_customers:,}", "Total Customers"),
        (c2, f"{high_value}", "High-Value"),
        (c3, f"{at_risk}", "At-Risk"),
        (c4, f"£{avg_monetary:,.0f}", "Avg. Spend"),
        (c5, f"{len(item_sim_df)}", "Products Indexed"),
    ]:
        col.markdown(f"""
<div class="metric-card">
  <div class="metric-val">{val}</div>
  <div class="metric-lbl">{lbl}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-header">📊 Customer Segment Distribution</div>', unsafe_allow_html=True)
        seg_df = rfm["Segment"].value_counts().reset_index()
        seg_df.columns = ["Segment", "Count"]
        COLOR_MAP = {
            "High-Value 🏆": "#4ade80",
            "Regular 🔄":    "#6366f1",
            "Occasional 💤": "#facc15",
            "At-Risk ⚠️":   "#f87171",
        }
        fig_pie = px.pie(seg_df, values="Count", names="Segment",
                         color="Segment", color_discrete_map=COLOR_MAP,
                         hole=0.55, template="plotly_dark")
        fig_pie.update_layout(
            paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
            legend=dict(font=dict(color="#94a3b8")),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        fig_pie.update_traces(textfont_color="white")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">💰 RFM Monetary Box Plot by Segment</div>', unsafe_allow_html=True)
        rfm_capped = rfm[rfm["Monetary"] <= rfm["Monetary"].quantile(0.95)]
        fig_box = px.box(rfm_capped, x="Segment", y="Monetary",
                         color="Segment", color_discrete_map=COLOR_MAP,
                         template="plotly_dark",
                         labels={"Monetary": "Total Spend (£)"})
        fig_box.update_layout(
            paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
            showlegend=False, xaxis_title="",
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown('<div class="section-header">🔵 RFM Scatter — Recency vs Frequency (size = Monetary)</div>', unsafe_allow_html=True)
    rfm_s = rfm[rfm["Monetary"] < rfm["Monetary"].quantile(0.97)].copy()
    rfm_s["MonetaryScaled"] = np.sqrt(rfm_s["Monetary"]).clip(5, 40)
    fig_scatter = px.scatter(rfm_s, x="Recency", y="Frequency",
                             size="MonetaryScaled", color="Segment",
                             color_discrete_map=COLOR_MAP, opacity=0.7,
                             template="plotly_dark",
                             labels={"Recency": "Recency (days)", "Frequency": "Frequency (orders)"},
                             hover_data={"Monetary": ":.0f", "MonetaryScaled": False})
    fig_scatter.update_layout(
        paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
        margin=dict(t=10, b=30, l=30, r=10), height=450
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRODUCT RECOMMENDER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎯 Product Recommender":
    st.markdown("""
<div class="hero-card">
  <div class="hero-title">🎯 Product Recommender</div>
  <div class="hero-sub">Item-Based Collaborative Filtering · Cosine Similarity</div>
</div>
""", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.2, 1])

    with col_l:
        st.markdown('<div class="section-header">🔍 Find Similar Products</div>', unsafe_allow_html=True)

        # Dropdown of all indexed products
        all_products = sorted(item_sim_df.index.tolist())
        selected_product = st.selectbox("Select a product", all_products,
                                         index=all_products.index("WHITE HANGING HEART T-LIGHT HOLDER")
                                         if "WHITE HANGING HEART T-LIGHT HOLDER" in all_products else 0)

        top_n = st.slider("Number of recommendations", min_value=3, max_value=10, value=5)

        if st.button("🚀 Get Recommendations"):
            similar = (item_sim_df[selected_product]
                       .drop(selected_product)
                       .sort_values(ascending=False)
                       .head(top_n))

            st.markdown(f"**Recommendations for:** `{selected_product}`")
            for rank, (prod, score) in enumerate(similar.items(), 1):
                st.markdown(f"""
<div class="rec-card">
  <span class="rec-rank">#{rank}</span>
  <div class="rec-name">{prod}</div>
  <div class="rec-score">Similarity: {score:.4f}</div>
</div>""", unsafe_allow_html=True)

            # Bar chart
            fig_bar = px.bar(
                x=similar.values, y=similar.index,
                orientation="h", template="plotly_dark",
                color=similar.values,
                color_continuous_scale=["#334155", "#6366f1", "#22d3ee"],
                labels={"x": "Cosine Similarity", "y": ""},
            )
            fig_bar.update_layout(
                paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
                coloraxis_showscale=False,
                margin=dict(t=10, b=10, l=10, r=10), height=300,
                yaxis=dict(categoryorder="total ascending")
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-header">ℹ️ How It Works</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="info-box">
<b>Algorithm:</b> Item-Based Collaborative Filtering<br><br>
<b>Step 1:</b> Build a Customer × Product matrix (500 top products)<br><br>
<b>Step 2:</b> Compute pairwise <b>Cosine Similarity</b> between all product vectors<br><br>
<b>Step 3:</b> For any product, return the top-N most similar items<br><br>
<b>Score Range:</b> 0 (no similarity) → 1 (identical purchase pattern)<br><br>
<i>Products frequently bought together by the same customers will have high similarity scores.</i>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="section-header">📦 Top 10 Most Popular Products</div>', unsafe_allow_html=True)
        # Show top products from sim matrix (by number of non-zero similarities)
        top_items = (item_sim_df > 0.3).sum().sort_values(ascending=False).head(10)
        for i, (prod, cnt) in enumerate(top_items.items(), 1):
            short = prod[:45] + "..." if len(prod) > 45 else prod
            st.markdown(f"**{i}.** {short} *(linked to {cnt} products)*")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — CUSTOMER SEGMENTATION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👥 Customer Segmentation":
    st.markdown("""
<div class="hero-card">
  <div class="hero-title">👥 Customer Segmentation</div>
  <div class="hero-sub">RFM Analysis · KMeans Clustering (k=4) · Silhouette Score: 0.6162</div>
</div>
""", unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1.2])

    with col_l:
        st.markdown('<div class="section-header">🔮 Predict Customer Segment</div>', unsafe_allow_html=True)
        st.markdown("Enter the customer's RFM values to predict their segment.")

        recency   = st.number_input("📅 Recency (days since last purchase)", min_value=1, max_value=730, value=30, step=1)
        frequency = st.number_input("🔁 Frequency (number of orders)", min_value=1, max_value=500, value=10, step=1)
        monetary  = st.number_input("💷 Monetary (total spend in £)", min_value=1.0, max_value=500000.0, value=1500.0, step=50.0)

        if st.button("🎯 Predict Cluster"):
            X = np.array([[recency, frequency, monetary]])
            X_scaled = scaler.transform(X)
            cluster_id = kmeans.predict(X_scaled)[0]
            segment = cluster_label_map[cluster_id]

            style_class, color, advice = SEGMENT_STYLES.get(
                segment, ("seg-regular","#6366f1","Keep monitoring this customer."))

            st.markdown(f"""
<br>
<div style="background:#1e293b;border:1px solid #334155;border-radius:14px;padding:1.5rem;">
  <div style="color:#94a3b8;font-size:0.85rem;margin-bottom:0.3rem;">Predicted Segment</div>
  <span class="seg-badge {style_class}">{segment}</span>
  <div style="margin-top:1rem;color:#cbd5e1;font-size:0.9rem;line-height:1.6;">
    {advice}
  </div>
  <hr style="border-color:#334155;margin:1rem 0;">
  <div style="display:flex;gap:2rem;">
    <div><div style="color:#94a3b8;font-size:0.78rem;">Recency</div><div style="color:#f1f5f9;font-weight:600;">{recency} days</div></div>
    <div><div style="color:#94a3b8;font-size:0.78rem;">Frequency</div><div style="color:#f1f5f9;font-weight:600;">{frequency} orders</div></div>
    <div><div style="color:#94a3b8;font-size:0.78rem;">Monetary</div><div style="color:#f1f5f9;font-weight:600;">£{monetary:,.0f}</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

            # Radar chart
            seg_profiles = rfm.groupby("Segment")[["Recency","Frequency","Monetary"]].mean()
            from sklearn.preprocessing import MinMaxScaler
            mms = MinMaxScaler()
            normed = pd.DataFrame(mms.fit_transform(seg_profiles), columns=seg_profiles.columns, index=seg_profiles.index)
            user_normed = mms.transform(X)[0]

            categories = ["Recency", "Frequency", "Monetary"]
            fig_radar = go.Figure()
            for seg_name, row in normed.iterrows():
                vals = row.tolist() + [row.tolist()[0]]
                c = SEGMENT_STYLES.get(seg_name, ("","#6366f1",""))[1]
                fig_radar.add_trace(go.Scatterpolar(
                    r=vals, theta=categories + [categories[0]],
                    name=seg_name, line=dict(color=c, width=1.5),
                    fill='toself', fillcolor=c, opacity=0.1
                ))
            user_vals = user_normed.tolist() + [user_normed[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=user_vals, theta=categories + [categories[0]],
                name="You", line=dict(color="#ffffff", width=2.5, dash="dot"),
                fill='toself', fillcolor="#ffffff", opacity=0.05
            ))
            fig_radar.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
                polar=dict(bgcolor="#1e293b"),
                legend=dict(font=dict(color="#94a3b8", size=10)),
                margin=dict(t=30, b=10, l=10, r=10), height=360
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-header">📊 Segment Profiles</div>', unsafe_allow_html=True)
        profile = rfm.groupby("Segment").agg(
            Customers=("CustomerID", "count"),
            Avg_Recency=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean"),
        ).round(1).reset_index()
        profile.columns = ["Segment","Customers","Avg Recency (days)","Avg Frequency","Avg Monetary (£)"]
        st.dataframe(profile.set_index("Segment"), use_container_width=True)

        st.markdown('<div class="section-header">📈 Segment Strategy Guide</div>', unsafe_allow_html=True)
        strategies = [
            ("High-Value 🏆", "#4ade80", "VIP rewards, early access, premium bundles, personal account managers"),
            ("Regular 🔄",    "#6366f1", "Cross-sell complementary products, seasonal campaigns, referral programs"),
            ("Occasional 💤", "#facc15", "Limited-time flash sales, reminder emails, loyalty point multipliers"),
            ("At-Risk ⚠️",   "#f87171", "Win-back discount codes, 'We miss you' campaigns, churn surveys"),
        ]
        for name, color, strategy in strategies:
            st.markdown(f"""
<div style="background:#1e293b;border-left:4px solid {color};border-radius:8px;padding:0.8rem 1rem;margin:0.5rem 0;">
  <div style="color:{color};font-weight:600;margin-bottom:0.3rem;">{name}</div>
  <div style="color:#94a3b8;font-size:0.85rem;">{strategy}</div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#475569;font-size:0.8rem;padding:0.5rem 0;">
  🛒 Shopper Spectrum · Built with Pandas · Scikit-learn · Plotly · Streamlit
</div>
""", unsafe_allow_html=True)
