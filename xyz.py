import streamlit as st
import os
import base64
from pathlib import Path
import tempfile
import streamlit.components.v1 as components

def main():
    st.set_page_config(page_title="PDF Bill Viewer", layout="wide")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.info("Use this sidebar to navigate through the app.")
    
    # Refresh button
    if st.sidebar.button("Refresh PDF List"):
        st.rerun()
    
    st.title("PDF Bill Viewer")
    
    # Use a more cloud-friendly approach for file paths
    # For local development
    local_path = Path("c:/Users/visha/OneDrive/Desktop/abcpdf/bills")
    # For cloud deployment
    cloud_path = Path("./bills")
    
    # Try cloud path first, then local path
    if cloud_path.exists():
        bill_folder = cloud_path
    elif local_path.exists():
        bill_folder = local_path
    else:
        st.error("Bills folder not found. Please upload PDFs using the uploader below.")
        
        # Add file uploader as a fallback
        uploaded_files = st.file_uploader("Upload PDF bills", type="pdf", accept_multiple_files=True)
        if uploaded_files:
            # Create a temporary directory to store uploaded files
            temp_dir = Path(tempfile.mkdtemp())
            bill_folder = temp_dir
            
            # Save uploaded files to the temporary directory
            for uploaded_file in uploaded_files:
                temp_file_path = bill_folder / uploaded_file.name
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            st.success(f"Successfully uploaded {len(uploaded_files)} files.")
        else:
            return
    
    # Get all PDF files in the bills folder
    try:
        pdf_files = [f.name for f in bill_folder.iterdir() if f.is_file() and f.suffix.lower() == '.pdf']
    except Exception as e:
        st.error(f"An error occurred while accessing the folder: {e}")
        return
    
    if not pdf_files:
        st.warning("No PDF files found in the bills folder.")
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
        # Read PDF file
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        
        # Display PDF using st.download_button with a label that encourages viewing
        st.download_button(
            label="📄 View PDF",
            data=pdf_bytes,
            file_name=pdf_path.name,
            mime="application/pdf",
            key="view_pdf"
        )
        
        # Alternative display method using st.components.v1
        st.write("### PDF Preview")
        st.write("If the PDF doesn't display properly, use the View PDF button above.")
        
        # Using a different HTML approach that might work better with Chrome security
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_display = f"""
            <embed
                src="data:application/pdf;base64,{base64_pdf}"
                width="700"
                height="800"
                type="application/pdf"
            >
        """
        components.html(pdf_display, height=800)  # Fixed: using components.html instead of st.components.v1.html
        
        # Also provide a regular download button
        st.download_button(
            label="💾 Download PDF",
            data=pdf_bytes,
            file_name=pdf_path.name,
            mime="application/pdf",
            key="download_pdf"
        )
    except Exception as e:
        st.error(f"An error occurred while displaying the PDF: {e}")

if __name__ == "__main__":
    main()
