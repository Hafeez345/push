import streamlit as st
import pandas as pd
import re

# App title
st.set_page_config(page_title="AI Data Agent", layout="wide")
st.title("AI Agent for Intelligent Data Queries")
st.markdown("Upload your data or use the sample data. Type any question to get exact results!")

# Sample data
sample_data = {
    "Name": ["Bilal Khan", "Ali Raza", "Sara Ahmed"],
    "Salary": [5000, 7000, 6000],
    "Contact": ["03001234567", "03007654321", "03009876543"],
    "State": ["Karachi", "Lahore", "Islamabad"]
}
df = pd.DataFrame(sample_data)

# Optional upload
uploaded_file = st.file_uploader("Upload CSV/Excel to replace sample data", type=["csv","xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

# Data preview
st.subheader("Data Preview")
st.dataframe(df)

# Question input
query = st.text_input("Type your question (e.g., 'salary of Bilal Khan'):")

if query:
    st.subheader("AI Agent Answer")

    # Normalize query
    query_clean = re.sub(r'[^\w\s]', '', query.lower())
    words = query_clean.split()
    results = pd.DataFrame()

    # --- Check if any column is mentioned in query ---
    matched_cols = [col for col in df.columns if col.lower() in query_clean]

    if matched_cols:
        col = matched_cols[0]  # pick the first matching column
        # Find row(s) where other words match (excluding column name)
        filter_words = [w for w in words if w not in col.lower()]
        filtered_rows = df[df.apply(lambda row: all(w in str(row['Name']).lower() for w in filter_words), axis=1)]
        if not filtered_rows.empty:
            # Return only the requested column values
            results = filtered_rows[[col]]

    # --- If no column matched, search full row ---
    if results.empty:
        mask = df.apply(lambda row: any(w in str(v).lower() for v in row for w in words), axis=1)
        results = df[mask]

    # Display results
    if not results.empty:
        st.write(results)
    else:
        st.write("No matching data found. Try a different query!")