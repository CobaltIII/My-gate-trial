# '''import streamlit as st
# from datetime import datetime
# import asyncio
# import asyncpg
# import os
# from dotenv import load_dotenv
# import nest_asyncio
# import random
# import string
# import time
# from datetime import datetime
# import pandas as pd

# nest_asyncio.apply()
# load_dotenv()

# DB_URL = os.getenv("URI")
# db_pool = None

# if "activity_log" not in st.session_state:
#     st.session_state.activity_log = [
#         "You logged in!"
#     ]


# async def connect_to_db():
#     global db_pool
#     if not db_pool:
#         db_pool = await asyncpg.create_pool(dsn=DB_URL)

# async def disconnect_from_db():
#     global db_pool
#     if db_pool:
#         await db_pool.close()

# async def get_connection():
#     global db_pool
#     return await db_pool.acquire()

# async def get_service_orders(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT S.Service_Name, R.Order_ID, R.Date, R.Time, R.Delivery_Status
#             FROM Resident_Orders_Service R
#             JOIN Services S ON R.Service_ID = S.Service_ID
#             WHERE R.House_Number = $1
#             ORDER BY R.Date DESC, R.Time DESC
#         """, house_number)
#         return rows
# async def get_all_amenities():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Amenity_ID, Amenity_Name, Availability_Status, Operating_Hours
#             FROM Amenities
#             ORDER BY Amenity_Name
#         """)
#         return rows
# async def get_all_services():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Service_ID, Service_Name, Provider_Name, Cost
#             FROM Services
#             ORDER BY Service_Name
#         """)
#         return rows

# def generate_passkey():
#     digits = ''.join(random.choices(string.digits, k=6))
#     return digits

# async def get_visitors(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Visitor_Name, Visit_Purpose,phone_number
#             FROM Visitor
#             ORDER BY Visitor_Name
#         """)
#         return rows

# def add_log(message):
#     timestamp = datetime.now().strftime("%I:%M %p")
#     st.session_state.activity_log.insert(0, f"{timestamp} {message}")

# async def get_activity_log():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Activity_Description, Timestamp
#             FROM Activity_Log
#             WHERE House_Number = $1
#             ORDER BY Timestamp DESC
#         """, house_number)
#         return rows

# async def get_cars(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT registration_number,model, parking_spot_number
#             FROM Car
#             WHERE resident_house_number = $1
#         """, house_number)
#         return rows

# async def get_booked_amenities(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#         SELECT A.Amenity_Name, R.Booking_Date, R.Start_Time, R.End_Time, R.Number_of_people
#         FROM Resident_Books_Amenity R
#         JOIN Amenities A ON A.Amenity_ID = R.Amenity_ID
#         WHERE R.House_Number = $1
#     """, house_number)
#         return rows


# # Run once when app starts
# asyncio.run(connect_to_db())

# # --- PAGE CONFIG ---
# st.set_page_config(page_title="SmartGate Dashboard", layout="wide")

# # --- HEADER ---
# with st.container():
#     cols = st.columns([2, 8, 2])
#     with cols[0]:
#         st.markdown("### SmartGate")
#     with cols[1]:
#         st.markdown(f"{datetime(2024, 4, 24, 12, 0).strftime('%B %d, %Y %I:%M %p')}")
#     with cols[2]:
#         st.image("https://randomuser.me/api/portraits/women/44.jpg", width=40)
#         st.markdown("*Esther Howard*")

# st.markdown("---")

# # --- SIDEBAR ---
# with st.sidebar:
#     st.markdown("## 📋 Dashboard")
#     st.button("🏠 Dashboard")
#     st.button("🧑‍🤝‍🧑 My Visitors")
#     st.button("📅 Book Amenity")
#     st.button("🛠 Order Services")
#     st.button("🚗 My Cars")

# # --- MAIN DASHBOARD HEADER ---
# st.markdown("## Hi, Esther Howard\nWelcome back!")
# st.markdown("Here's a quick overview of your society activities.")

# # --- MAIN GRID ---
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("### Add Visitor")
#     visitor_name = st.text_input("Visitor Name")
#     visit_date = st.date_input("Date of Visit")
#     purpose = st.text_input("Purpose")
#     st.text_input("Passkey", value=str(generate_passkey()), disabled=True)

#     if st.button("Submit") and visitor_name and purpose:
#         full_visit_time = visit_date
#         visit_id = (
#             full_visit_time.year
#             + full_visit_time.month
#             + full_visit_time.day
#         )

#         async def add_visitor():
#             async with db_pool.acquire() as conn:
#                 await conn.execute("""
#                     INSERT INTO Visitor (Visitor_ID, Visitor_Name, Phone_Number, Has_Passkey, Visit_Purpose)
#                     VALUES ($1, $2, $3, $4, $5)
#                 """, visit_id, visitor_name, "9876543210", True, purpose)

#         asyncio.get_event_loop().run_until_complete(add_visitor())
#         add_log(f"Visitor added: *{visitor_name}*")
#         st.success("Visitor added to the system.")

#     bookings = asyncio.get_event_loop().run_until_complete(get_booked_amenities(house_number))

