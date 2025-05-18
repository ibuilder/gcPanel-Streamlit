"""
PDF helper functions for the Documents module.

This module provides helper functions for rendering PDFs in the Documents module.
"""

import streamlit as st
from modules.pdf_viewer.pdf_viewer import PDFViewer

def display_pdf_document(file_path, document_name):
    """Display a PDF document with a title.
    
    Args:
        file_path: Path to the PDF file
        document_name: Name of the document to display as a header
    """
    st.subheader(document_name)
    PDFViewer.display_pdf(
        pdf_file=file_path,
        height=700
    )