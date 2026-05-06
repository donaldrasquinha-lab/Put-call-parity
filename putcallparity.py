import streamlit as st
import requests
import pandas as pd

# --- 1. INITIALIZE SESSION STATE ---
# This keeps track of your connection status even when the page refreshes
if 'upstox_connected' not in st.session_state:
    st.session_state.upstox_connected = False
if 'github_connected' not in st.session_state:
    st.session_state.github_connected = False

# --- 2. UI HEADER ---
st.set_page_config(page_title="Nifty Arb Center", layout="wide")
st.title("🚀 Nifty Live Arbitrage Center")

# Top Status Bar
c1, c2 = st.columns(2)
upstox_status = "🟢 Connected" if st.session_state.upstox_connected else "🔴 Disconnected"
github_status = "🟢 Linked" if st.session_state.github_connected else "🔴 Unlinked"

c1.info(f"**Upstox:** {upstox_status}")
c2.info(f"**GitHub Repo:** {github_status}")

# --- 3. SIDEBAR (The Control Panel) ---
with st.sidebar:
    st.header("🔗 System Integration")
    
    # User Inputs
    upstox_api_key = st.text_input("Upstox API Key", type="password", placeholder="Enter your client_id")
    github_user_repo = st.text_input("GitHub Path (user/repo)", value="donaldrasquinha-lab/nifty-live-scan")
    
    # The Connect Button
    if st.button("⚡ Connect All Systems", use_container_width=True):
        
        # 3a. Verify GitHub Connection (Logic moved INSIDE the button)
        # We use 'raw' to get the actual file data
        github_url = f"https://githubusercontent.com{github_user_repo}/main/nifty50_upstox_keys.csv"
        
        try:
            res = requests.get(github_url, timeout=5)
            if res.status_code == 200:
                st.session_state.github_connected = True
                st.success("✅ GitHub linked successfully!")
                st.toast("Keys loaded from GitHub")
            else:
                st.session_state.github_connected = False
                st.error(f"❌ File not found (Error {res.status_code}). Check if your repo is PUBLIC.")
        except Exception as e:
            st.session_state.github_connected = False
            st.error(f"📡 Network Error: {str(e)}")

        # 3b. Upstox Login Link
        if upstox_api_key:
            # We show the login link only if they provided an API key
            st.markdown(f"### [👉 Click here to log in to Upstox](https://upstox.com{upstox_api_key}&redirect_uri=https://google.com)")
        else:
            st.warning("Enter Upstox API Key to generate login link.")

# --- 4. MAIN DASHBOARD CONTENT ---
if st.session_state.github_connected:
    st.success("Ready to scan Nifty Stocks. Connect Upstox to see Live Data.")
    # Placeholder for the Live Table
    st.divider()
    st.subheader("📊 Live Scanner Table")
    st.info("Waiting for Upstox WebSocket connection...")
else:
    st.warning("👈 Please link your GitHub Repository in the sidebar to start.")