#     if bookings:
#         df_amenities = pd.DataFrame([dict(row) for row in bookings])
#         df_amenities.columns = ["Amenity", "Date", "Start", "End", "People"]
        
#         st.markdown("### Booked Amenities")
#         st.table(df_amenities)
#     st.markdown("### ➕ Book a New Amenity")

#     amenities = asyncio.get_event_loop().run_until_complete(get_all_amenities())

#     if amenities:
#         amenity_options = [f"{row['amenity_name']} ({row['availability_status']})" for row in amenities]
#         selected = st.selectbox("Select Amenity", amenity_options, key="amenity_select")
#         selected_amenity = amenities[amenity_options.index(selected)]

#         booking_date = st.date_input("Booking Date", datetime.now().date(), key="amenity_date")
#         start_time = st.time_input("Start Time", datetime.strptime("10:00", "%H:%M").time(), key="amenity_start")
#         end_time = st.time_input("End Time", datetime.strptime("11:00", "%H:%M").time(), key="amenity_end")
#         num_people = st.number_input("Number of People", min_value=1, max_value=20, value=1, key="amenity_people")

#         if st.button("Book Amenity"):
#             booking_id = int(time.time())

#             async def book_amenity():
#                 async with db_pool.acquire() as conn:
#                     await conn.execute("""
#                         INSERT INTO Resident_Books_Amenity (
#                             House_Number, Amenity_ID, Booking_ID, Booking_Date, Start_Time, End_Time, Number_of_people
#                         ) VALUES ($1, $2, $3, $4, $5, $6, $7)
#                     """, house_number, selected_amenity["amenity_id"], booking_id, booking_date, start_time, end_time, num_people)

#             asyncio.run(book_amenity())
#             add_log(f"Booked amenity: *{selected_amenity['amenity_name']}* on {booking_date}")
#             st.success("Amenity booked successfully!")
#     else:
#         st.warning("No amenities available.")


#     st.markdown("### My Cars")

#     cars = asyncio.get_event_loop().run_until_complete(get_cars(house_number))

#     if cars:
#         df_cars = pd.DataFrame([dict(row) for row in cars])
#         df_cars.columns = ["Registration Number", "Model", "Parking Spot"]
#         st.table(df_cars)   
#     else:
#         st.info("No cars registered.")

# with col2:
#     st.markdown("### My Visitors")
#     visitors = asyncio.get_event_loop().run_until_complete(get_visitors(house_number))
#     df_visitors = pd.DataFrame(visitors)
#     df_visitors.columns = ["Visitor Name", "Visit Purpose", "Phone Number"]

#     st.markdown("### My Visitors")
#     st.table(df_visitors)  # Automatically removes index styling

#     st.markdown("### Service Orders")

#     orders = asyncio.get_event_loop().run_until_complete(get_service_orders(house_number))

#     if orders:
#         order_data = [{
#             "Order ID": row["order_id"],
#             "Service": row["service_name"],
#             "Date": row["date"].strftime("%b %d, %Y"),
#             "Time": row["time"].strftime("%I:%M %p"),
#             "Status": row["delivery_status"]
#         } for row in orders]
#         st.table(order_data)
#     else:
#         st.info("No service orders found.")
    
#     st.markdown("### 📦 Order a Service")

#     services = asyncio.get_event_loop().run_until_complete(get_all_services())

#     if services:
#      service_names = [f"{row['service_name']} (by {row['provider_name']} - ₹{row['cost']})" for row in services]
#      selected = st.selectbox("Select Service", service_names)
#      selected_service = services[service_names.index(selected)]
    
#      order_date = st.date_input("Order Date", datetime.now().date())
#      order_time = st.time_input("Order Time", datetime.now().time())

#      if st.button("Place Order"):
#         order_id = int(time.time())  # Using Unix timestamp as unique Order_ID
#         async def place_order():
#             async with db_pool.acquire() as conn:
#                 await conn.execute("""
#                     INSERT INTO Resident_Orders_Service (House_Number, Service_ID, Order_ID, Date, Time, Delivery_Status)
#                     VALUES ($1, $2, $3, $4, $5, $6)
#                 """, house_number, selected_service["service_id"], order_id, order_date, order_time, "Pending")

#         asyncio.get_event_loop().run_until_complete(place_order())
#         add_log(f"Ordered service: *{selected_service['service_name']}*")
#         st.success("Service ordered successfully!")
#     else:
#      st.warning("No services available.")

#     st.markdown("### Activity Log")
#     for log_entry in st.session_state.activity_log:
#         st.markdown(f"- {log_entry}")

    
# '''



# import streamlit as st
# from datetime import datetime
# import asyncio
# import asyncpg
# import os
# from dotenv import load_dotenv
# import nest_asyncio
# import random
# import string
# import time
# import pandas as pd

# nest_asyncio.apply()
# load_dotenv()

# DB_URL = os.getenv("URI")
# db_pool = None

# if "activity_log" not in st.session_state:
#     st.session_state.activity_log = ["You logged in!"]

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.user_type = None
#     st.session_state.user_id = None

# async def connect_to_db():
#     global db_pool
#     if not db_pool:
#         db_pool = await asyncpg.create_pool(dsn=DB_URL)

