import streamlit as st
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh
import requests

st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")

# File path to the Excel file
book_id = "1VmzWXUwhriK9VmPrJToqNxw7xaJbxChDl6LSWjNkLDc"
result_book_id = "1Xpto8UzUeUAE09rrtlXadcfpEgHgVv6HdguDV80Wwvk"
result_sheet_ids = [0]
youtube_book_id = "1UaOHKEVCJ8fMGx-wJxHWMY4inGtUNMjYSDEGfRXc9UA"
sheet_ids = [0]
# sheet_ids = [0,43261632,2106503987,1611940137,841538100,1472086766,68508585,1779814472,922711054,932744470,279159895,813667844,1087373046,450500849]
youtube_sheet_id = [0]
youtube_sheet_path = f"https://docs.google.com/spreadsheets/d/{youtube_book_id}/export?format=csv&gid={youtube_sheet_id[0]}"
youtube_df = pd.read_csv(youtube_sheet_path)
youtube_video_id = youtube_df["Link"][0]

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

# Function to load data from Excel (removed caching to allow reload on every run)
def load_result_data():
    dfs = pd.DataFrame()
    for sheet_id in result_sheet_ids:
        sheet_path = f"https://docs.google.com/spreadsheets/d/{result_book_id}/export?format=csv&gid={sheet_id}"

        # Read the sheet into a DataFrame
        df = pd.read_csv(sheet_path)
        
        # Check if the DataFrame is empty
        if not df.empty:
            dfs = pd.concat([dfs, df], ignore_index=True)
    # filtered_dfs = dfs[dfs['Status'].isin(['On-Stage', 'Next'])]        
    # del filtered_dfs['SI']

    return df

# Load data from the Excel file every time the app reruns
data = load_schedule_data()
result = load_result_data()

# Group by 'Zone' and sum 'Points'
zone_result = result.groupby('Zone')['Points'].sum().reset_index()

# Optionally, if you want to sort by the sum of Points
zone_result = zone_result.sort_values(by='Points', ascending=False)

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

github_storage = "https://raw.githubusercontent.com/amirul-dev/jeddah_sahithyolsavu_files/refs/heads/main/"

# Sidebar content
color_logo = github_storage+"color_logo.png"
new_logo = github_storage+"new_logo.png"
QR_code = github_storage+"QR2.png"

tab_titles = [
    "Schedule",
    "Individual Results",
    "Zone Results"
]

tabs = st.tabs(tab_titles)

with tabs[0]:

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
        </style>
        """, 
        unsafe_allow_html=True
        )

        # Generate HTML table with data
        table_html = filtered_df.to_html(classes="custom-table", index=False)

        # Display table
        st.markdown(table_html, unsafe_allow_html=True)
        
with tabs[1]:    
    colmain1selection, colmain2selection, _ = st.columns([1,1,1])  # Adjust the ratios as needed
    
    with colmain1selection:
        unique_programs = result["Program"].unique()
        selected_program = st.selectbox("Choose a Program:", options=["All"] + unique_programs.tolist())

        # Filter the DataFrame based on the selected stage
        if selected_program == "All":
            filtered_df = result
        else:
            filtered_df = result[result["Program"] == selected_program]
        
    with colmain2selection: 
        unique_categories = result["Category"].unique()
        selected_category = st.selectbox("Choose a category:", options=["All"] + unique_categories.tolist())

        # Filter the DataFrame based on the selected stage
        if selected_category == "All":
            filtered_df = filtered_df
        else:
            filtered_df = filtered_df[filtered_df["Category"] == selected_category]
    
    # Convert paths to <img> HTML tags in the last column
    def image_formatter(image_path):
        return f'<img src="{github_storage+image_path}" width="100" height="100" />'

    # Apply the image formatter to the last column (assuming the last column is named "Image Path")
    filtered_df.iloc[:, -1] = filtered_df.iloc[:, -1].apply(image_formatter)

    # Generate HTML table with updated last column containing images
    table_html = filtered_df.to_html(classes="custom-table", index=False, escape=False)

    # Display table
    st.markdown(table_html, unsafe_allow_html=True)

with tabs[2]:
    st.markdown(
    """
    <style>
    .custom-table-summary {
        border-collapse: collapse;
        width: 80%; /* Adjust table width to make it larger */
        margin: 20px auto; /* Center the table horizontally with margin */
        border-radius: 12px; /* Rounded corners for the table */
        overflow: hidden; /* Ensure rounded corners are respected */
        background-color: #2C3E50; /* Dark background color */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for a lifted effect */
    }
    .custom-table-summary th, .custom-table-summary td {
        border: 1px solid #34495E; /* Darker border color for grid */
        padding: 20px 25px; /* Larger padding for better spacing */
        text-align: center; /* Center align the content of the cells */
        color: white;
        font-size: 18px; /* Larger font size for better readability */
    }
    .custom-table-summary th {
        background-color: #1ABC9C; /* Vibrant header background */
        font-weight: bold;
        text-transform: uppercase; /* Uppercase headers */
    }
    .custom-table-summary td {
        background-color: #34495E; /* Slightly lighter background for cells */
    }
    .custom-table-summary tr:nth-child(even) td {
        background-color: #2C3E50; /* Alternating row colors for better readability */
    }
    .custom-table-summary tr:hover td {
        background-color: #16A085; /* Hover effect for rows */
        cursor: pointer;
    }
    </style>
    """, 
    unsafe_allow_html=True
    )
    
    
    _, resultcolumn, _ = st.columns([1,2,1])
    
    with resultcolumn:
        # Generate HTML table with updated last column containing images
        table_html = zone_result.to_html(classes="custom-table-summary", index=False, escape=False)

        # Display table
        st.markdown(table_html, unsafe_allow_html=True)




