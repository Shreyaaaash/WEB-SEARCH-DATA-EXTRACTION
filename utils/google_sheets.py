import io
import pandas as pd
import requests
import streamlit as st
def load_public_google_sheet(sheet_url):
    try:
        csv_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
        
        response = requests.get(csv_url)
        
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text), 
                             error_bad_lines=False,  
                             on_bad_lines='skip',    
                             engine='python')        
            return df
        else:
            st.error(f"Failed to load Google Sheet. HTTP Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"An error occurred while accessing the Google Sheet: {e}")
        return None