# utils/data_processing.py

import pandas as pd
import streamlit as st

def display_table(data):
    df = pd.DataFrame(data)
    st.dataframe(df)

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
