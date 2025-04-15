# 🛡️ SmartGate Visitor Management System

SmartGate is a secure, user-friendly gate management solution designed for residential societies. It digitizes the flow of permissions, logs, and entries at the gate, allowing residents and guards to seamlessly manage visitor and vehicle entries in real-time.

---

## 🚀 Features

### 👤 Resident Dashboard
- View and manage approved visitors
- Book amenities (clubhouse, gym, etc.)
- Register personal vehicles
- Order services (e.g. maid, plumber)
- Track activity logs of all interactions

### 🧍‍♂️ Guard Dashboard
- Approve visitor entries based on permissions
- Allow cars based on registration details
- Request permission from residents on the fly
- Maintain logs of all actions (visitor/car approvals)
- View assigned shift and joining details

---

## 📦 Tech Stack

| Component         | Technology         |
|------------------|--------------------|
| Frontend         | [Streamlit](https://streamlit.io/) |
| Backend (async)  | [asyncpg](https://magicstack.github.io/asyncpg/) + PostgreSQL |
| UI Framework     | Streamlit native + Custom CSS |
| ORM              | Raw SQL Queries    |
| State Handling   | `st.session_state` |

---

## 🗄️ Database Schema

The system uses the following key tables:

- **Resident** (house_number, name, password)
- **Visitor** (visitor_id, name, phone, visit_purpose, has_passkey)
- **Permissions** (permission_id, resident_house_number, visitor_id, guard_badge_number, issue_time, approval_status)
- **Guard** (badge_number, shift_timings, date_of_joining)
- **Car** (car_number, registration_number, model, resident_house_number)
- **Log** (date, time, visitor_id, car_id) — ✅ Used for activity history
- **Guard_Asks_For_Permission**
- **Permission_Asked_From_Resident / For_Visitor**
- **Resident_Books_Amenity**, **Amenities**
- **Resident_Orders_Service**, **Services**

---

## 🧑‍💻 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/CobaltIII/My-gate-trial.git
```

### 2. Setup Python Environment
```bash
conda create -n smartgate python=3.10
conda activate smartgate
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file in the root directory:
```
URI= private right now
```

### 4. Run the Streamlit App
```bash
streamlit run home.py
```

---

## 📂 File Structure

```
smartgate/
│
├── home.py                  # Main Streamlit app
├── .env                     # Database credentials
├── requirements.txt         # All dependencies
├── README.md                # Project documentation
└── /assets                  # (Optional) images/icons
```

---

## 🧪 Demo Credentials

| Role      | ID      | Password |
|-----------|---------|----------|
| Resident  | 3001    | 1234     |
| Guard     | 1001    | 1234     |

---
