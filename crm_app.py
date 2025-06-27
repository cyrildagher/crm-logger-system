import streamlit as st
import pandas as pd
from datetime import datetime
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

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

# --- Search Bar ---
st.header("📋 Client List")
search = st.text_input("🔍 Search by Name or Niche")
if search:
    filtered_df = df[df['Name'].str.contains(search, case=False, na=False) | df['Niche'].str.contains(search, case=False, na=False)]
else:
    filtered_df = df.copy()

# --- AgGrid Table ---
gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination()
gb.configure_default_column(editable=True, groupable=True)
gb.configure_selection('single', use_checkbox=True)
gb.configure_grid_options(domLayout='normal')

# Add a delete button column
if 'delete_row' not in st.session_state:
    st.session_state.delete_row = None

grid_options = gb.build()
grid_response = AgGrid(
    filtered_df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    allow_unsafe_jscode=True,
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=True,
    height=400,
    width='100%'
)

selected = grid_response['selected_rows']

# --- Edit and Delete Buttons ---
if selected:
    selected_row = selected[0]
    st.write(f"Selected: **{selected_row['Name']}** | {selected_row['Email']} | {selected_row['Purpose']}")
    col1, col2 = st.columns(2)
    if col1.button("✏️ Edit Selected"):
        st.session_state.edit_index = df[(df['Timestamp'] == selected_row['Timestamp']) & (df['Name'] == selected_row['Name'])].index[0]
        st.info("Edit functionality can be implemented here.")
    if col2.button("🗑️ Delete Selected"):
        st.session_state.delete_row = selected_row

# --- Confirmation Dialog for Delete ---
if st.session_state.get('delete_row') is not None:
    with st.modal("Confirm Delete"):
        st.warning(f"Are you sure you want to delete client: **{st.session_state.delete_row['Name']}**?")
        confirm_col1, confirm_col2 = st.columns(2)
        if confirm_col1.button("Yes, Delete"):
            idx = df[(df['Timestamp'] == st.session_state.delete_row['Timestamp']) & (df['Name'] == st.session_state.delete_row['Name'])].index
            if not idx.empty:
                df.drop(idx, inplace=True)
                df.to_csv(FILENAME, index=False)
                st.success("Client deleted.")
            st.session_state.delete_row = None
            st.experimental_rerun()
        if confirm_col2.button("Cancel"):
            st.session_state.delete_row = None
            st.experimental_rerun()
