import streamlit as st

import pandas as pd

# ---------------------------
# Page config (minimal UI)
# ---------------------------
st.set_page_config(
    page_title="DataCleaner",
    page_icon="🧹",
    layout="centered"
)

st.title("🧹 DataCleanr")
st.caption("Upload a CSV or Excel file and clean it in one click.")

# ---------------------------
# File Upload
# ---------------------------
uploaded_file = st.file_uploader(
    "Upload your file",
    type=["csv", "xlsx"]
)

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")


    st.subheader("🔍 Raw Data Preview")
    st.dataframe(df.head())

    st.divider()

    # ---------------------------
    # Cleaning Options
    # ---------------------------
    st.subheader("🧹 Cleaning Options")

    col1, col2 = st.columns(2)

    with col1:
        remove_dupes = st.checkbox("Remove duplicate rows")
        drop_na = st.checkbox("Remove missing values")

    with col2:
        standardize_cols = st.checkbox("Standardize column names")
        reset_index = st.checkbox("Reset index")

    # ---------------------------
    # Clean Button
    # ---------------------------
    if st.button("✨ Clean Data"):
        df_clean = df.copy()

        if remove_dupes:
            df_clean = df_clean.drop_duplicates()

        if drop_na:
            df_clean = df_clean.dropna()

        if standardize_cols:
            df_clean.columns = (
                df_clean.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_")
            )

        if reset_index:
            df_clean = df_clean.reset_index(drop=True)

        st.success("Data cleaned successfully!")

        st.subheader("✅ Cleaned Data Preview")
        st.dataframe(df_clean.head())

        # ---------------------------
        # Download
        # ---------------------------
        st.download_button(
            "⬇️ Download Cleaned CSV",
            df_clean.to_csv(index=False),
            "cleaned_data.csv",
            "text/csv"
        )

else:
    st.info("👆 Upload a file to get started.")
