import streamlit as st
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh
import requests

st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")

# Define CSS for background image
# Sidebar content
bg_url = f"https://raw.githubusercontent.com/amirul-dev/Jeddah_sahithyolsavu/refs/heads/main/Picture3.png"

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

# Custom CSS to set the sidebar background color
st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: rgb(8, 16, 38);
        color: white;  /* Change text color to white for better contrast */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content
image_url = f"https://raw.githubusercontent.com/amirul-dev/Jeddah_sahithyolsavu/refs/heads/main/download.png"
logo_url = f"https://raw.githubusercontent.com/amirul-dev/Jeddah_sahithyolsavu/refs/heads/main/sahithyolsavu logo.png"

st.sidebar.image(logo_url)  # Replace with your image path

video_url = "https://raw.githubusercontent.com/amirul-dev/Jeddah_sahithyolsavu/refs/heads/main/HIGHLIGHT%20VIDEO%20-%20SSF%20KAVIYOOR%20UNIT%20SAHITHYOLSAV%2023.mp4"

# Sidebar for the video with autoplay
st.sidebar.markdown(
    f"""
    <video style="width: 100%;" autoplay loop muted>
        <source src="{video_url}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    """,
    unsafe_allow_html=True
)

# st.sidebar.video(r"https://www.youtube.com/embed/SJr28k2EGd0?autoplay=1&mute=1")  # Replace with your image path

# Path to the local video file
# video_path = r"C:\Users\274913\Downloads\HIGHLIGHTS VIDEO .mp4"  # Replace with the actual path to your video file

# # HTML to embed the local video with autoplay
# video_html = f"""
# <video width="300" height="200" autoplay muted loop>
#     <source src="{video_path}" type="video/mp4">
#     Your browser does not support the video tag.
# </video>
# """

# Display the video in the sidebar
# st.sidebar.markdown(video_html, unsafe_allow_html=True)

######################### google drive video - no autoplay
# # Google Drive video ID
# file_id = "1E-YgWyiZyRsNGd5-GGNwsWu-AtRGiSLB"  # Replace with your actual Google Drive file ID
# # Create the viewer URL
# video_url = f"https://drive.google.com/file/d/{file_id}/preview"
# # HTML to embed the Google Drive video in the sidebar
# video_html = f"""
# <iframe width="300" height="200" src="{video_url}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
# """
# # Display the video in the sidebar
# st.sidebar.markdown(video_html, unsafe_allow_html=True)
#############################

############Youtube Video
video_id = "SJr28k2EGd0"  # Replace with your actual YouTube video ID
# Create the embed URL with parameters to minimize UI elements
video_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&controls=0&showinfo=0&modestbranding=1&rel=0&disablekb=1"
# HTML to embed the YouTube video in the sidebar
video_html = f"""
<iframe width="300" height="200" src="{video_url}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
"""
# Display the video in the sidebar
st.sidebar.markdown(video_html, unsafe_allow_html=True)
########################3

# Create two columns for the title and the image
col1, col2 = st.columns([2, 1])  # Adjust the ratios as needed

# Title of the app in the first column
with col1:
    st.title("Live Event Schedule")

# Display the image in the second column
with col2:
    st.image(image_url, width=200)

# File path to the Excel file
book_id = "1VmzWXUwhriK9VmPrJToqNxw7xaJbxChDl6LSWjNkLDc"
sheet_ids = [0]
# sheet_ids = [0,43261632,2106503987,1611940137,841538100,1472086766,68508585,1779814472,922711054,932744470,279159895,813667844,1087373046,450500849]


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

# CSS for white borders, gridlines, and 50% transparent cells
st.markdown(
    """
    <style>
    .custom-table {
        border-collapse: collapse;
        width: 100%;
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
table_html = data.to_html(classes="custom-table", index=False)

# Display table
st.markdown(table_html, unsafe_allow_html=True)


