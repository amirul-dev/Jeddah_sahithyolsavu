import streamlit as st
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh
import requests

st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")

# File path to the Excel file
book_id = "1VmzWXUwhriK9VmPrJToqNxw7xaJbxChDl6LSWjNkLDc"
youtube_book_id = "1UaOHKEVCJ8fMGx-wJxHWMY4inGtUNMjYSDEGfRXc9UA"
sheet_ids = [0]
# sheet_ids = [0,43261632,2106503987,1611940137,841538100,1472086766,68508585,1779814472,922711054,932744470,279159895,813667844,1087373046,450500849]
youtube_sheet_id = [0]
youtube_sheet_path = f"https://docs.google.com/spreadsheets/d/{youtube_book_id}/export?format=csv&gid={youtube_sheet_id[0]}"
youtube_df = pd.read_csv(youtube_sheet_path)
youtube_video_id = youtube_df["Link"][0]

# Function to load data from Excel (removed caching to allow reload on every run)
def load_data():
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
data = load_data()

# Define CSS for background image
# Sidebar content
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

# Sidebar content
color_logo = f"https://raw.githubusercontent.com/amirul-dev/jeddah_sahithyolsavu_files/refs/heads/main/color_logo.png"
new_logo = f"https://raw.githubusercontent.com/amirul-dev/jeddah_sahithyolsavu_files/refs/heads/main/new_logo.png"
QR_code = f"https://raw.githubusercontent.com/amirul-dev/Jeddah_sahithyolsavu/refs/heads/main/QR2.png"

# Create two columns for the title and the image
colmain1, colmain2 = st.columns([1,2])  # Adjust the ratios as needed

with colmain1:
    st.image(color_logo, width=200)
    ############Youtube Video
    # Create the embed URL with parameters to minimize UI elements
    video_url = f"https://www.youtube.com/embed/{youtube_video_id}?autoplay=1&mute=1&controls=0&showinfo=0&modestbranding=1&rel=0&disablekb=1"
    # HTML to embed the YouTube video in the sidebar
    video_html = f"""
    <iframe width="100%" height="300" src="{video_url}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    """
    # Display the video in the sidebar
    st.markdown(video_html, unsafe_allow_html=True)
    ########################3 
    
    # Center the "Scan Me" title
    st.markdown("<h1 style='text-align: center;'>Scan Me</h1>", unsafe_allow_html=True)
    
    # Center the QR code image with 50% of the column width
    qr_html = f"""
    <div style="display: flex; justify-content: center;">
        <img src="{QR_code}" style="width: 50%; max-width: 300px;">
    </div>
    """
    st.markdown(qr_html, unsafe_allow_html=True)
        
    

with colmain2:
    # Title of the app in the first column
    st.title("Live Event Schedule")
        
    unique_stages = data["Stage"].unique()
    selected_stage = st.sidebar.selectbox("Choose a stage:", options=["All"] + unique_stages.tolist())

    # Filter the DataFrame based on the selected stage
    if selected_stage == "All":
        filtered_df = data
    else:
        filtered_df = data[data["Stage"] == selected_stage]

    # CSS for white borders, gridlines, and 50% transparent cells
    st.markdown(
        """
        <style>
        .custom-table {
            border-collapse: collapse;
            width: 100%; /* Make table take the full width */
            margin: 0; /* Remove any default margin */
        }
        .custom-table th, .custom-table td {
            border: 1px solid white;
            padding: 8px;
            text-align: left;
            color: white;
        }
        .custom-table th {
            background-color: rgba(51, 51, 51, 0.25); /* 50% transparent header */
        }
        .custom-table td {
            background-color: rgba(68, 68, 68, 0.25); /* 50% transparent cells */
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Generate HTML table with data
    table_html = filtered_df.to_html(classes="custom-table", index=False)

    # Display table
    st.markdown(table_html, unsafe_allow_html=True)