# async def disconnect_from_db():
#     global db_pool
#     if db_pool:
#         await db_pool.close()

# async def get_connection():
#     global db_pool
#     return await db_pool.acquire()

# async def is_valid_resident(house_number):
#     async with db_pool.acquire() as conn:
#         result = await conn.fetchval("SELECT COUNT(*) FROM Resident WHERE House_Number = $1", house_number)
#         return result > 0

# async def is_valid_guard(badge_number):
#     async with db_pool.acquire() as conn:
#         result = await conn.fetchval("SELECT COUNT(*) FROM Guard WHERE Badge_Number = $1", badge_number)
#         return result > 0

# async def get_service_orders(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT S.Service_Name, R.Order_ID, R.Date, R.Time, R.Delivery_Status
#             FROM Resident_Orders_Service R
#             JOIN Services S ON R.Service_ID = S.Service_ID
#             WHERE R.House_Number = $1
#             ORDER BY R.Date DESC, R.Time DESC
#         """, house_number)
#         return rows

# async def get_all_amenities():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Amenity_ID, Amenity_Name, Availability_Status, Operating_Hours
#             FROM Amenities
#             ORDER BY Amenity_Name
#         """)
#         return rows

# async def get_all_services():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Service_ID, Service_Name, Provider_Name, Cost
#             FROM Services
#             ORDER BY Service_Name
#         """)
#         return rows

# def generate_passkey():
#     digits = ''.join(random.choices(string.digits, k=6))
#     return digits

# async def get_visitors():
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Visitor_Name, Visit_Purpose, phone_number
#             FROM Visitor
#             ORDER BY Visitor_Name
#         """)
#         return rows

# def add_log(message):
#     timestamp = datetime.now().strftime("%I:%M %p")
#     st.session_state.activity_log.insert(0, f"{timestamp} {message}")

# async def get_activity_log(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT Activity_Description, Timestamp
#             FROM Activity_Log
#             WHERE House_Number = $1
#             ORDER BY Timestamp DESC
#         """, house_number)
#         return rows

# async def get_cars(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT registration_number, model, parking_spot_number
#             FROM Car
#             WHERE resident_house_number = $1
#         """, house_number)
#         return rows

# async def get_booked_amenities(house_number):
#     async with db_pool.acquire() as conn:
#         rows = await conn.fetch("""
#             SELECT A.Amenity_Name, R.Booking_Date, R.Start_Time, R.End_Time, R.Number_of_people
#             FROM Resident_Books_Amenity R
#             JOIN Amenities A ON A.Amenity_ID = R.Amenity_ID
#             WHERE R.House_Number = $1
#         """, house_number)
#         return rows

# asyncio.run(connect_to_db())
# st.set_page_config(page_title="SmartGate Dashboard", layout="wide")

# if not st.session_state.logged_in:
#     st.title("🔐 Login to SmartGate")

#     user_type = st.selectbox("Login as", ["Resident", "Guard"])
#     user_id = st.text_input("Enter House Number" if user_type == "Resident" else "Enter Badge Number")
#     password = st.text_input("Enter Password", type="password")

#     if st.button("Login"):
#         if password != "1234":
#             st.error("Incorrect password.")
#         elif not user_id.strip().isdigit():
#             st.error("Please enter a valid numeric ID.")
#         else:
#             user_id = int(user_id.strip())
#             if user_type == "Resident":
#                 if asyncio.run(is_valid_resident(user_id)):
#                     st.session_state.logged_in = True
#                     st.session_state.user_type = "Resident"
#                     st.session_state.user_id = user_id
#                     st.success("Resident login successful.")
#                     st.rerun()

#                 else:
#                     st.error("House number not found.")
#             else:
#                 if asyncio.run(is_valid_guard(user_id)):
#                     st.session_state.logged_in = True
#                     st.session_state.user_type = "Guard"
#                     st.session_state.user_id = user_id
#                     st.success("Guard login successful.")
#                     st.rerun()

#                 else:
#                     st.error("Badge number not found.")
#     st.stop()

# # Place the rest of your dashboard code here

# user_id = st.session_state.user_id

# # --- HEADER ---
# with st.container():
#     cols = st.columns([2, 8, 2])
#     with cols[0]:
#         st.markdown("### SmartGate")
#     with cols[1]:
#         st.markdown(f"{datetime.now().strftime('%B %d, %Y %I:%M %p')}")
#     with cols[2]:
#         st.image("https://randomuser.me/api/portraits/women/44.jpg", width=40)
#         st.markdown(f"{st.session_state.user_type} {user_id}")

# st.markdown("---")

# # --- SIDEBAR ---
# with st.sidebar:
#     st.markdown("## 📋 Dashboard")
#     st.button("🏠 Dashboard")
#     st.button("🧑‍🤝‍🧑 My Visitors")
#     st.button("📅 Book Amenity")
#     st.button("🛠 Order Services")
#     st.button("🚗 My Cars")

# # --- MAIN DASHBOARD HEADER ---
# st.markdown(f"## Hi, {st.session_state.user_type} {user_id}Welcome back!")
# st.markdown("Here's a quick overview of your society activities.")

