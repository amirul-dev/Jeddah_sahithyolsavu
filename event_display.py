import streamlit as st
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh
import requests

st_autorefresh(interval=0.5 * 60 * 5000, key="dataframerefresh")

# Sidebar content

image_id = "1AP_j7U74DbnHo0ji38OkjZzfEPFCpb0f"
image_url = f"https://drive.google.com/uc?export=view&id={image_id}"
image = requests.get(image_url)

st.sidebar.image(image.content)  # Replace with your image path
# st.sidebar.video(r"https://www.youtube.com/embed/SJr28k2EGd0?autoplay=1&mute=1")  # Replace with your image path

# Path to the local video file
video_path = r"C:\Users\274913\Downloads\HIGHLIGHTS VIDEO .mp4"  # Replace with the actual path to your video file

# HTML to embed the local video with autoplay
video_html = f"""
<video width="300" height="200" autoplay muted loop>
    <source src="{video_path}" type="video/mp4">
    Your browser does not support the video tag.
</video>
"""

# Display the video in the sidebar
st.sidebar.markdown(video_html, unsafe_allow_html=True)

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

#############Youtube Video
# video_id = "SJr28k2EGd0"  # Replace with your actual YouTube video ID
# # Create the embed URL with parameters to minimize UI elements
# video_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&controls=0&showinfo=0&modestbranding=1&rel=0&disablekb=1"
# # HTML to embed the YouTube video in the sidebar
# video_html = f"""
# <iframe width="300" height="200" src="{video_url}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
# """
# # Display the video in the sidebar
# st.sidebar.markdown(video_html, unsafe_allow_html=True)
#########################3

# Title of the app
st.title("Live Event Schedule")

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

# Display the event schedule in a table (without scrolls and full width)
st.table(data.reset_index(drop=True).to_dict(orient='records'))


