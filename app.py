import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
import csv


credentials_dict = {
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    "universe_domain": st.secrets["universe_domain"]
}



# Convert the dictionary to ServiceAccountCredentials object
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

# Open the spreadsheet
gc = gspread.authorize(credentials)
spreadsheet_id = '16M1g3sCR38HW1muj4IzgcpPhZBOkzWh0xOET_XtCZsc'
sheet = gc.open_by_key(spreadsheet_id).sheet1

# Get all values from the sheet
data = sheet.get_all_values()

# Create a pandas DataFrame from the retrieved data
df = pd.DataFrame(data[1:], columns=data[0])  # Skip header row

def filter_data(df, filters):
    filtered_df = df.copy()
    for col, value in filters.items():
        if value is not None:  # Check if value is None before applying filter
            filtered_df = filtered_df[filtered_df[col] == value]
    return filtered_df

filters = {}
st.title('Centralised Data System for TMA')

# Instructions
st.header('How to use:')
st.markdown('1. Apply the Filters using the sidebar options.')
st.markdown('2. Click on the "Filtered Data" button to filtered the data.')
st.markdown('3. Click on "Download symbol" button to download the filtered data.')


with st.sidebar:
    # Add filter options dynamically based on data types
    for col in df.columns:
        if df[col].dtype == object:
            filters[col] = st.selectbox(f"Filter {col}", [None] + list(df[col].unique()), key=f"filter_{col}")  # Set default to None and include all unique values
        else:
            filters[col] = st.selectbox(f"Filter {col}", [None] + list(df[col].unique()), key=f"filter_{col}")  # Set default to None and include all unique values

    # Use a separate variable for button creation to avoid loop issues
    button_clicked = st.button("Apply Filters")

# Apply filters after clicking the button
if button_clicked:
    filtered_df = filter_data(df.copy(), filters)
    st.dataframe(filtered_df)