# # --- MAIN GRID ---
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("### Add Visitor")
#     visitor_name = st.text_input("Visitor Name")
#     visit_date = st.date_input("Date of Visit")
#     purpose = st.text_input("Purpose")
#     st.text_input("Passkey", value=str(generate_passkey()), disabled=True)

#     if st.button("Submit") and visitor_name and purpose:
#         full_visit_time = visit_date
#         visit_id = full_visit_time.year + full_visit_time.month + full_visit_time.day

#         async def add_visitor():
#             async with db_pool.acquire() as conn:
#                 await conn.execute("""
#                     INSERT INTO Visitor (Visitor_ID, Visitor_Name, Phone_Number, Has_Passkey, Visit_Purpose)
#                     VALUES ($1, $2, $3, $4, $5)
#                 """, visit_id, visitor_name, "9876543210", True, purpose)

#         asyncio.run(add_visitor())
#         add_log(f"Visitor added: *{visitor_name}*")
#         st.success("Visitor added to the system.")

#     bookings = asyncio.run(get_booked_amenities(user_id))
#     if bookings:
#         df_amenities = pd.DataFrame([dict(row) for row in bookings])
#         df_amenities.columns = ["Amenity", "Date", "Start", "End", "People"]
#         st.markdown("### Booked Amenities")
#         st.table(df_amenities)

#     st.markdown("### ➕ Book a New Amenity")
#     amenities = asyncio.run(get_all_amenities())
#     if amenities:
#         amenity_options = [f"{row['amenity_name']} ({row['availability_status']})" for row in amenities]
#         selected = st.selectbox("Select Amenity", amenity_options, key="amenity_select")
#         selected_amenity = amenities[amenity_options.index(selected)]

#         booking_date = st.date_input("Booking Date", datetime.now().date(), key="amenity_date")
#         start_time = st.time_input("Start Time", datetime.strptime("10:00", "%H:%M").time(), key="amenity_start")
#         end_time = st.time_input("End Time", datetime.strptime("11:00", "%H:%M").time(), key="amenity_end")
#         num_people = st.number_input("Number of People", min_value=1, max_value=20, value=1, key="amenity_people")

#         if st.button("Book Amenity"):
#             booking_id = int(time.time())
#             async def book_amenity():
#                 async with db_pool.acquire() as conn:
#                     await conn.execute("""
#                         INSERT INTO Resident_Books_Amenity (
#                             House_Number, Amenity_ID, Booking_ID, Booking_Date, Start_Time, End_Time, Number_of_people
#                         ) VALUES ($1, $2, $3, $4, $5, $6, $7)
#                     """, user_id, selected_amenity["amenity_id"], booking_id, booking_date, start_time, end_time, num_people)
#             asyncio.run(book_amenity())
#             add_log(f"Booked amenity: *{selected_amenity['amenity_name']}* on {booking_date}")
#             st.success("Amenity booked successfully!")
#     else:
#         st.warning("No amenities available.")

#     st.markdown("### My Cars")
#     cars = asyncio.run(get_cars(user_id))
#     if cars:
#         df_cars = pd.DataFrame([dict(row) for row in cars])
#         df_cars.columns = ["Registration Number", "Model", "Parking Spot"]
#         st.table(df_cars)
#     else:
#         st.info("No cars registered.")

# with col2:
#     st.markdown("### My Visitors")
#     visitors = asyncio.run(get_visitors(house_number))
#     df_visitors = pd.DataFrame(visitors)
#     df_visitors.columns = ["Visitor Name", "Visit Purpose", "Phone Number"]
#     st.table(df_visitors)

#     st.markdown("### Service Orders")
#     orders = asyncio.run(get_service_orders(user_id))
#     if orders:
#         order_data = [{
#             "Order ID": row["order_id"],
#             "Service": row["service_name"],
#             "Date": row["date"].strftime("%b %d, %Y"),
#             "Time": row["time"].strftime("%I:%M %p"),
#             "Status": row["delivery_status"]
#         } for row in orders]
#         st.table(order_data)
#     else:
#         st.info("No service orders found.")

#     st.markdown("### 📦 Order a Service")
#     services = asyncio.run(get_all_services())
#     if services:
#         service_names = [f"{row['service_name']} (by {row['provider_name']} - ₹{row['cost']})" for row in services]
#         selected = st.selectbox("Select Service", service_names)
#         selected_service = services[service_names.index(selected)]

#         order_date = st.date_input("Order Date", datetime.now().date())
#         order_time = st.time_input("Order Time", datetime.now().time())

#         if st.button("Place Order"):
#             order_id = int(time.time())
#             async def place_order():
#                 async with db_pool.acquire() as conn:
#                     await conn.execute("""
#                         INSERT INTO Resident_Orders_Service (House_Number, Service_ID, Order_ID, Date, Time, Delivery_Status)
#                         VALUES ($1, $2, $3, $4, $5, $6)
#                     """, user_id, selected_service["service_id"], order_id, order_date, order_time, "Pending")
#             asyncio.run(place_order())
#             add_log(f"Ordered service: *{selected_service['service_name']}*")
#             st.success("Service ordered successfully!")
#     else:
#         st.warning("No services available.")

