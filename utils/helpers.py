import streamlit as st
import pandas as pd
import io
import base64
from datetime import datetime
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def format_date(date_str):
    """Format a date string for display"""
    if not date_str:
        return ""
    
    try:
        date_obj = datetime.strptime(str(date_str), '%Y-%m-%d')
        return date_obj.strftime('%b %d, %Y')
    except Exception:
        return date_str

def format_currency(amount):
    """Format a number as currency"""
    if amount is None:
        return "$0.00"
    
    try:
        return "${:,.2f}".format(float(amount))
    except ValueError:
        return "$0.00"

def df_to_csv(df):
    """Convert DataFrame to CSV for download"""
    return df.to_csv(index=False).encode('utf-8')

def df_to_excel(df):
    """Convert DataFrame to Excel for download"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def create_download_link(file_content, file_name, link_text):
    """Create a download link for a file"""
    b64 = base64.b64encode(file_content).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">{link_text}</a>'
    return href

def generate_pdf_report(title, content, data_frame=None):
    """Generate a PDF report"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, title)
    
    # Add content
    c.setFont("Helvetica", 12)
    y_position = height - 100
    
    # Split content into lines
    for line in content.split('\n'):
        c.drawString(72, y_position, line)
        y_position -= 20
    
    # Add table if dataframe is provided
    if data_frame is not None:
        # Convert DataFrame to a list of lists
        data = [data_frame.columns.tolist()] + data_frame.values.tolist()
        
        # Calculate column widths
        col_widths = [100] * len(data[0])
        
        # Draw table header
        y_position -= 20
        c.setFont("Helvetica-Bold", 10)
        x_position = 72
        for i, col in enumerate(data[0]):
            c.drawString(x_position, y_position, str(col))
            x_position += col_widths[i]
        
        # Draw table rows
        c.setFont("Helvetica", 10)
        for row in data[1:]:
            y_position -= 20
            if y_position < 72:  # Check if we need a new page
                c.showPage()
                y_position = height - 72
            
            x_position = 72
            for i, cell in enumerate(row):
                c.drawString(x_position, y_position, str(cell))
                x_position += col_widths[i]
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer

def truncate_text(text, max_length=50):
    """Truncate text to a maximum length"""
    if text and len(text) > max_length:
        return text[:max_length-3] + "..."
    return text
