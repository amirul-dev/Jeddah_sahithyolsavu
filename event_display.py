import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Configure to hide Streamlit UI elements
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")

# File path to the Excel file
book_id = "1VmzWXUwhriK9VmPrJToqNxw7xaJbxChDl6LSWjNkLDc"
sheet_ids = [0]

# Function to load data from Excel (removed caching to allow reload on every run)
def load_schedule_data():
    dfs = pd.DataFrame()
    for sheet_id in sheet_ids:
        sheet_path = f"https://docs.google.com/spreadsheets/d/{book_id}/export?format=csv&gid={sheet_id}"

        # Read the sheet into a DataFrame
        df = pd.read_csv(sheet_path)
        
        # Check if the DataFrame is empty
        if not df.empty:
            dfs = pd.concat([dfs, df], ignore_index=True)
    filtered_dfs = dfs[dfs['Status'].isin(['On-Stage', 'Next'])]        
    del filtered_dfs['SI']

    return filtered_dfs

# Load data from the Excel file every time the app reruns
data = load_schedule_data()

# Define CSS for background image
bg_url = f"https://raw.githubusercontent.com/amirul-dev/jeddah_sahithyolsavu_files/refs/heads/main/bg.png"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{bg_url}");
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

github_storage = "https://raw.githubusercontent.com/amirul-dev/jeddah_sahithyolsavu_files/refs/heads/main/"

# Sidebar content
color_logo = github_storage + "color_logo.png"
new_logo = github_storage + "new_logo.png"
QR_code = github_storage + "QR2.png"
        
column1, column2 = st.columns([2,1])
        
with column1: 
    st.title("Live Event Schedule")
   
with column2:    
    unique_stages = data["Stage"].unique()
    selected_stage = st.selectbox("Choose a stage:", options=["All"] + unique_stages.tolist())

# Filter the DataFrame based on the selected stage
if selected_stage == "All":
    filtered_df = data
else:
    filtered_df = data[data["Stage"] == selected_stage]

# CSS for responsive table and styling
st.markdown(
"""
<style>
.custom-table-container {
    width: 100%;
    overflow-x: auto; /* Enable horizontal scrolling on smaller screens */
}
.custom-table {
    border-collapse: collapse;
    width: 100%; /* Make table take the full width */
    margin: 20px 0; /* Add margin for spacing */
    border-radius: 12px; /* Rounded corners for the table */
    overflow: hidden; /* Ensure rounded corners are respected */
    background-color: #2C3E50; /* Dark background color */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for a lifted effect */
}
.custom-table th, .custom-table td {
    border: 1px solid #34495E; /* Darker border color for grid */
    padding: 12px 15px; /* Padding for better spacing */
    text-align: left;
    color: white;
    font-size: 14px; /* Slightly larger font size for better readability */
}
.custom-table th {
    background-color: #1ABC9C; /* Vibrant header background */
    font-weight: bold;
    text-transform: uppercase; /* Uppercase headers */
}
.custom-table td {
    background-color: #34495E; /* Slightly lighter background for cells */
}
.custom-table tr:nth-child(even) td {
    background-color: #2C3E50; /* Alternating row colors for better readability */
}
.custom-table tr:hover td {
    background-color: #16A085; /* Hover effect for rows */
    cursor: pointer;
}

/* Responsive adjustments for mobile */
@media only screen and (max-width: 768px) {
    .custom-table th, .custom-table td {
        font-size: 12px; /* Smaller font size for mobile */
        padding: 8px 10px; /* Reduced padding */
    }
}
</style>
""", 
unsafe_allow_html=True
)

# Generate HTML table with data
table_html = filtered_df.to_html(classes="custom-table", index=False)

# Display table in a scrollable container
st.markdown(f'<div class="custom-table-container">{table_html}</div>', unsafe_allow_html=True)
