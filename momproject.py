import streamlit as st
import pandas as pd
import io

st.title("📊 Schedule Summary")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Read first sheet
    df = pd.read_excel(uploaded_file, sheet_name=0)

    # Use iloc to grab the correct columns (B, E, F, G, H)
    df = df.iloc[:, [1, 4, 5, 6, 7]]   # B=1, E=4, F=5, G=6, H=7
    df.columns = ["Store", "Category", "SectionSize", "Footage", "Hours"]

    # Filtered out rows for display
    filtered_group = group[~group["Category"].isin(["New Items", "Maintenance"])]

    output_lines = []
    results_for_excel = []
    for store, group in df.groupby("Store"):
        # Categories to display
        categories = [
        f"{row['Category']} {row['SectionSize']} {row['Footage']} ft,"
        for _, row in filtered_group.iterrows()
        ]
        total_hours = group["Hours"].sum()
        line = f"{store}\t " + " ".join(categories) + f" Total Hours - {total_hours}\t"
        output_lines.append(line)
        
        # Build one row per store for Excel
        results_for_excel.append({
            "Store": store,
            "Summary": " ".join(categories) + f" | Total Hours - {total_hours}"
        })

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
    # Create DataFrame for Excel
    results_df = pd.DataFrame(results_for_excel)
    
    # Download as Excel file
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        results_df.to_excel(writer, index=False, sheet_name="Summary")

    st.download_button(
        label="📥 Download Results as Excel",
        data=excel_buffer.getvalue(),
        file_name="sheet1_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )








