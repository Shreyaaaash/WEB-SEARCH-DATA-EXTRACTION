import streamlit as st
import pandas as pd
import re
import requests
import io  # Import io for StringIO
from utils.search_api import search_entities
from utils.llm_extraction import extract_info_from_text
from utils.data_processing import display_table, save_to_csv
from config import SERP_API_KEY, GROQ_API_KEY
import tempfile 

def load_public_google_sheet(sheet_url):
    try:
        # Convert the Google Sheets URL to the export link for CSV format
        csv_url = convert_to_csv_url(sheet_url)
        
        response = requests.get(csv_url)
        
        if response.status_code == 200 and response.headers['Content-Type'] == 'text/csv':
            df = pd.read_csv(io.StringIO(response.text), 
                             on_bad_lines='skip',    
                             engine='python')        
            return df
        else:
            st.error("Failed to load Google Sheet. Ensure it is publicly accessible and check the URL.")
            return None
    except Exception as e:
        st.error(f"An error occurred while accessing the Google Sheet: {e}")
        return None

def convert_to_csv_url(sheet_url):
    """
    Convert a standard Google Sheets link to a CSV export link.
    """
    if "docs.google.com/spreadsheets/d/" in sheet_url:
        # Extract sheet ID from the URL
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        # Construct CSV export link
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        return csv_url
    else:
        raise ValueError("Invalid Google Sheets URL format.")

def main():
    st.title("Automated Data Extraction Dashboard")

    data_source_option = st.radio("Choose data source", ("Upload CSV file", "Connect Google Sheet"))
    df = None

    if data_source_option == "Upload CSV file":
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("CSV file loaded successfully!")
                st.dataframe(df)  
            except pd.errors.ParserError:
                st.error("Failed to parse CSV file. Please check the file format.")
            except Exception as e:
                st.error(f"An unexpected error occurred while loading the CSV file: {e}")
    elif data_source_option == "Connect Google Sheet":
        sheet_url = st.text_input("Enter Google Sheet URL (must be publicly accessible)")
        
        if sheet_url:
            df = load_public_google_sheet(sheet_url)
            if df is not None:
                st.write("Google Sheet loaded successfully!")
                st.dataframe(df)

    if df is not None and not df.empty:
        selected_column = st.selectbox("Select the column to process", df.columns.tolist())
        
        available_entities = df[selected_column].dropna().unique()
        
        if available_entities.size == 0:
            st.error("No valid entities found in the selected column.")
            return
        
        st.info(f"Please enter a query related to one of the following entities:\n{', '.join(available_entities)}")
        
        query = st.text_input("Enter your query (e.g., 'Get the email address of {company}')")
        
        matched_entity = None
        if query:

            for entity in available_entities:
                if re.search(rf'\b{re.escape(entity)}\b', query, re.IGNORECASE):
                    matched_entity = entity
                    break
            
            if not matched_entity:
                st.error("The entity specified in the query does not match any entry in the selected column.")
                return
            
            processed_query = re.sub(rf'\b{re.escape(matched_entity)}\b', 'PLACEHOLDER', query, flags=re.IGNORECASE)
            
            if st.button("Start Extraction"):
                with st.spinner('Processing data...'):
                    search_results = search_entities(matched_entity, processed_query, SERP_API_KEY)
                    
                    extracted_info = extract_info_from_text(search_results, GROQ_API_KEY)  # Adjusted call
                    
                    st.success("Extraction completed!")
                    st.write("Extraction Results:")
                    
                    results = [{"entity": matched_entity, "extracted_info": info} for info in extracted_info]
                    
                    results_display = ""
                    for result in results:
                        results_display += f"**Entity**: {result['entity']}\n"
                        results_display += f"**Extracted Info**:\n{result['extracted_info'].replace('\n', '<br>')}\n\n"  # Add double newlines for spacing
                    
                    st.markdown(results_display, unsafe_allow_html=True)

                    output_filename = "extraction_results.csv"
                    
                    df_results = pd.DataFrame(results)
                    df_results['extracted_info'] = df_results['extracted_info'].str.replace('\n', ' ', regex=False)  # Replace newlines with spaces for CSdf_resV

                    if 'df_results' not in st.session_state:
                            st.session_state['df_results'] = pd.DataFrame()  # Initialize with a default empty DataFrame or your data

                    # Access or modify df_results
                    df_results = st.session_state['df_results']
                    save_to_csv(df_results.to_dict(orient='records'), output_filename)  # Adjusted call
                    
                    
                    with open(output_filename, 'rb') as f:
                        st.download_button(
                            label="Download Results as CSV",
                            data=f,
                            file_name=output_filename,
                            mime='text/csv'
                        )
    else:
        st.info("Please upload a CSV file or connect to a Google Sheet to begin the extraction process.")

if __name__ == "__main__":
    main()