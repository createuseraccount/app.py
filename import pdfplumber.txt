import pdfplumber
import pandas as pd
import streamlit as st

def extract_data_from_pdf(pdf_path):
    """Extract text or table data from the PDF file."""
    transactions = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split("\n"):
                    # Adjust this part based on your statement's format
                    if is_transaction_line(line):
                        transactions.append(parse_transaction(line))
    return transactions

def is_transaction_line(line):
    """Identify if a line contains transaction data. Adjust based on PDF structure."""
    import re
    # Example: Look for lines with a specific pattern (date, description, amount)
    return bool(re.match(r"\d{2}/\d{2}/\d{4}.*\d+\.\d{2}$", line))

def parse_transaction(line):
    """Parse a line of transaction data into a structured format."""
    # Example: Split into date, description, and amount
    parts = line.split()
    date = parts[0]
    amount = parts[-1]
    description = " ".join(parts[1:-1])
    return {"Date": date, "Description": description, "Amount": amount}

def export_to_excel(transactions):
    """Export the extracted transactions to an Excel file."""
    df = pd.DataFrame(transactions)
    return df.to_excel(index=False, engine="openpyxl")

def main():
    st.title("Credit Card Statement Parser")

    uploaded_file = st.file_uploader("Upload your credit card statement (PDF)", type="pdf")

    if uploaded_file is not None:
        st.write("Extracting data from PDF...")
        transactions = extract_data_from_pdf(uploaded_file)

        if not transactions:
            st.error("No transactions found in the PDF.")
        else:
            df = pd.DataFrame(transactions)
            st.dataframe(df)

            excel_file = export_to_excel(transactions)

            st.download_button(
                label="Download Excel File",
                data=excel_file,
                file_name="transactions.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()
