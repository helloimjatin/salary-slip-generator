import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

# Function to generate professional salary slip PDF
def generate_salary_slip(row):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)  # Prevent auto page breaks
    pdf.add_page()

    # College Name & Address
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "XYZ COLLEGE, India", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "123, College Road, City, State, India - 123456", ln=True, align="C")
    pdf.cell(0, 8, "Phone: +91-1234567890 | Email: info@xyzcollege.edu", ln=True, align="C")

    # Salary Slip Title
    pdf.ln(5)
    pdf.set_font("Arial", "BU", 14)
    pdf.cell(0, 10, "Salary Slip", ln=True, align="C")

    # Employee Details
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.cell(100, 8, f"Professor Name : {row['Name']}", ln=False)
    pdf.cell(0, 8, f"Month : {row['Month']}", ln=True)
    pdf.cell(100, 8, f"Department     : {row['Department']}", ln=True)

    # Salary Table
    pdf.ln(3)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 8, "Earnings", border=1, align="C")
    pdf.cell(0, 8, "Amount (INR)", border=1, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(100, 8, "Basic Salary", border=1)
    pdf.cell(0, 8, f"{row['Basic Salary']}", border=1, ln=True)
    pdf.cell(100, 8, "HRA", border=1)
    pdf.cell(0, 8, f"{row['HRA']}", border=1, ln=True)
    pdf.cell(100, 8, "Other Allowance", border=1)
    pdf.cell(0, 8, f"{row['Other Allowance']}", border=1, ln=True)
    pdf.cell(100, 8, "Gross Salary", border=1)
    pdf.cell(0, 8, f"{row['Gross Salary']}", border=1, ln=True)
    pdf.cell(100, 8, "Deductions", border=1)
    pdf.cell(0, 8, f"{row['Deductions']}", border=1, ln=True)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 8, "Net Salary", border=1)
    pdf.cell(0, 8, f"{row['Net Salary']}", border=1, ln=True)

    # Signatures
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(90, 8, "Authorized Signatory", align="L")
    pdf.cell(0, 8, "Employee Signature", align="R", ln=True)

    # Footer (carefully placed)
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "XYZ College | Confidential Document", align="C")

    # Save PDF to BytesIO
    pdf_data = pdf.output(dest='S').encode('latin1')
    buffer = io.BytesIO(pdf_data)
    return buffer


# Streamlit App
st.title("📑 Professional Salary Slip Generator")
st.write("Upload an Excel file containing professor salary details to generate professional salary slips.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Excel file loaded successfully!")
        st.dataframe(df)

        st.write("### 📥 Download Salary Slips:")
        for index, row in df.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{row['Name']} ({row['Department']})**")
            with col2:
                pdf_buffer = generate_salary_slip(row)
                st.download_button(
                    label="Download PDF",
                    data=pdf_buffer,
                    file_name=f"{row['Name'].replace(' ', '_')}_salary_slip.pdf",
                    mime="application/pdf"
                )
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
