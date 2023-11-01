import streamlit as st
import pandas as pd

# Load the Excel file
file_path = "rqt1.xlsx"
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.error(f"File not found: {file_path}")
    st.stop()

# Title of the application
st.title("Query Application")

# Query Search
st.header("Query Search")

# Search input
search_term = st.text_input("Search for a keyword:")

# Filter data based on the keyword
filtered_df = df[df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]

# Display search results
st.dataframe(filtered_df)

# Add a new query
st.header("Add a New Query")

# Input for query information
new_id = st.text_input("Query ID")
new_domaine = st.selectbox("Query Domain", ["risk", "finance", "accounting", "human resources"])
new_script = st.text_area("Query Script")

# Button to add the new query
if st.button("Add Query"):
    if new_id and new_domaine and new_script:
        new_data = {
            "Id_rqt": new_id,
            "Domaine": new_domaine,
            "Script_requete": new_script,
            "Date": pd.to_datetime("now")
        }
        df = df._append(new_data, ignore_index=True)
        df.to_excel(file_path, index=False)
        st.success("Query added successfully.")

# Display the DataFrame
st.write(df)

# Advanced Data Search
st.header("Advanced Data Search")

# Option for advanced criteria
search_criteria = st.selectbox("Search by criteria:", ["Id_rqt", "Domaine", "Script_requete"])

# Search input for advanced criteria
advanced_search_term = st.text_input(f"Search by {search_criteria}:")

# Filter data based on advanced criteria
if search_criteria == "Id_rqt":
    advanced_filtered_df = df[df["Id_rqt"].str.lower().str.contains(advanced_search_term.lower())]
elif search_criteria == "Domaine":
    advanced_filtered_df = df[df["Domaine"].str.lower().str.contains(advanced_search_term.lower())]
elif search_criteria == "Script_requete":
    advanced_filtered_df = df[df["Script_requete"].str.lower().str.contains(advanced_search_term.lower())]

# Display advanced search results
st.dataframe(advanced_filtered_df)

# Delete Data Option
st.header("Delete Data")

# Multiselect for selecting rows to delete
selected_rows = st.multiselect("Select rows to delete", advanced_filtered_df.index)

# Button to delete selected rows
if st.button("Delete Selected Rows"):
    if selected_rows:
        df = df.drop(selected_rows)
        df.to_excel(file_path, index=False)
        st.success("Selected rows deleted successfully.")

# Display the updated DataFrame
st.write(df)