#     st.markdown("### Activity Log")
#     for log_entry in st.session_state.activity_log:
#         st.markdown(f"- {log_entry}")

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
import pandas as pd
import random
from datetime import datetime

nest_asyncio.apply()
load_dotenv()

house_number = 3001
DB_URL = os.getenv("URI")
db_pool = None

query_params = st.query_params
params = st.query_params
page = query_params.get("page", "login")

if "activity_log" not in st.session_state:
    st.session_state.activity_log = ["You logged in!"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_id = None

async def connect_to_db():
    global db_pool
    if not db_pool:
        db_pool = await asyncpg.create_pool(dsn=DB_URL,min_size = 1,max_size = 1)

async def disconnect_from_db():
    global db_pool
    if db_pool:
        await db_pool.close()

async def get_connection():
    global db_pool
    return await db_pool.acquire()

async def is_valid_resident(house_number):
    async with db_pool.acquire() as conn:
        result = await conn.fetchval("SELECT COUNT(*) FROM Resident WHERE House_Number = $1", house_number)
        return result > 0

async def is_valid_guard(badge_number):
    async with db_pool.acquire() as conn:
        result = await conn.fetchval("SELECT COUNT(*) FROM Guard WHERE Badge_Number = $1", badge_number)
        return result > 0

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

async def get_all_amenities():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT Amenity_ID, Amenity_Name, Availability_Status, Operating_Hours
            FROM Amenities
            ORDER BY Amenity_Name
        """)
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

async def get_visitors(house_number):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT V.visitor_name, V.visit_purpose, V.phone_number
            FROM Visitor V
            JOIN Permissions P ON V.Visitor_ID = P.Visitor_ID
            WHERE P.Resident_House_Number = $1;
        """,house_number)
        return rows

def add_log(message):
    timestamp = datetime.now().strftime("%I:%M %p")
    st.session_state.activity_log.insert(0, f"{timestamp} {message}")

