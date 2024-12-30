import pdfplumber
import pandas as pd
import streamlit as st

def extract_data_from_pdf(pdf_path):
    """Extract text or table data from the PDF file."""
    transactions = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            st.write(f"Page {page_num} Text:")
            st.code(text)  # Display the text for debugging
            if text:
                for line in text.split("\n"):
                    if is_transaction_line(line):
                        transaction = parse_transaction(line)
                        if transaction:
                            transactions.append(transaction)
    return transactions

def is_transaction_line(line):
    """Identify if a line contains transaction data. Adjust based on PDF structure."""
    import re
    # Adjust regex to match ICICI credit card transaction lines (date pattern + amount)
    # Example: "02/12/2024 DESCRIPTION 1,234.56"
    return bool(re.match(r"\d{2}/\d{2}/\d{4}.*\d{1,3}(,\d{3})*(\.\d{2})?$", line))

def parse_transaction(line):
    """Parse a line of transaction data into a structured format."""
    import re
    try:
        # Split the line into date, description, and amount based on known format
        parts = re.split(r"\s{2,}", line)  # Split on multiple spaces (ICICI's format)
        date = parts[0]
        amount = parts[-1].replace(",", "")  # Remove commas from amount
        description = " ".join(parts[1:-1])  # Combine the middle parts as description
        return {"Date": date, "Description": description, "Amount": float(amount)}
    except (IndexError, ValueError):
        # Handle unexpected line formats gracefully
        return None

def export_to_excel(transactions):
    """Export the extracted transactions to an Excel file."""
    df = pd.DataFrame(transactions)
    output = pd.ExcelWriter("transactions.xlsx", engine="openpyxl")
    df.to_excel(output, index=False)
    output.seek(0)
    return output.getvalue()

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
