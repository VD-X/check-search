import streamlit as st
import os
import base64
from pathlib import Path

def main():
    st.set_page_config(page_title="PDF Bill Viewer", layout="wide")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.info("Use this sidebar to navigate through the app.")
    
    # Refresh button
    if st.sidebar.button("Refresh PDF List"):
        st.rerun()  # Changed from st.experimental_user()
    
    st.title("PDF Bill Viewer")
    
    # Path to the bills folder
    bill_folder = Path("c:/Users/visha/OneDrive/Desktop/abcpdf/bills")
    
    # Check if the folder exists
    if not bill_folder.exists():
        st.error(f"Error: The folder {bill_folder} does not exist.")
        st.info("Please create a folder named 'bills' in your project directory and add PDF files to it.")
        return
    
    # Get all PDF files in the bills folder
    try:
        pdf_files = [f.name for f in bill_folder.iterdir() if f.is_file() and f.suffix.lower() == '.pdf']
    except Exception as e:
        st.error(f"An error occurred while accessing the folder: {e}")
        return
    
    if not pdf_files:
        st.warning("No PDF files found in the bills folder.")
        st.info("Please add some PDF files to the bills folder.")
        return
    
    # Create a dropdown to select a PDF file
    selected_pdf = st.selectbox("Select a bill to view:", pdf_files)
    
    if selected_pdf:
        pdf_path = bill_folder / selected_pdf
        
        # Display PDF file
        display_pdf(pdf_path)

def display_pdf(pdf_path):
    """Display the PDF file in the Streamlit app."""
    try:
        # Opening the file and encoding to base64
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        # Embedding PDF in HTML
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
        
        # Displaying the PDF
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        # Also provide a download button
        with open(pdf_path, "rb") as file:
            btn = st.download_button(
                label="Download PDF",
                data=file,
                file_name=pdf_path.name,
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"An error occurred while displaying the PDF: {e}")

if __name__ == "__main__":
    main()