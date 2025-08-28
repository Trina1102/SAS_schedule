import streamlit as st
import pandas as pd

st.title("📊 Schedule Summary")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Read first sheet
    df = pd.read_excel(uploaded_file, sheet_name=0)

    # Use iloc to grab the correct columns (B, E, F, G, H)
    df = df.iloc[:, [1, 4, 5, 6, 7]]   # B=1, E=4, F=5, G=6, H=7
    df.columns = ["Store", "Category", "SectionSize", "Footage", "Hours"]

    # Remove unwanted categories
    df = df[~df["Category"].isin(["New Items", "Maintenance"])]

    output_lines = []
    for store, group in df.groupby("Store"):
        categories = [
            f"{row['Category']} {row['SectionSize']} {row['Footage']},"
            for _, row in group.iterrows()
        ]
        total_hours = group["Hours"].sum()
        line = f"{store}\t " + "".join(categories) + f" Total Hours - {total_hours +4}\t"
        output_lines.append(line)

    # Show results on the webpage
    st.subheader("Formatted Results")
    for line in output_lines:
        st.text(line)

    # Option to download as text file
    result_text = "\n".join(output_lines)
    st.download_button(
        label="📥 Download Results as TXT",
        data=result_text,
        file_name="sheet1_output.txt",
        mime="text/plain"
    )


