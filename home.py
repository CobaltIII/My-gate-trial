import streamlit as st
from datetime import datetime
import asyncio
import asyncpg
import os
from dotenv import load_dotenv
import nest_asyncio
import random
import string
import time
from datetime import datetime
import pandas as pd

nest_asyncio.apply()
load_dotenv()

DB_URL = os.getenv("URI")
db_pool = None

if "activity_log" not in st.session_state:
    st.session_state.activity_log = [
        "You logged in!"
    ]


async def connect_to_db():
    global db_pool
    if not db_pool:
        db_pool = await asyncpg.create_pool(dsn=DB_URL)

async def disconnect_from_db():
    global db_pool
    if db_pool:
        await db_pool.close()

async def get_connection():
    global db_pool
    return await db_pool.acquire()

async def get_service_orders(house_number):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT S.Service_Name, R.Order_ID, R.Date, R.Time, R.Delivery_Status
            FROM Resident_Orders_Service R
            JOIN Services S ON R.Service_ID = S.Service_ID
            WHERE R.House_Number = $1
            ORDER BY R.Date DESC, R.Time DESC
        """, house_number)
        return rows
async def get_all_services():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT Service_ID, Service_Name, Provider_Name, Cost
            FROM Services
            ORDER BY Service_Name
        """)
        return rows

def generate_passkey():
    digits = ''.join(random.choices(string.digits, k=6))
    return digits

async def get_visitors():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT Visitor_Name, Visit_Purpose,phone_number
            FROM Visitor
            ORDER BY Visitor_Name
        """)
        return rows

def add_log(message):
    timestamp = datetime.now().strftime("%I:%M %p")
    st.session_state.activity_log.insert(0, f"{timestamp} {message}")

async def get_activity_log():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT Activity_Description, Timestamp
            FROM Activity_Log
            WHERE House_Number = $1
            ORDER BY Timestamp DESC
        """, 3001)
        return rows

async def get_cars(house_number):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT registration_number,model, parking_spot_number
            FROM Car
            WHERE resident_house_number = $1
        """, house_number)
        return rows

async def get_booked_amenities(house_number):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
        SELECT A.Amenity_Name, R.Booking_Date, R.Start_Time, R.End_Time, R.Number_of_people
        FROM Resident_Books_Amenity R
        JOIN Amenities A ON A.Amenity_ID = R.Amenity_ID
        WHERE R.House_Number = $1
    """, house_number)
        return rows


# Run once when app starts
asyncio.run(connect_to_db())

# --- PAGE CONFIG ---
st.set_page_config(page_title="SmartGate Dashboard", layout="wide")

# --- HEADER ---
with st.container():
    cols = st.columns([2, 8, 2])
    with cols[0]:
        st.markdown("### SmartGate")
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
    visit_date = st.date_input("Date of Visit")
    purpose = st.text_input("Purpose")
    st.text_input("Passkey", value=str(generate_passkey()), disabled=True)

    if st.button("Submit") and visitor_name and purpose:
        full_visit_time = visit_date
        visit_id = (
            full_visit_time.year
            + full_visit_time.month
            + full_visit_time.day
        )

        async def add_visitor():
            async with db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO Visitor (Visitor_ID, Visitor_Name, Phone_Number, Has_Passkey, Visit_Purpose)
                    VALUES ($1, $2, $3, $4, $5)
                """, visit_id, visitor_name, "9876543210", True, purpose)

        asyncio.get_event_loop().run_until_complete(add_visitor())
        add_log(f"Visitor added: **{visitor_name}**")
        st.success("Visitor added to the system.")

    bookings = asyncio.get_event_loop().run_until_complete(get_booked_amenities(3001))

    if bookings:
        df_amenities = pd.DataFrame([dict(row) for row in bookings])
        df_amenities.columns = ["Amenity", "Date", "Start", "End", "People"]
        
        st.markdown("### Booked Amenities")
        st.table(df_amenities)

    st.markdown("### My Cars")

    cars = asyncio.get_event_loop().run_until_complete(get_cars(3001))

    if cars:
        df_cars = pd.DataFrame([dict(row) for row in cars])
        df_cars.columns = ["Registration Number", "Model", "Parking Spot"]
        st.table(df_cars)   
    else:
        st.info("No cars registered.")

with col2:
    st.markdown("### My Visitors")
    visitors = asyncio.get_event_loop().run_until_complete(get_visitors())
    df_visitors = pd.DataFrame(visitors)
    df_visitors.columns = ["Visitor Name", "Visit Purpose", "Phone Number"]

    st.markdown("### My Visitors")
    st.table(df_visitors)  # Automatically removes index styling

    st.markdown("### Service Orders")

    orders = asyncio.get_event_loop().run_until_complete(get_service_orders(3001))

    if orders:
        order_data = [{
            "Order ID": row["order_id"],
            "Service": row["service_name"],
            "Date": row["date"].strftime("%b %d, %Y"),
            "Time": row["time"].strftime("%I:%M %p"),
            "Status": row["delivery_status"]
        } for row in orders]
        st.table(order_data)
    else:
        st.info("No service orders found.")
    
    st.markdown("### 📦 Order a Service")

    services = asyncio.get_event_loop().run_until_complete(get_all_services())

    if services:
     service_names = [f"{row['service_name']} (by {row['provider_name']} - ₹{row['cost']})" for row in services]
     selected = st.selectbox("Select Service", service_names)
     selected_service = services[service_names.index(selected)]
    
     order_date = st.date_input("Order Date", datetime.now().date())
     order_time = st.time_input("Order Time", datetime.now().time())

     if st.button("Place Order"):
        order_id = int(time.time())  # Using Unix timestamp as unique Order_ID
        async def place_order():
            async with db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO Resident_Orders_Service (House_Number, Service_ID, Order_ID, Date, Time, Delivery_Status)
                    VALUES ($1, $2, $3, $4, $5, $6)
                """, 3001, selected_service["service_id"], order_id, order_date, order_time, "Pending")

        asyncio.get_event_loop().run_until_complete(place_order())
        add_log(f"Ordered service: **{selected_service['service_name']}**")
        st.success("Service ordered successfully!")
    else:
     st.warning("No services available.")

    st.markdown("### Activity Log")
    for log_entry in st.session_state.activity_log:
        st.markdown(f"- {log_entry}")
