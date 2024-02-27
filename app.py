import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
import csv


# Replace with the path to your uploaded JSON key file
jsonPath = 'trans-maldividan-airways-600438efe5d0.json'


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file']


credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonPath, scope)
gc = gspread.authorize(credentials)

# Open a specific spreadsheet by its ID
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

# Download functionality using a dedicated function for clarity
# @st.cache
# def download_csv(data):
#     with open('filtered_data.csv', 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(data.columns)
#         writer.writerows(data.values)

# # # Download button outside the filter section
# # if st.button("Download Filtered Data", key="download_button"):  # Unique key for button
# #     if button_clicked:  # Check if filtering was applied
# #         download_csv(filtered_df)
# #         st.success("Filtered data downloaded as 'filtered_data.csv'")
# #     else:
# #         st.warning("Please apply filters first before downloading.")

# if st.button("Download Filtered Data", key="download_button"):  # Unique key for button
#     if button_clicked and not filtered_df.empty:  # Check if filtering was applied and data is not empty
#         download_csv(filtered_df)
#         st.success("Filtered data downloaded as 'filtered_data.csv'")
#     else:
#         st.warning("Please apply filters and make sure there are filtered results before downloading.")

