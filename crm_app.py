import streamlit as st
import pandas as pd
from datetime import datetime
import os

FILENAME = "clients.csv"

# Load or create CSV
if not os.path.exists(FILENAME):
    df = pd.DataFrame(columns=["Timestamp", "Name", "Contact", "Email", "Purpose", "Niche"])
    df.to_csv(FILENAME, index=False)
else:
    df = pd.read_csv(FILENAME)

st.title("📇 Client CRM Manager")

# Add new client
st.header("➕ Add New Client")
with st.form("client_form"):
    name = st.text_input("Client Name")
    contact = st.text_input("Contact Number")
    email = st.text_input("Email Address")
    purpose = st.text_input("Purpose of Engagement")
    niche = st.text_input("Client Niche/Industry")
    submitted = st.form_submit_button("Add Client")

    if submitted:
        new_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Contact": contact,
            "Email": email,
            "Purpose": purpose,
            "Niche": niche
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(FILENAME, index=False)
        st.success("✅ Client added successfully!")

# View clients
st.header("📋 Client List")
st.dataframe(df)
