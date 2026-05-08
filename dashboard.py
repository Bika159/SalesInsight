import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================
# Page Configuration
# ============================================
st.set_page_config(
    page_title="Executive Sales Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# Custom CSS for Dark Premium Theme
# ============================================
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    :root {
        --bg-color: #0A0E1A;
        --card-bg: #161B2E;
        --accent-blue: #00D4FF;
        --accent-gold: #FFD700;
        --accent-green: #00FF88;
        --text-color: #E0E6ED;
    }

    .main {
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }

    /* Card Styling */
    .metric-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #2D3748;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease, border-color 0.3s ease;
        animation: slideUp 0.8s ease-out;
        text-align: center;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        border-color: var(--accent-blue);
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    }

    .metric-label {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: var(--accent-blue);
        font-size: 32px;
        font-weight: 700;
    }

    .metric-value.gold { color: var(--accent-gold); }
    .metric-value.green { color: var(--accent-green); }

    /* Chart Containers */
    .chart-container {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #2D3748;
        margin-bottom: 24px;
        animation: fadeIn 1s ease-in;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    /* Custom Titles */
    h1, h2, h3 {
        color: var(--text-color) !important;
        font-weight: 700 !important;
    }

    .insight-box {
        background: rgba(0, 212, 255, 0.05);
        border-left: 4px solid var(--accent-blue);
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 10px;
    }

    .stButton>button {
        background-color: var(--accent-blue) !important;
        color: var(--bg-color) !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Data Loading
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv("clean_data.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

with st.spinner("Initializing Enterprise Intelligence..."):
    df_raw = load_data()

# ============================================
# Sidebar Filters
# ============================================
st.sidebar.markdown('<h2 style="font-size:1.5rem;"><i class="fa-solid fa-gears" style="color:#00D4FF; margin-right:10px;"></i> Control Center</h2>', unsafe_allow_html=True)
st.sidebar.markdown("---")

# Refresh Button
if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df_raw['Region'].unique(),
    default=df_raw['Region'].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df_raw['Category'].unique(),
    default=df_raw['Category'].unique()
)

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df_raw['Order Year'].unique(), reverse=True),
    default=df_raw['Order Year'].unique()
)

# Apply Filters
df = df_raw[
    (df_raw['Region'].isin(region_filter)) &
    (df_raw['Category'].isin(category_filter)) &
    (df_raw['Order Year'].isin(year_filter))
]

# ============================================
# Header Section
# ============================================
st.markdown('<h1><i class="fa-solid fa-shield-halved" style="color:#00D4FF; margin-right:10px;"></i> Superstore Sales Intelligence</h1>', unsafe_allow_html=True)
st.markdown(f"**Snapshot Period:** {df['Order Date'].min().strftime('%b %Y')} — {df['Order Date'].max().strftime('%b %Y')} | **Current View:** {', '.join(map(str, year_filter)) if year_filter else 'All Years'}")

# ============================================
# 1. KPI Row (4 Cards)
# ============================================
total_sales = df['Sales'].sum()
total_orders = df['Order ID'].nunique()
total_customers = df['Customer ID'].nunique() # Fixed: Unique Customers
avg_order_value = total_sales / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Total Sales</div>
        <div class="metric-value">${total_sales:,.0f}</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Total Orders</div>
        <div class="metric-value gold">{total_orders:,}</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Total Customers</div>
        <div class="metric-value green">{total_customers:,}</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Avg Order Value</div>
        <div class="metric-value">${avg_order_value:,.2f}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# Charts Grid
# ============================================

