# member1.py
import streamlit as st
import pdfplumber

def extract_resume_text(uploaded_file):
    """
    Extracts text from an uploaded PDF or TXT file in Streamlit.
    
    Args:
        uploaded_file: Uploaded file object from st.file_uploader
    
    Returns:
        str: Extracted text content
    """
    if uploaded_file is None:
        return ""
    
    # Get file extension
    file_name = uploaded_file.name.lower()
    
    try:
        if file_name.endswith('.pdf'):
            # Method 1: Using pdfplumber
            text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
            
        elif file_name.endswith('.txt'):
            # Read text file directly
            return uploaded_file.read().decode("utf-8").strip()
        
        else:
            st.error("Unsupported file type. Please upload a PDF or TXT file.")
            return ""
            
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return ""

# Example usage inside Streamlit
if __name__ == "__main__":
    st.title("📄 Resume Text Extractor")
    
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
    
    if uploaded_file:
        text = extract_resume_text(uploaded_file)
        if text:
            st.subheader("Extracted Text:")
            st.text_area("Content", text, height=300)
