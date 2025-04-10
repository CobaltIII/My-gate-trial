import streamlit as st
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="SmartGate Dashboard", layout="wide")

# --- HEADER ---
with st.container():
    cols = st.columns([2, 8, 2])
    with cols[0]:
        st.markdown("### 🚪 SmartGate")
    with cols[1]:
        st.markdown(f"**{datetime(2024, 4, 24, 12, 0).strftime('%B %d, %Y %I:%M %p')}**")
    with cols[2]:
        st.image("https://randomuser.me/api/portraits/women/44.jpg", width=40)
        st.markdown("**Esther Howard**")

st.markdown("---")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 📋 Dashboard")
    st.button("🏠 Dashboard")
    st.button("🧑‍🤝‍🧑 My Visitors")
    st.button("📅 Book Amenity")
    st.button("🛠 Order Services")
    st.button("🚗 My Cars")

# --- MAIN DASHBOARD HEADER ---
st.markdown("## Hi, Esther Howard\nWelcome back!")
st.markdown("Here's a quick overview of your society activities.")

# --- MAIN GRID ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Add Visitor")
    visitor_name = st.text_input("Visitor Name")
    visit_time = st.text_input("Date/Time of Visit")
    purpose = st.text_input("Purpose")
    st.text_input("Passkey", value="498172", disabled=True)
    st.button("Submit")

    st.markdown("### Booked Amenities")
    st.table({
        "Amenity": ["Gym"],
        "Date": ["April 26"],
        "Time Slot": ["10:00 AM - 11:00 AM"],
        "No. of People": [1]
    })

    st.markdown("### My Cars")
    st.image("https://static.vecteezy.com/system/resources/previews/003/694/243/non_2x/car-icon-in-flat-style-simple-traffic-icon-free-vector.jpg", width=80)
    st.text("XV2 1234")

with col2:
    st.markdown("### My Visitors")
    st.markdown("[Add Visitor](#)")
    st.button("Order Service", key="order_service_button1")
    st.table({
        "Order ID": [1024, 1023],
        "Date": ["Apr 23, 2024", "Apr 23, 2024"],
        "Status": ["Completed", "Pending"]
    })

    st.markdown("### Service Orders")
    st.button("Order Service", key="order_service_button2")
    st.table({
        "Order ID": [1024, 1023],
        "Service": ["Laundry", "Cleaning"],
        "Status": ["Completed", "Pending"]
    })

    st.markdown("### Activity Log")
    st.markdown("""
    - **10:45 AM** Visitor Jane Doe approved  
    - **09:30 AM** Gym booked: April 26, 2024  
    - **09:00 AM** Service Order #1024 created
    """)