# Row 1: Monthly Trend & Sales by Category/Segment
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size:1.2rem;"><i class="fa-solid fa-calendar-days" style="color:#00D4FF; margin-right:8px;"></i> Monthly Sales Performance Trend</h3>', unsafe_allow_html=True)
    monthly_sales = df.groupby(['Order Year', 'Order Month'])['Sales'].sum().reset_index()
    monthly_sales['Date'] = pd.to_datetime(
        monthly_sales[['Order Year', 'Order Month']]
        .rename(columns={'Order Year': 'year', 'Order Month': 'month'})
        .assign(day=1)
    )
    monthly_sales = monthly_sales.sort_values('Date')
    
    fig_trend = px.line(
        monthly_sales, x='Date', y='Sales',
        line_shape='spline',
        color_discrete_sequence=['#00D4FF']
    )
    fig_trend.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#94A3B8',
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis_title="", yaxis_title="Sales ($)",
        hovermode="x unified",
        template='plotly_dark'
    )
    fig_trend.update_traces(fill='tozeroy', fillcolor='rgba(0, 212, 255, 0.1)')
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size:1.2rem;"><i class="fa-solid fa-folder-tree" style="color:#00D4FF; margin-right:8px;"></i> Sales by Category & Segment</h3>', unsafe_allow_html=True)
    cat_seg = df.groupby(['Category', 'Segment'])['Sales'].sum().reset_index()
    fig_grouped = px.bar(
        cat_seg, x='Category', y='Sales', color='Segment',
        barmode='group',
        color_discrete_map={'Consumer': '#00D4FF', 'Corporate': '#FFD700', 'Home Office': '#00FF88'}
    )
    fig_grouped.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#94A3B8',
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template='plotly_dark'
    )
    st.plotly_chart(fig_grouped, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2: Top Cities & Top Products
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size:1.2rem;"><i class="fa-solid fa-city" style="color:#00D4FF; margin-right:8px;"></i> Top 10 Cities by Sales</h3>', unsafe_allow_html=True)
    top_cities = df.groupby('City')['Sales'].sum().nlargest(10).reset_index().sort_values('Sales')
    fig_city = px.bar(
        top_cities, x='Sales', y='City',
        orientation='h',
        color_discrete_sequence=['#00D4FF']
    )
    fig_city.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        template='plotly_dark'
    )
    st.plotly_chart(fig_city, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size:1.2rem;"><i class="fa-solid fa-box-open" style="color:#FFD700; margin-right:8px;"></i> Top 10 Best Selling Products</h3>', unsafe_allow_html=True)
    top_products = df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index().sort_values('Sales')
    fig_prod = px.bar(
        top_products, x='Sales', y='Product Name',
        orientation='h',
        color_discrete_sequence=['#FFD700']
    )
    fig_prod.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        template='plotly_dark'
    )
    st.plotly_chart(fig_prod, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 3: Shipping Speed & Top States
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size:1.2rem;"><i class="fa-solid fa-truck-fast" style="color:#00FF88; margin-right:8px;"></i> Shipping Speed Analysis (Avg Days)</h3>', unsafe_allow_html=True)
    ship_speed = df.groupby('Ship Mode')['Shipping Days'].mean().reset_index().sort_values('Shipping Days')
    fig_ship = px.bar(
        ship_speed, x='Ship Mode', y='Shipping Days',
        color='Shipping Days',
        color_continuous_scale=['#00FF88', '#FFD700', '#FF6B6B']
    )
    fig_ship.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        template='plotly_dark'
    )
    st.plotly_chart(fig_ship, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row3_col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size:1.2rem;"><i class="fa-solid fa-map-location-dot" style="color:#00D4FF; margin-right:8px;"></i> Top 15 States by Sales</h3>', unsafe_allow_html=True)
    top_states = df.groupby('State')['Sales'].sum().nlargest(15).reset_index()
    fig_state = px.bar(
        top_states, x='State', y='Sales',
        color_discrete_sequence=['#00D4FF']
    )
    fig_state.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        template='plotly_dark'
    )
    st.plotly_chart(fig_state, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# Executive Summary Insights
# ============================================
st.markdown("---")
st.markdown('<h2><i class="fa-solid fa-lightbulb" style="color:#FFD700; margin-right:10px;"></i> Executive Strategic Summary</h2>', unsafe_allow_html=True)

# Calculation of Insights
top_selling_city = df.groupby('City')['Sales'].sum().idxmax()
best_selling_product = df.groupby('Product Name')['Sales'].sum().idxmax()
fastest_ship_mode = df.groupby('Ship Mode')['Shipping Days'].mean().idxmin()

# Get best month name
best_month_idx = df.groupby('Order Month')['Sales'].sum().idxmax()
best_month_name = datetime(2000, best_month_idx, 1).strftime('%B')

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown(f"""
    <div class="insight-box">
        <i class="fa-solid fa-rocket" style="color:#00D4FF; margin-right:5px;"></i> <b>Market Leader:</b> The highest revenue is currently generated in <b>{top_selling_city}</b>, indicating strong localized demand.
    </div>
    <div class="insight-box">
        <i class="fa-solid fa-trophy" style="color:#FFD700; margin-right:5px;"></i> <b>Star Product:</b> <b>{best_selling_product}</b> remains the primary revenue driver across all regions.
    </div>
    """, unsafe_allow_html=True)

with insight_col2:
    st.markdown(f"""
    <div class="insight-box">
        <i class="fa-solid fa-bolt-lightning" style="color:#00FF88; margin-right:5px;"></i> <b>Logistics Efficiency:</b> <b>{fastest_ship_mode}</b> is the most efficient shipping method with the lowest average transit time.
    </div>
    <div class="insight-box">
        <i class="fa-solid fa-calendar-check" style="color:#00D4FF; margin-right:5px;"></i> <b>Seasonal Peak:</b> Historical data suggests <b>{best_month_name}</b> as the strongest month for sales performance.
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><center><p style='color: #64748B;'>Enterprise Sales Dashboard v2.0 | Built with Streamlit & Plotly</p></center>", unsafe_allow_html=True)