async def get_activity_log(house_number):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT Activity_Description, Timestamp
            FROM Activity_Log
            WHERE House_Number = $1
            ORDER BY Timestamp DESC
        """, house_number)
        return rows

async def get_cars(house_number):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT registration_number, model, parking_spot_number
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


async def generate_unique_permission_id(conn):
    while True:
        pid = random.randint(100000, 999999)  # or any suitable range
        exists = await conn.fetchval("SELECT 1 FROM Permissions WHERE Permission_ID = $1", pid)
        if not exists:
            return pid

# Connect to the database
asyncio.run(connect_to_db())
st.set_page_config(page_title="SmartGate Dashboard", layout="wide")

def resident_dashboard():
    from datetime import datetime
    import pandas as pd
    import asyncio
    import time

    user_id = st.session_state.user_id

    if "resident_section" not in st.session_state:
        st.session_state.resident_section = "dashboard"

    # HEADER
    with st.container():
        cols = st.columns([2, 8, 2])
        with cols[0]:
            st.markdown("### SmartGate")
        with cols[1]:
            st.markdown(f"{datetime.now().strftime('%B %d, %Y %I:%M %p')}")
        with cols[2]:
            st.image("https://randomuser.me/api/portraits/women/44.jpg", width=40)
            st.markdown(f"{st.session_state.user_type} {user_id}")

    st.markdown("---")

    # SIDEBAR
    with st.sidebar:
        st.markdown("## 📋 Dashboard")
        if st.button("🏠 Dashboard"):
            st.session_state.resident_section = "dashboard"
        if st.button("🧑‍🤝‍🧑 My Visitors"):
            st.session_state.resident_section = "visitors"
        if st.button("📅 Book Amenity"):
            st.session_state.resident_section = "book_amenity"
        if st.button("🛠 Order Services"):
            st.session_state.resident_section = "services"
        if st.button("🚗 My Cars"):
            st.session_state.resident_section = "cars"
        st.markdown("---")
        if st.button("🔓 Logout"):
            for key in ["logged_in", "user_type", "user_id", "activity_log", "resident_section"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # MAIN BODY CONTENT
    section = st.session_state.resident_section
    house_number = user_id  # Assuming user_id maps to house number

    if section == "dashboard":
        st.markdown(f"## Hi, {st.session_state.user_type} {user_id} — Welcome back!")
        st.markdown("Here's a quick overview of your society activities.")

        async def fetch_stats(house_number):
            async with db_pool.acquire() as conn:
                visitors = await conn.fetchval("""
                    SELECT COUNT(*) FROM Permissions WHERE Resident_House_Number = $1
                """, house_number)

                cars = await conn.fetchval("""
                    SELECT COUNT(*) FROM Car WHERE Resident_House_Number = $1
                """, house_number)

                amenities = await conn.fetchval("""
                    SELECT COUNT(*) FROM Resident_Books_Amenity WHERE House_Number = $1
                """, house_number)

                services = await conn.fetchval("""
                    SELECT COUNT(*) FROM Resident_Orders_Service WHERE House_Number = $1
                """, house_number)

                return {
                    "Visitors Approved": visitors or 0,
                    "Cars Registered": cars or 0,
                    "Amenities Booked": amenities or 0,
                    "Services Ordered": services or 0
                }

        stats = asyncio.run(fetch_stats(user_id))

        col1, col2 = st.columns(2)
        with col1:
            st.metric("👥 Visitors Approved", stats["Visitors Approved"])
            st.metric("🚗 Cars Registered", stats["Cars Registered"])
        with col2:
            st.metric("🏓 Amenities Booked", stats["Amenities Booked"])
            st.metric("🧹 Services Ordered", stats["Services Ordered"])

    elif section == "visitors":
        st.markdown("## 🧑‍🤝‍🧑 My Visitors")

        async def get_my_visitors(house_number):
            async with db_pool.acquire() as conn:
                return await conn.fetch("""
                    SELECT v.Visitor_ID, v.Visitor_Name, v.Phone_Number, v.Has_Passkey, v.Visit_Purpose
                    FROM Permissions p
                    JOIN Visitor v ON p.Visitor_ID = v.Visitor_ID
                    WHERE p.Resident_House_Number = $1
                """, house_number)

        async def approve_passkey(visitor_id):
            async with db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE Visitor
                    SET Has_Passkey = TRUE
                    WHERE Visitor_ID = $1
                """, visitor_id)

        visitors = asyncio.run(get_my_visitors(house_number))
        search = st.text_input("🔍 Search Visitor by Name or Phone")

        pending_visitors = [v for v in visitors if not v['has_passkey'] and (search.lower() in v['visitor_name'].lower() or search in v['phone_number'])]
        approved_visitors = [v for v in visitors if v['has_passkey'] and (search.lower() in v['visitor_name'].lower() or search in v['phone_number'])]

        if pending_visitors:
            st.markdown("### ⏳ Visitors Pending Approval")
            for v in pending_visitors:
                with st.container():
                    st.markdown(f"**{v['visitor_name']}** - {v['phone_number']} ({v['visit_purpose']})")
                    if st.button(f"✅ Approve {v['visitor_name']}", key=f"approve_{v['visitor_id']}"):
                        asyncio.run(approve_passkey(v['visitor_id']))
                        st.success(f"{v['visitor_name']} approved successfully!")
                        st.rerun()


        st.markdown("### ✅ Approved Visitors")
        if approved_visitors:
            df_approved = pd.DataFrame([{
                "Name": v['visitor_name'],
                "Phone": v['phone_number'],
                "Purpose": v['visit_purpose']
            } for v in approved_visitors])
            st.table(df_approved)
        else:
            st.info("No approved visitors found.")

        # Add Visitor Section
        st.markdown("---")
        st.markdown("### ➕ Add Visitor")
        visitor_name = st.text_input("Visitor Name")
        visit_date = st.date_input("Date of Visit")
        purpose = st.text_input("Purpose")
        st.text_input("Passkey", value=str(generate_passkey()), disabled=True)

        if st.button("Submit") and visitor_name and purpose:
            full_visit_time = visit_date
            visit_id = full_visit_time.year + full_visit_time.month + full_visit_time.day

            async def add_visitor():
                async with db_pool.acquire() as conn:
                    async with conn.transaction():
                        permission_id = await generate_unique_permission_id(conn)

                        await conn.execute("""
                            INSERT INTO Visitor (Visitor_ID, Visitor_Name, Phone_Number, Has_Passkey, Visit_Purpose)
                            VALUES ($1, $2, $3, $4, $5)
                        """, visit_id, visitor_name, "9876543210", True, purpose)

                        await conn.execute("""
                            INSERT INTO Permissions (Permission_ID, Issue_Time, Approval_Status, Resident_House_Number, Visitor_ID, Guard_Badge_Number)
                            VALUES ($1, $2, $3, $4, $5, $6)
                        """, permission_id, datetime.now(), True, house_number, visit_id, 1001)

                        await conn.execute("""
                            INSERT INTO Permission_Asked_From_Resident (Permission_ID, House_Number)
                            VALUES ($1, $2)
                        """, permission_id, house_number)

                        await conn.execute("""
                            INSERT INTO Permission_Asked_For_Visitor (Permission_ID, Visitor_ID)
                            VALUES ($1, $2)
                        """, permission_id, visit_id)

            asyncio.run(add_visitor())
            add_log(f"Visitor added: **{visitor_name}**")
            st.success("Visitor added to the system.")

    elif section == "book_amenity":
        bookings = asyncio.run(get_booked_amenities(user_id))
        if bookings:
            df_amenities = pd.DataFrame([dict(row) for row in bookings])
            df_amenities.columns = ["Amenity", "Date", "Start", "End", "People"]
            st.markdown("### Booked Amenities")
            st.table(df_amenities)

        st.markdown("### ➕ Book a New Amenity")
        amenities = asyncio.run(get_all_amenities())
        if amenities:
            amenity_options = [f"{row['amenity_name']} ({row['availability_status']})" for row in amenities]
            selected = st.selectbox("Select Amenity", amenity_options, key="amenity_select")
            selected_amenity = amenities[amenity_options.index(selected)]

            booking_date = st.date_input("Booking Date", datetime.now().date(), key="amenity_date")
            start_time = st.time_input("Start Time", datetime.strptime("10:00", "%H:%M").time(), key="amenity_start")
            end_time = st.time_input("End Time", datetime.strptime("11:00", "%H:%M").time(), key="amenity_end")
            num_people = st.number_input("Number of People", min_value=1, max_value=20, value=1, key="amenity_people")

            if st.button("Book Amenity"):
                booking_id = int(time.time())

                async def book_amenity():
                    async with db_pool.acquire() as conn:
                        await conn.execute("""
                            INSERT INTO Resident_Books_Amenity (
                                House_Number, Amenity_ID, Booking_ID, Booking_Date, Start_Time, End_Time, Number_of_people
                            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                        """, user_id, selected_amenity["amenity_id"], booking_id, booking_date, start_time, end_time, num_people)

                asyncio.run(book_amenity())
                add_log(f"Booked amenity: *{selected_amenity['amenity_name']}* on {booking_date}")
                st.success("Amenity booked successfully!")
        else:
            st.warning("No amenities available.")

    elif section == "services":
        st.markdown("### Service Orders")
        orders = asyncio.run(get_service_orders(user_id))
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
        services = asyncio.run(get_all_services())
        if services:
            service_names = [f"{row['service_name']} (by {row['provider_name']} - ₹{row['cost']})" for row in services]
            selected = st.selectbox("Select Service", service_names)
            selected_service = services[service_names.index(selected)]

            order_date = st.date_input("Order Date", datetime.now().date())
            order_time = st.time_input("Order Time", datetime.now().time())

            if st.button("Place Order"):
                order_id = int(time.time())

                async def place_order():
                    async with db_pool.acquire() as conn:
                        await conn.execute("""
                            INSERT INTO Resident_Orders_Service (House_Number, Service_ID, Order_ID, Date, Time, Delivery_Status)
                            VALUES ($1, $2, $3, $4, $5, $6)
                        """, user_id, selected_service["service_id"], order_id, order_date, order_time, "Pending")
                        add_log(f"Ordered service: *{selected_service['service_name']}*")

                asyncio.run(place_order())
                st.success("Service ordered successfully!")
        else:
            st.warning("No services available.")

    elif section == "cars":
        st.markdown("### My Cars")
        cars = asyncio.run(get_cars(user_id))
        if cars:
            df_cars = pd.DataFrame([dict(row) for row in cars])
            df_cars.columns = ["Registration Number", "Model", "Parking Spot"]
            st.table(df_cars)
        else:
            st.info("No cars registered.")

    # Activity Log (optional in all views)
    st.markdown("---")
    st.markdown("### Activity Log")
    for log_entry in st.session_state.activity_log:
        st.markdown(f"- {log_entry}")

