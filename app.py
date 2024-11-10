


#BESTEST UNTILL NOW

# import streamlit as st
# import pandas as pd
# import re
# from utils.search_api import search_entities
# from utils.llm_extraction import extract_info_from_text
# from utils.data_processing import display_table, save_to_csv
# from config import SERP_API_KEY, GROQ_API_KEY

# def main():
#     st.title("Automated Data Extraction Dashboard")

#     # File upload section
#     uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
#     if uploaded_file:
#         try:
#             df = pd.read_csv(uploaded_file)
#             st.write("CSV file loaded successfully!")
#             st.dataframe(df)
            
#             # Direct user query input
#             query = st.text_input("Enter your query (e.g., 'Get the latest phone of Samsung')")
            
#             # Column selection for entities
#             if not df.empty:
#                 selected_column = st.selectbox(
#                     "Select the column to process",
#                     df.columns.tolist()
#                 )
                
#                 # Extract potential entity from query by matching against the CSV column
#                 potential_entities = df[selected_column].values
#                 matched_entity = None
                
#                 for entity in potential_entities:
#                     # Using regex to search for whole words (case-insensitive)
#                     if re.search(rf'\b{re.escape(entity)}\b', query, re.IGNORECASE):
#                         matched_entity = entity
#                         break
                
#                 # If no entity found, display an error
#                 if not matched_entity:
#                     st.error("The entity specified in the query does not match any entry in the selected CSV column.")
#                     return
                
#                 # Replace the identified entity in the query with "PLACEHOLDER" for processing
#                 processed_query = re.sub(rf'\b{re.escape(matched_entity)}\b', 'PLACEHOLDER', query, flags=re.IGNORECASE)
                
#                 # Start extraction process
#                 if st.button("Start Extraction"):
#                     with st.spinner('Processing data...'):
#                         # Perform search and extraction
#                         search_results = search_entities(matched_entity, processed_query, SERP_API_KEY)
#                         extracted_info = extract_info_from_text(search_results, GROQ_API_KEY)
                        
#                         # Display and save results
#                         st.success("Extraction completed!")
#                         st.write("Extraction Results:")
#                         results = [{"entity": matched_entity, "extracted_info": extracted_info}]
#                         display_table(results)
                        
#                         # Save results
#                         output_filename = "extraction_results.csv"
#                         save_to_csv(results, output_filename)
                        
#                         # Create download button
#                         with open(output_filename, 'rb') as f:
#                             st.download_button(
#                                 label="Download Results as CSV",
#                                 data=f,
#                                 file_name=output_filename,
#                                 mime='text/csv'
#                             )
        
#         except Exception as e:
#             st.error(f"An error occurred while processing the file: {e}")
#     else:
#         st.info("Please upload a CSV file to begin the extraction process.")

# if __name__ == "__main__":
#     main()



import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import io
import re
import json
import streamlit as st
import pandas as pd
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils.search_api import search_entities
from utils.llm_extraction import extract_info_from_text
from utils.data_processing import display_table, save_to_csv
from config import SERP_API_KEY, GROQ_API_KEY


def authenticate_google_sheets(credentials_file_content):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    credentials_dict = json.loads(credentials_file_content)

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

    client = gspread.authorize(credentials)
    
    return client

def load_google_sheet(sheet_url, credentials_file_content):
    try:
        client = authenticate_google_sheets(credentials_file_content)
        sheet = client.open_by_url(sheet_url)
        
        # Fetch the first worksheet
        worksheet = sheet.get_worksheet(0)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"An error occurred while accessing the Google Sheet: {e}")
        return None

def main():
    st.title("Automated Data Extraction Dashboard")

    data_source_option = st.radio("Choose data source", ("Upload CSV file", "Connect Google Sheet"))
    df = None

    if data_source_option == "Upload CSV file":
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("CSV file loaded successfully!")
            st.dataframe(df.head())  

    elif data_source_option == "Connect Google Sheet":
        sheet_url = st.text_input("Enter Google Sheet URL")
        credentials_file = st.file_uploader("Upload Google Sheets API credentials JSON file", type=["json"])
        
        if sheet_url and credentials_file:
            try:
                credentials_file_content = credentials_file.getvalue().decode("utf-8")
                
                df = load_google_sheet(sheet_url, credentials_file_content)
                if df is not None:
                    st.write("Google Sheet loaded successfully!")
                    st.dataframe(df.head()) 
                
                    selected_column = st.selectbox("Select the column to process", df.columns.tolist())
                    st.info(f"Selected column for processing: {selected_column}")
            except Exception as e:
                st.error(f"An error occurred while processing the credentials file: {e}")
            
    if df is not None and not df.empty:
        selected_column = st.selectbox(
            "Select the column to process",
            df.columns.tolist()
        )
        
        available_entities = df[selected_column].unique()
        st.info(f"Please enter a query related to one of the following entities:\n{', '.join(available_entities)}")
        
        query = st.text_input("Enter your query (e.g., 'Get the latest phone of Samsung')")
        

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
                    extracted_info = extract_info_from_text(search_results, GROQ_API_KEY)
                    
                    st.success("Extraction completed!")
                    st.write("Extraction Results:")
                    results = [{"entity": matched_entity, "extracted_info": extracted_info}]
                    display_table(results)
                    
                    output_filename = "extraction_results.csv"
                    save_to_csv(results, output_filename)
                    
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

