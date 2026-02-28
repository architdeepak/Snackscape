import streamlit as st
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Snackscape - Premium Snack Subscriptions",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ultra-modern professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
        color: #ffffff;
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
    }
    
    /* Animated gradient background */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Header Section */
    .hero-header {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(20, 20, 20, 0.98) 100%);
        padding: 4rem 3rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(212, 175, 55, 0.2);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.8),
            0 0 100px rgba(212, 175, 55, 0.1) inset;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, 
            transparent 0%, 
            rgba(212, 175, 55, 0.03) 25%,
            transparent 50%,
            rgba(212, 175, 55, 0.03) 75%,
            transparent 100%);
        background-size: 200% 200%;
        animation: gradientShift 15s ease infinite;
        pointer-events: none;
    }
    
    .logo-container {
        text-align: center;
        position: relative;
        z-index: 2;
    }
    
    .logo-text {
        font-family: 'Playfair Display', serif;
        font-size: 5.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #FFD700 0%, #d4af37 50%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 8px;
        margin: 0;
        line-height: 1.2;
        text-shadow: 0 0 80px rgba(212, 175, 55, 0.5);
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.4)); }
        to { filter: drop-shadow(0 0 40px rgba(212, 175, 55, 0.8)); }
    }
    
    .tagline {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.4rem;
        color: #c0c0c0;
        font-weight: 300;
        margin-top: 1rem;
        letter-spacing: 4px;
        text-transform: uppercase;
    }
    
    /* Modern Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(30, 30, 30, 0.6);
        padding: 1rem 2rem;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(212, 175, 55, 0.1);
        margin-bottom: 3rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #888;
        background: transparent;
        border: none;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #d4af37;
        background: rgba(212, 175, 55, 0.1);
        border-radius: 12px;
    }
    
    .stTabs [aria-selected="true"] {
        color: #FFD700 !important;
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(212, 175, 55, 0.1) 100%) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(212, 175, 55, 0.2);
    }
    
    /* Current Plan Status Card */
    .status-card {
        background: linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(30, 30, 30, 0.95) 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
    }
    
    .status-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(135deg, #FFD700, #d4af37, #FFA500);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }
    
    .status-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .status-item {
        text-align: center;
        padding: 1.5rem;
        background: rgba(212, 175, 55, 0.05);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .status-item:hover {
        background: rgba(212, 175, 55, 0.1);
        transform: translateY(-5px);
    }
    
    .status-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.9rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    
    .status-value {
        font-family: 'Inter', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFD700, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Premium Plan Cards */
    .plan-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2.5rem;
        margin: 3rem 0;
    }
    
    .plan-card {
        background: linear-gradient(135deg, rgba(25, 25, 25, 0.98) 0%, rgba(20, 20, 20, 0.98) 100%);
        border-radius: 24px;
        padding: 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(212, 175, 55, 0.15);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }
    
    .plan-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #FFD700, #d4af37, #FFA500);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .plan-card:hover {
        transform: translateY(-12px) scale(1.02);
        border-color: rgba(212, 175, 55, 0.4);
        box-shadow: 
            0 30px 80px rgba(0, 0, 0, 0.8),
            0 0 60px rgba(212, 175, 55, 0.3);
    }
    
    .plan-card:hover::before {
        opacity: 1;
    }
    
    .plan-header {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(212, 175, 55, 0.05) 100%);
        padding: 2.5rem 2rem;
        text-align: center;
        border-bottom: 1px solid rgba(212, 175, 55, 0.1);
    }
    
    .plan-name {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #FFD700;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }
    
    .plan-description {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #aaa;
        font-weight: 300;
        line-height: 1.6;
        margin-top: 1rem;
    }
    
    .plan-body {
        padding: 2.5rem 2rem;
    }
    
    .plan-price-section {
        text-align: center;
        margin-bottom: 2.5rem;
        padding: 2rem 0;
        background: rgba(212, 175, 55, 0.03);
        border-radius: 16px;
    }
    
    .plan-price {
        font-family: 'Inter', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }
    
    .plan-period {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        color: #777;
        font-weight: 400;
        margin-top: 0.5rem;
    }
    
    .feature-list {
        list-style: none;
        padding: 0;
        margin: 2rem 0;
    }
    
    .feature-item {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #ccc;
        padding: 1rem;
        margin: 0.5rem 0;
        background: rgba(212, 175, 55, 0.03);
        border-radius: 10px;
        border-left: 3px solid #d4af37;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .feature-item:hover {
        background: rgba(212, 175, 55, 0.08);
        transform: translateX(5px);
        border-left-color: #FFD700;
    }
    
    .feature-icon {
        font-size: 1.2rem;
        color: #FFD700;
    }
    
    /* Premium Button Styling */
    .stButton > button {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 1.2rem 3rem;
        background: linear-gradient(135deg, #FFD700 0%, #d4af37 50%, #FFA500 100%);
        color: #000;
        border: none;
        border-radius: 12px;
        width: 100%;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 8px 25px rgba(212, 175, 55, 0.4),
            0 0 30px rgba(212, 175, 55, 0.2) inset;
        letter-spacing: 1px;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 
            0 12px 40px rgba(212, 175, 55, 0.6),
            0 0 50px rgba(212, 175, 55, 0.3) inset;
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Success Message */
    .success-banner {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(76, 175, 80, 0.05) 100%);
        border: 2px solid rgba(76, 175, 80, 0.5);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        color: #4CAF50;
        box-shadow: 0 10px 40px rgba(76, 175, 80, 0.2);
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Section Titles */
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin: 4rem 0 3rem 0;
        background: linear-gradient(135deg, #FFD700, #d4af37, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 2px;
    }
    
    /* Stats Cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.9) 0%, rgba(20, 20, 20, 0.9) 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(212, 175, 55, 0.2);
        transition: all 0.4s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    .stat-card:hover {
        transform: translateY(-10px) scale(1.05);
        border-color: rgba(212, 175, 55, 0.5);
        box-shadow: 0 20px 50px rgba(212, 175, 55, 0.3);
    }
    
    .stat-number {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        margin-bottom: 1rem;
    }
    
    .stat-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 500;
    }
    
    /* Content Cards */
    .content-card {
        background: linear-gradient(135deg, rgba(25, 25, 25, 0.95) 0%, rgba(20, 20, 20, 0.95) 100%);
        padding: 3rem;
        border-radius: 20px;
        border: 1px solid rgba(212, 175, 55, 0.15);
        margin: 2rem 0;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.6);
    }
    
    .content-card h3 {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: #FFD700;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    
    .content-card p {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        line-height: 1.9;
        color: #bbb;
        font-weight: 300;
    }
    
    /* Form Styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        font-family: 'Inter', sans-serif;
        background: rgba(30, 30, 30, 0.8) !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        border-radius: 12px !important;
        color: #fff !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.3) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        margin-top: 5rem;
        border-top: 1px solid rgba(212, 175, 55, 0.2);
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .footer-text {
        color: #d4af37;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .footer-subtext {
        color: #777;
        font-size: 0.95rem;
        font-weight: 300;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .logo-text {
            font-size: 3rem;
            letter-spacing: 4px;
        }
        
        .section-title {
            font-size: 2.5rem;
        }
        
        .plan-price {
            font-size: 3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_plan' not in st.session_state:
    st.session_state.current_plan = 'Premium Plan'
if 'country' not in st.session_state:
    st.session_state.country = 'India'
if 'renewal_date' not in st.session_state:
    st.session_state.renewal_date = (datetime.now() + timedelta(days=27)).strftime('%B %d, %Y')
if 'selected_plan' not in st.session_state:
    st.session_state.selected_plan = None

# Hero Header
st.markdown("""
<div class="hero-header">
    <div class="logo-container">
        <h1 class="logo-text">SNACKSCAPE</h1>
        <p class="tagline">Curated Global Flavors</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation
tab1, tab2, tab3, tab4 = st.tabs(["🏠 HOME", "📦 PLANS", "ℹ️ ABOUT", "📧 CONTACT"])

with tab1:
    st.markdown('<h2 class="section-title">Welcome to Snackscape</h2>', unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">50K+</div>
            <div class="stat-label">Happy Members</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">30+</div>
            <div class="stat-label">Countries</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">100%</div>
            <div class="stat-label">Satisfaction</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">4.9★</div>
            <div class="stat-label">Rating</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Content Section
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h3>Experience the World Through Snacks</h3>
            <p>
                Snackscape brings you a carefully curated selection of premium snacks from around the globe, 
                delivered right to your doorstep every month. Each box is a journey through different cultures, 
                flavors, and culinary traditions.
            </p>
        </div>
        
        <div class="content-card">
            <h3>Why Choose Snackscape?</h3>
            <p>
                <span style="color: #FFD700; font-weight: 600;">✨ Curated Selection:</span> Hand-picked by expert food curators<br><br>
                <span style="color: #FFD700; font-weight: 600;">🌍 Global Variety:</span> Discover treats from over 30 countries<br><br>
                <span style="color: #FFD700; font-weight: 600;">📦 Quality Guaranteed:</span> Premium products with authentic flavors<br><br>
                <span style="color: #FFD700; font-weight: 600;">🎁 Flexible Plans:</span> Choose the subscription that fits your lifestyle
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="content-card" style="height: 100%;">
            <h3 style="text-align: center;">What's Inside</h3>
            <div style="margin-top: 2rem;">
                <div style="background: rgba(212, 175, 55, 0.1); padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #FFD700;">
                    <div style="color: #FFD700; font-size: 1.8rem; margin-bottom: 0.5rem;">🍫</div>
                    <div style="font-family: 'Space Grotesk'; font-weight: 600; color: #FFD700; margin-bottom: 0.5rem;">Premium Chocolates</div>
                    <div style="font-family: 'Inter'; color: #aaa; font-size: 0.95rem;">Artisan chocolates from master chocolatiers</div>
                </div>
                
                <div style="background: rgba(212, 175, 55, 0.1); padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #FFD700;">
                    <div style="color: #FFD700; font-size: 1.8rem; margin-bottom: 0.5rem;">🥨</div>
                    <div style="font-family: 'Space Grotesk'; font-weight: 600; color: #FFD700; margin-bottom: 0.5rem;">Savory Delights</div>
                    <div style="font-family: 'Inter'; color: #aaa; font-size: 0.95rem;">Unique chips, crackers, and savory treats</div>
                </div>
                
                <div style="background: rgba(212, 175, 55, 0.1); padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #FFD700;">
                    <div style="color: #FFD700; font-size: 1.8rem; margin-bottom: 0.5rem;">🍬</div>
                    <div style="font-family: 'Space Grotesk'; font-weight: 600; color: #FFD700; margin-bottom: 0.5rem;">Sweet Surprises</div>
                    <div style="font-family: 'Inter'; color: #aaa; font-size: 0.95rem;">Candies and confections from around the world</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown('<h2 class="section-title">Choose Your Experience</h2>', unsafe_allow_html=True)
    
    # Current Status Card
    st.markdown(f"""
    <div class="status-card">
        <div class="status-grid">
            <div class="status-item">
                <div class="status-label">Current Plan</div>
                <div class="status-value">{st.session_state.current_plan}</div>
            </div>
            <div class="status-item">
                <div class="status-label">Location</div>
                <div class="status-value">{st.session_state.country}</div>
            </div>
            <div class="status-item">
                <div class="status-label">Next Renewal</div>
                <div class="status-value">{st.session_state.renewal_date}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Plan definitions
    plans = {
        'Basic Plan': {
            'price': 20,
            'items': 5,
            'description': 'Perfect for snack enthusiasts starting their global flavor journey',
            'features': [
                '5 premium snacks per box',
                'Snacks from 2-3 countries',
                'Free standard shipping',
                'Cancel anytime',
                'Monthly surprise treats',
                'Access to member recipes'
            ]
        },
        'Standard Plan': {
            'price': 30,
            'items': 10,
            'description': 'Our most popular choice for adventurous taste explorers',
            'features': [
                '10 premium snacks per box',
                'Snacks from 4-5 countries',
                'Free express shipping',
                'Exclusive limited editions',
                'Digital recipe booklet',
                'Priority customer support',
                'Member community access'
            ]
        },
        'Premium Plan': {
            'price': 45,
            'items': 20,
            'description': 'The ultimate experience for true snack connoisseurs',
            'features': [
                '20 premium snacks per box',
                'Snacks from 7-8 countries',
                'Free overnight shipping',
                'Rare & exclusive items',
                'Physical recipe book',
                'VIP customer support',
                'Early access to products',
                'Members-only events',
                'Quarterly bonus box'
            ]
        }
    }
    
    # Display plans
    cols = st.columns(3)
    
    for idx, (plan_name, plan_details) in enumerate(plans.items()):
        with cols[idx]:
            st.markdown(f"""
            <div class="plan-card">
                <div class="plan-header">
                    <h3 class="plan-name">{plan_name}</h3>
                    <p class="plan-description">{plan_details['description']}</p>
                </div>
                <div class="plan-body">
                    <div class="plan-price-section">
                        <div class="plan-price">${plan_details['price']}</div>
                        <div class="plan-period">per month</div>
                    </div>
                    <div class="feature-list">
            """, unsafe_allow_html=True)
            
            for feature in plan_details['features']:
                st.markdown(f"""
                <div class="feature-item">
                    <span class="feature-icon">✓</span>
                    <span>{feature}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div></div></div>', unsafe_allow_html=True)
            
            if st.button(f"Select {plan_name}", key=f"btn_{plan_name}"):
                st.session_state.selected_plan = plan_name
                st.session_state.current_plan = plan_name
                st.rerun()
    
    # Success message
    if st.session_state.selected_plan:
        st.markdown(f"""
        <div class="success-banner">
            ✅ Successfully upgraded to {st.session_state.selected_plan}!<br>
            <span style="font-size: 1.1rem; color: #8BC34A;">Your next box ships on {st.session_state.renewal_date}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎉 Confirm Subscription"):
            st.balloons()
            st.success(f"🎊 Congratulations! Your {st.session_state.selected_plan} is now active!")

with tab3:
    st.markdown('<h2 class="section-title">About Snackscape</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h3>Our Story</h3>
            <p>
                Founded in 2023, Snackscape was born from a simple idea: everyone deserves to experience 
                the incredible diversity of global snack culture. Our founders, avid travelers and food 
                enthusiasts, wanted to bring the joy of discovering new flavors to people everywhere.
            </p>
        </div>
        
        <div class="content-card">
            <h3>Our Mission</h3>
            <p>
                We partner with small producers and artisan brands from around the world to bring you 
                authentic, high-quality snacks that tell a story. Every box is curated to provide not 
                just great taste, but a cultural experience that connects you to different parts of the world.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h3>What Makes Us Different</h3>
            <p>
                <span style="color: #FFD700; font-weight: 600;">🌱 Sustainability:</span><br>
                Eco-friendly packaging and ethical sourcing<br><br>
                
                <span style="color: #FFD700; font-weight: 600;">🤝 Fair Trade:</span><br>
                Direct partnerships with producers<br><br>
                
                <span style="color: #FFD700; font-weight: 600;">🎯 Authenticity:</span><br>
                Only genuine, traditional recipes<br><br>
                
                <span style="color: #FFD700; font-weight: 600;">💝 Community:</span><br>
                Join 50,000+ snack lovers worldwide
            </p>
        </div>
        
        <div class="content-card">
            <h3>Awards & Recognition</h3>
            <p style="font-size: 1.2rem; line-height: 2;">
                🏆 Best Subscription Box 2024<br>
                ⭐ 4.9/5 Stars - 10,000+ Reviews<br>
                📰 Featured in Forbes & TechCrunch<br>
                🎖️ Top Rated by Consumer Reports
            </p>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown('<h2 class="section-title">Get in Touch</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-family: Playfair Display; color: #FFD700; margin-bottom: 2rem;'>Send Us a Message</h3>", unsafe_allow_html=True)
        
        with st.form("contact_form"):
            name = st.text_input("Name", placeholder="Your name")
            email = st.text_input("Email", placeholder="your.email@example.com")
            subject = st.selectbox("Subject", 
                                  ["General Inquiry", "Subscription Support", "Partnership", "Feedback", "Other"])
            message = st.text_area("Message", placeholder="How can we help you?", height=150)
            
            submitted = st.form_submit_button("Send Message")
            
            if submitted:
                if name and email and message:
                    st.markdown("""
                    <div class="success-banner">
                        ✅ Thank you for your message!<br>
                        <span style="font-size: 1.1rem;">We'll get back to you within 24 hours.</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("⚠️ Please fill in all required fields.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h3 style="text-align: center;">Contact Info</h3>
            
            <div style="margin: 2rem 0; padding: 1.5rem; background: rgba(212, 175, 55, 0.05); border-radius: 12px; border-left: 3px solid #FFD700;">
                <div style="color: #FFD700; font-size: 1.5rem; margin-bottom: 0.5rem;">📧</div>
                <div style="font-family: 'Space Grotesk'; color: #888; font-size: 0.9rem; margin-bottom: 0.3rem;">EMAIL</div>
                <div style="font-family: 'Inter'; color: #fff;">support@snackscape.com</div>
            </div>
            
            <div style="margin: 2rem 0; padding: 1.5rem; background: rgba(212, 175, 55, 0.05); border-radius: 12px; border-left: 3px solid #FFD700;">
                <div style="color: #FFD700; font-size: 1.5rem; margin-bottom: 0.5rem;">📱</div>
                <div style="font-family: 'Space Grotesk'; color: #888; font-size: 0.9rem; margin-bottom: 0.3rem;">PHONE</div>
                <div style="font-family: 'Inter'; color: #fff;">1-800-SNACKS</div>
            </div>
            
            <div style="margin: 2rem 0; padding: 1.5rem; background: rgba(212, 175, 55, 0.05); border-radius: 12px; border-left: 3px solid #FFD700;">
                <div style="color: #FFD700; font-size: 1.5rem; margin-bottom: 0.5rem;">🕐</div>
                <div style="font-family: 'Space Grotesk'; color: #888; font-size: 0.9rem; margin-bottom: 0.3rem;">HOURS</div>
                <div style="font-family: 'Inter'; color: #fff; font-size: 0.95rem;">
                    Mon-Fri: 9AM - 6PM EST<br>
                    Sat-Sun: 10AM - 4PM EST
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(212, 175, 55, 0.2);">
                <div style="font-family: 'Space Grotesk'; color: #FFD700; margin-bottom: 1rem;">FOLLOW US</div>
                <div style="font-family: 'Inter'; color: #aaa; font-size: 1.1rem;">
                    Instagram • Twitter • Facebook
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p class="footer-text">© 2025 Snackscape. All rights reserved.</p>
    <p class="footer-subtext">Bringing global flavors to your doorstep, one box at a time.</p>
</div>
""", unsafe_allow_html=True)