def guard_dashboard():
    import streamlit as st
    import asyncio
    import asyncpg
    from datetime import datetime

    async def get_guard_info(badge_number):
        async with db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT Shift_Timings, Date_Of_Joining
                FROM Guard
                WHERE Badge_Number = $1
            """, badge_number)
            return row

    async def get_visitorsGuard():
        async with db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT v.*
                FROM Visitor v
                JOIN Permissions o ON v.Visitor_ID = o.Visitor_ID
                WHERE o.approval_status = TRUE;
            """)
            return rows

    async def get_cars():
        async with db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT *
                FROM Car
                ORDER BY Model
            """)
            return rows

    async def request_visitor_permission(visitor_name, phone_number, purpose, house_number, badge_number):
        async with db_pool.acquire() as conn:
            full_visit_time = datetime.now()
            date_part = full_visit_time.strftime("%Y%m%d")
            time_suffix = str(int(full_visit_time.timestamp() * 1000))[-4:]
            visitor_id = int(date_part + time_suffix)
            visitor_id = visitor_id%10000
            permission_id = await generate_unique_permission_id(conn)
            async with conn.transaction():
                # Step 1: Insert visitor
                await conn.fetchval("""
                    INSERT INTO Visitor (Visitor_id,Visitor_Name, Phone_Number, Has_Passkey, Visit_Purpose)
                    VALUES ($1, $2, $3, $4,$5)
                """, visitor_id,visitor_name, phone_number, False, purpose)

                # Step 2: Insert permission request
                await conn.fetchval("""
                    INSERT INTO Permissions (Permission_id, Issue_Time, Approval_Status, Resident_House_Number, Visitor_ID, Guard_Badge_Number)
                    VALUES ($1,CURRENT_TIMESTAMP, FALSE, $2, $3, $4)
                """, permission_id,house_number, visitor_id, badge_number)

                # Step 3: Link in Guard_Asks_For_Permission
                await conn.execute("""
                    INSERT INTO Guard_Asks_For_Permission (Guard_ID, Permission_ID, Request_Timestamp)
                    VALUES ($1, $2, CURRENT_TIMESTAMP)
                """, badge_number, permission_id)

                # Step 4: Insert into permission_asked_from_resident table
                await conn.execute("""
                    INSERT INTO permission_asked_from_resident (permission_id, house_number)
                    VALUES ($1, $2)
                """, permission_id, house_number)

            result = asyncio.run(request_visitor_permission(visitor_name, phone_number, purpose, house_number, badge))
            st.success(f"Requested permission for visitor {visitor_name} (ID: {result['visitor_id']}) to house {house_number}")

            return {"visitor_id": visitor_id, "permission_id": permission_id}


    user_id = st.session_state.user_id
    badge = user_id

    st.markdown(f"## Hi, Guard {user_id} — Welcome back!")

    if "guard_section" not in st.session_state:
        st.session_state.guard_section = "dashboard"

    # SIDEBAR
    with st.sidebar:
        st.markdown("## 📋 Dashboard")
        if st.button("🏠 Dashboard"):
            st.session_state.guard_section = "dashboard"
        if st.button("🧑‍🤝‍🧑 My Shifts"):
            st.session_state.guard_section = "shifts"
        if st.button("📅 Allow Visitors"):
            st.session_state.guard_section = "allow_visitors"
        if st.button("🚗 Allow Cars"):
            st.session_state.guard_section = "allow_cars"
        if st.button("🛠 Request Permission"):
            st.session_state.guard_section = "request_permission"
        st.markdown("---")
        if st.button("🔓 Logout"):
            for key in ["logged_in", "user_type", "user_id", "activity_log", "guard_section"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # SECTION ROUTING
    section = st.session_state.guard_section

    if section == "dashboard":
        st.markdown("### Overview")
        col1, col2 = st.columns(2)
        col1.metric("Visitors Checked", 23)
        col2.metric("Cars Allowed", 14)

    elif section == "shifts":
        shift, doj = asyncio.run(get_guard_info(badge))
        st.markdown("### 🧑‍💼 My Shifts")
        st.info(f"**Shift Timing:** {shift}")
        st.info(f"**Date of Joining:** {doj.strftime('%B %d, %Y')}")

    elif section == "allow_visitors":
        st.markdown("### 📅 Allow Visitors")
        visitors = asyncio.run(get_visitorsGuard())
        search = st.text_input("Search Visitor by Name or Phone")
        
        for v in visitors:
            if search.lower() in v['visitor_name'].lower() or search in v['phone_number']:
                st.markdown(f"**{v['visitor_name']}** - {v['phone_number']}")
                if st.button(f"✅ Allow {v['visitor_name']}", key=v['visitor_id']):
                    
                    # Approve the visitor by updating Permissions table
                    async def approve_visitor(visitor_id):
                        async with db_pool.acquire() as conn:
                            # Update the Permission record to set Approval_Status = TRUE
                            await conn.execute("""
                                UPDATE Permissions
                                SET Approval_Status = TRUE
                                WHERE Visitor_ID = $1
                            """, visitor_id)
                    
                    # Call the function to approve the visitor
                    asyncio.run(approve_visitor(v['visitor_id']))
                    st.success(f"{v['visitor_name']} allowed!")
                    add_log(f"Visitor {v['visitor_name']} approved by Guard {badge}")

    elif section == "allow_cars":
        st.markdown("### 🚗 Allow Cars")
        cars = asyncio.run(get_cars())
        search = st.text_input("Search Car by Reg Number or Model")
        for c in cars:
            if search.lower() in c['model'].lower() or search in c['registration_number']:
                st.markdown(f"**{c['model']}** - {c['registration_number']}")
                if st.button(f"✅ Allow {c['model']}", key=c['car_number']):
                    st.success(f"Car {c['model']} allowed!")

    elif section == "request_permission":
        st.markdown("### 🛠 Request Visitor Permission")
        
        # Collect required information
        visitor_name = st.text_input("Visitor Name")
        phone_number = st.text_input("Phone Number")
        purpose = st.text_input("Visit Purpose")
        house_number = st.text_input("House Number")
        st.text_input("Badge Number", value=str(badge), disabled=True)
        # Button to request permission
        if st.button("📨 Request Permission"):
            # You need to update the function to take these arguments
            asyncio.run(request_visitor_permission(visitor_name, phone_number, purpose, int(house_number), badge))
            st.success(f"Requested permission for visitor {visitor_name} to house {house_number}")

if page == "resident" and st.session_state.logged_in:
    resident_dashboard()
    st.stop()
elif page == "guard" and st.session_state.logged_in:
    guard_dashboard()
    st.stop()
    
# LOGIN SECTION
if not st.session_state.logged_in:
    st.title("🔐 Login to SmartGate")

    user_type = st.selectbox("Login as", ["Resident", "Guard"])
    user_id = st.text_input("Enter House Number" if user_type == "Resident" else "Enter Badge Number")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if password != "1234":
            st.error("Incorrect password.")
        elif not user_id.strip().isdigit():
            st.error("Please enter a valid numeric ID.")
        else:
            user_id = int(user_id.strip())
            if user_type == "Resident":
                if asyncio.run(is_valid_resident(user_id)):
                    st.session_state.logged_in = True
                    st.session_state.user_type = "Resident"
                    st.session_state.user_id = user_id
                    st.query_params["page"] = "resident"
                    st.rerun()
                else:
                    st.error("House number not found.")
            else:
                if asyncio.run(is_valid_guard(user_id)):
                    st.session_state.logged_in = True
                    st.session_state.user_type = "Guard"
                    st.session_state.user_id = user_id
                    st.query_params["page"] = "guard"
                    st.rerun()
                else:
                    st.error("Badge number not found.")
    st.stop()
