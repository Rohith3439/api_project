import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Leave Management System", layout="wide")

# =============================
# GLOBAL STYLE
# =============================
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.stTextInput>div>div>input {
    border-radius: 8px;
}

.stButton>button {
    width: 100%;
    height: 45px;
    border-radius: 8px;
    background-color: #1f4e79;
    color: white;
}

.card {
    background-color: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# =============================
# SESSION
# =============================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# =============================
# LOGIN PAGE
# =============================
def login_page():

    st.image("slide2_clean.png", width='stretch')

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("## 🔐 Login")

        emp_id = st.text_input("Employee ID")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            res = requests.post(f"{API}/login", json={
                "employee_id": emp_id,
                "password": password
            })

            if res.status_code == 200:
                data = res.json()
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = data["user_id"]
                st.session_state["role"] = data["role"]
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown('</div>', unsafe_allow_html=True)

# =============================
# EMPLOYEE DASHBOARD
# =============================
def employee_dashboard():

    st.sidebar.title("👤 Employee Menu")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.title("📊 Employee Dashboard")

    tabs = st.tabs(["Apply Leave", "My Leaves", "Update Leave", "Delete Leave"])

    # APPLY
    with tabs[0]:
        st.subheader("Apply Leave")

        lt = st.text_input("Leave Type")
        s = st.date_input("Start Date")
        e = st.date_input("End Date")
        r = st.text_area("Reason")

        if st.button("Apply Leave"):
            res = requests.post(f"{API}/leave", json={
                "user_id": st.session_state["user_id"],
                "leave_type": lt,
                "start_date": str(s),
                "end_date": str(e),
                "reason": r
            })

            if res.status_code == 200:
                st.success("Leave Applied")
            else:
                st.error(res.text)

    # VIEW
    with tabs[1]:
        st.subheader("My Leaves")

        res = requests.get(f"{API}/leave/{st.session_state['user_id']}")

        if res.status_code == 200:
            data = res.json()

            if data:
                df = pd.DataFrame(data)

                df.columns = [
                    "Leave ID",
                    "User ID",
                    "Type",
                    "Start Date",
                    "End Date",
                    "Reason",
                    "Status"
                ]

                st.dataframe(df, width='stretch')
            else:
                st.info("No records")

    # UPDATE (DROPDOWN)
    with tabs[2]:
        st.subheader("Update Leave")

        res = requests.get(f"{API}/leave/{st.session_state['user_id']}")

        if res.status_code == 200:
            data = res.json()

            if data:
                df = pd.DataFrame(data)

                df["display"] = (
                    "ID " + df["id"].astype(str) + " | " +
                    df["leave_type"] + " | " +
                    df["start_date"] + " → " + df["end_date"]
                )

                selected = st.selectbox("Select Leave", df["display"])

                selected_row = df[df["display"] == selected].iloc[0]
                leave_id = selected_row["id"]

                new_start = st.date_input("New Start Date", pd.to_datetime(selected_row["start_date"]))
                new_end = st.date_input("New End Date", pd.to_datetime(selected_row["end_date"]))
                new_reason = st.text_input("New Reason", value=selected_row["reason"])

                if st.button("Update Leave"):
                    res = requests.put(f"{API}/leave/{leave_id}", json={
                        "start_date": str(new_start),
                        "end_date": str(new_end),
                        "reason": new_reason
                    })

                    if res.status_code == 200:
                        st.success("Leave Updated")
                        st.rerun()
                    else:
                        st.error(res.text)

            else:
                st.info("No leaves available")

    # DELETE (DROPDOWN)
    with tabs[3]:
        st.subheader("Delete Leave")

        res = requests.get(f"{API}/leave/{st.session_state['user_id']}")

        if res.status_code == 200:
            data = res.json()

            if data:
                df = pd.DataFrame(data)

                df["display"] = (
                    "ID " + df["id"].astype(str) + " | " +
                    df["leave_type"] + " | " +
                    df["start_date"] + " → " + df["end_date"]
                )

                selected = st.selectbox("Select Leave to Delete", df["display"], key="delete_select")

                selected_row = df[df["display"] == selected].iloc[0]
                leave_id = selected_row["id"]

                if st.button("Delete Leave"):
                    res = requests.delete(f"{API}/leave/{leave_id}")

                    if res.status_code == 200:
                        st.success("Leave Deleted")
                        st.rerun()
                    else:
                        st.error(res.text)

            else:
                st.info("No leaves available")

# =============================
# ADMIN DASHBOARD
# =============================
def admin_dashboard():

    st.sidebar.title("👨‍💼 Admin Menu")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.title("📊 Admin Dashboard")

    tab1, tab2 = st.tabs(["All Leaves", "Manage Leaves"])

    # ALL LEAVES
    with tab1:
        st.subheader("All Leave Requests")

        res = requests.get(f"{API}/all-leaves")

        if res.status_code == 200:
            data = res.json()

            if data:
                df = pd.DataFrame(data)

                df.columns = [
                    "Leave ID",
                    "Employee Name",
                    "Employee ID",
                    "Type",
                    "Start Date",
                    "End Date",
                    "Reason",
                    "Status"
                ]

                st.dataframe(df, width='stretch')
            else:
                st.info("No data")

    # MANAGE
    with tab2:
        st.subheader("Manage Leaves")

        res = requests.get(f"{API}/active-leaves")

        if res.status_code == 200:
            data = res.json()

            if data:
                for leave in data:
                    col1, col2, col3 = st.columns([4,1,1])

                    with col1:
                        st.write(f"""
                        **{leave['employee_name']} ({leave['employee_id']})**  
                        {leave['leave_type']} | {leave['start_date']} → {leave['end_date']}  
                        Reason: {leave['reason']}  
                        Status: {leave['status']}
                        """)

                    with col2:
                        if st.button("Approve", key=f"a{leave['leave_id']}"):
                            requests.put(f"{API}/approve/{leave['leave_id']}")
                            st.rerun()

                    with col3:
                        if st.button("Reject", key=f"r{leave['leave_id']}"):
                            requests.put(f"{API}/reject/{leave['leave_id']}")
                            st.rerun()

                    st.divider()
            else:
                st.info("No active leaves")

# =============================
# MAIN FLOW
# =============================
if not st.session_state["logged_in"]:
    login_page()
else:
    if st.session_state["role"] == "admin":
        admin_dashboard()
    else:
        employee_dashboard()