import streamlit as st
import requests
import pandas as pd

# --- INITIALIZE SESSION STATE ---
if 'upstox_connected' not in st.session_state:
    st.session_state.upstox_connected = False
if 'github_connected' not in st.session_state:
    st.session_state.github_connected = False

# --- UI HEADER ---
st.title("🚀 Nifty Live Arbitrage Center")

# Connection Status Bar
c1, c2 = st.columns(2)
upstox_status = "🟢 Connected" if st.session_state.upstox_connected else "🔴 Disconnected"
github_status = "🟢 Linked" if st.session_state.github_connected else "🔴 Unlinked"
c1.info(f"**Upstox:** {upstox_status}")
c2.info(f"**GitHub Repo:** {github_status}")

# --- THE CONNECT BUTTON ---
with st.sidebar:
    st.header("🔗 System Integration")

# Use this updated block inside your button logic
github_url = f"https://githubusercontent.com/{github_user_repo}/main/nifty50_upstox_keys.csv"
try:
    res = requests.get(github_url, timeout=5)
    if res.status_code == 200:
        st.session_state.github_connected = True
        st.success("GitHub linked successfully!")
    elif res.status_code == 404:
        st.error(f"File not found at: {github_url}. Check your file name!")
    else:
        st.error(f"GitHub returned error code: {res.status_code}")
except Exception as e:
    st.error(f"Connection failed: {str(e)}")

    # Input fields for configuration
    upstox_api_key = st.text_input("Upstox API Key", type="password")
    github_user_repo = st.text_input("GitHub Path (user/repo)", value="your-name/nifty-scanner")
    
    if st.button("⚡ Connect All Systems", use_container_width=True):
        # 1. Trigger Upstox Auth (Opens daily login in new tab)
        auth_url = f"https://upstox.com{upstox_api_key}&redirect_uri=YOUR_REDIRECT_URL"
        st.markdown(f'<a href="{auth_url}" target="_blank">Click here to log in to Upstox</a>', unsafe_allow_html=True)
        
        # 2. Verify GitHub Link
        github_url = f"https://githubusercontent.com{github_user_repo}/main/nifty50_upstox_keys.csv"
        try:
            res = requests.get(github_url)
            if res.status_code == 200:
                st.session_state.github_connected = True
                st.success("GitHub repository successfully linked!")
            else:
                st.error("GitHub file not found. Check repo path.")
        except:
            st.error("Network error connecting to GitHub.")
