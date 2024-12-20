import streamlit as st
import pandas as pd

st.title("CSV File Uploader")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Add a button to submit and display data
if uploaded_file is not None:
    # Read the file name
    file_name = uploaded_file.name
    st.write(f"Uploaded file name: {file_name}")

    # Add a submit button
    if st.button("Submit"):
        # Read the CSV data into a pandas DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the data
        st.write("Data inside the file:")
        st.dataframe(df)
