"""
PDF viewer module for the gcPanel Construction Management Dashboard.

This module provides PDF viewing capabilities using PDF.js.
"""

import streamlit as st
import base64
from typing import Optional, Dict, Any, List, Callable
import os
import uuid
import pandas as pd
from datetime import datetime, timedelta
import random

class PDFViewer:
    """PDF viewer component using PDF.js."""
    
    @staticmethod
    def display_pdf(
        pdf_file: Optional[str] = None,
        pdf_bytes: Optional[bytes] = None,
        height: int = 600,
        width: str = "100%",
        enable_annotation: bool = False,
        viewer_id: Optional[str] = None
    ) -> None:
        """
        Display a PDF file using PDF.js.
        
        Args:
            pdf_file: Path to the PDF file (alternative to pdf_bytes)
            pdf_bytes: PDF file content as bytes (alternative to pdf_file)
            height: Height of the viewer in pixels
            width: Width of the viewer (CSS value)
            enable_annotation: Whether to enable annotation tools
            viewer_id: Optional unique ID for the viewer
        """
        if not pdf_file and not pdf_bytes:
            st.error("Either pdf_file or pdf_bytes must be provided.")
            return
        
        # Generate a unique ID for the viewer if not provided
        if viewer_id is None:
            viewer_id = f"pdf_viewer_{uuid.uuid4().hex[:8]}"
        
        # Load PDF data
        if pdf_file:
            if os.path.exists(pdf_file):
                with open(pdf_file, "rb") as f:
                    pdf_data = f.read()
            else:
                st.error(f"PDF file not found: {pdf_file}")
                return
        else:
            pdf_data = pdf_bytes
        
        # Base64 encode the PDF data
        pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
        
        # Create the PDF.js viewer HTML
        pdf_viewer_html = f"""
        <div id="{viewer_id}" style="width: {width}; height: {height}px; border: 1px solid #dee2e6; border-radius: 5px; overflow: hidden;">
            <iframe 
                src="https://mozilla.github.io/pdf.js/web/viewer.html?file=data:application/pdf;base64,{pdf_base64}#zoom=page-fit"
                width="100%" 
                height="100%" 
                style="border: none;">
            </iframe>
        </div>
        """
        
        # Display the PDF viewer
        st.components.v1.html(pdf_viewer_html, height=height)
    
    @staticmethod
    def advanced_pdf_viewer(
        pdf_file: Optional[str] = None,
        pdf_bytes: Optional[bytes] = None,
        height: int = 700,
        width: str = "100%",
        enable_annotation: bool = True,
        enable_signature: bool = True,
        on_annotation_save: Optional[callable] = None,
        viewer_id: Optional[str] = None
    ) -> None:
        """
        Display an advanced PDF viewer with annotation capabilities.
        
        Args:
            pdf_file: Path to the PDF file (alternative to pdf_bytes)
            pdf_bytes: PDF file content as bytes (alternative to pdf_file)
            height: Height of the viewer in pixels
            width: Width of the viewer (CSS value)
            enable_annotation: Whether to enable annotation tools
            enable_signature: Whether to enable signature tools
            on_annotation_save: Callback when annotations are saved
            viewer_id: Optional unique ID for the viewer
        """
        if not pdf_file and not pdf_bytes:
            st.error("Either pdf_file or pdf_bytes must be provided.")
            return
        
        # Generate a unique ID for the viewer if not provided
        if viewer_id is None:
            viewer_id = f"pdf_advanced_viewer_{uuid.uuid4().hex[:8]}"
        
        # Load PDF data
        if pdf_file:
            if os.path.exists(pdf_file):
                with open(pdf_file, "rb") as f:
                    pdf_data = f.read()
                file_name = os.path.basename(pdf_file)
            else:
                st.error(f"PDF file not found: {pdf_file}")
                return
        else:
            pdf_data = pdf_bytes
            file_name = "document.pdf"
        
        # Base64 encode the PDF data
        pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
        
        # Create toolbar options based on settings
        toolbar_options = """
            <div class="toolbar">
                <div class="toolbar-item">
                    <select id="scale-select">
                        <option value="auto">Auto Zoom</option>
                        <option value="page-fit">Page Fit</option>
                        <option value="page-width">Page Width</option>
                        <option value="0.5">50%</option>
                        <option value="0.75">75%</option>
                        <option value="1">100%</option>
                        <option value="1.25">125%</option>
                        <option value="1.5">150%</option>
                        <option value="2">200%</option>
                    </select>
                </div>
                <div class="toolbar-item">
                    <button id="prev-page"><i class="material-icons">keyboard_arrow_left</i></button>
                    <span id="page-num"></span> / <span id="page-count"></span>
                    <button id="next-page"><i class="material-icons">keyboard_arrow_right</i></button>
                </div>
        """
        
        if enable_annotation:
            toolbar_options += """
                <div class="toolbar-item">
                    <button id="text-tool" title="Add Text"><i class="material-icons">text_fields</i></button>
                    <button id="highlight-tool" title="Highlight Text"><i class="material-icons">brush</i></button>
                    <button id="rectangle-tool" title="Draw Rectangle"><i class="material-icons">crop_square</i></button>
                    <button id="circle-tool" title="Draw Circle"><i class="material-icons">radio_button_unchecked</i></button>
                    <button id="arrow-tool" title="Draw Arrow"><i class="material-icons">arrow_forward</i></button>
                </div>
            """
        
        if enable_signature:
            toolbar_options += """
                <div class="toolbar-item">
                    <button id="signature-tool" title="Add Signature"><i class="material-icons">draw</i></button>
                </div>
            """
        
        toolbar_options += """
                <div class="toolbar-item toolbar-right">
                    <button id="save-annotations" title="Save Annotations"><i class="material-icons">save</i></button>
                    <button id="print-pdf" title="Print"><i class="material-icons">print</i></button>
                    <button id="download-pdf" title="Download"><i class="material-icons">download</i></button>
                </div>
            </div>
        """
        
        # Create the PDF viewer HTML
        pdf_viewer_html = f"""
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <style>
            .pdf-container {{
                width: {width};
                height: {height}px;
                display: flex;
                flex-direction: column;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                overflow: hidden;
            }}
            
            .toolbar {{
                display: flex;
                flex-wrap: wrap;
                padding: 8px;
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
            }}
            
            .toolbar-item {{
                margin-right: 15px;
                display: flex;
                align-items: center;
            }}
            
            .toolbar-right {{
                margin-left: auto;
                margin-right: 0;
            }}
            
            .toolbar button {{
                background: none;
                border: none;
                cursor: pointer;
                padding: 5px;
                margin: 0 2px;
                border-radius: 4px;
            }}
            
            .toolbar button:hover {{
                background-color: #e9ecef;
            }}
            
            .toolbar button.active {{
                background-color: #3e79f730;
                color: #3e79f7;
            }}
            
            .toolbar select {{
                padding: 5px 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
            }}
            
            .pdf-viewer {{
                flex-grow: 1;
                overflow: hidden;
            }}
            
            .annotation-layer {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                pointer-events: none;
            }}
            
            .annotation {{
                position: absolute;
                pointer-events: all;
            }}
            
            .signature-pad-container {{
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                z-index: 1000;
                display: none;
            }}
            
            #signature-pad {{
                border: 1px solid #ced4da;
                border-radius: 4px;
            }}
            
            .signature-buttons {{
                display: flex;
                justify-content: flex-end;
                margin-top: 10px;
            }}
            
            .signature-buttons button {{
                padding: 5px 10px;
                margin-left: 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            
            #clear-signature {{
                background-color: #f8f9fa;
                color: #212529;
            }}
            
            #apply-signature {{
                background-color: #3e79f7;
                color: white;
            }}
        </style>
        
        <div class="pdf-container" id="{viewer_id}_container">
            {toolbar_options}
            
            <div class="pdf-viewer" id="{viewer_id}">
                <iframe 
                    id="{viewer_id}_iframe"
                    src="https://mozilla.github.io/pdf.js/web/viewer.html?file=data:application/pdf;base64,{pdf_base64}#zoom=page-fit"
                    width="100%" 
                    height="100%" 
                    style="border: none;">
                </iframe>
            </div>
        </div>
        
        <!-- Signature pad (hidden by default) -->
        <div class="signature-pad-container" id="{viewer_id}_signature_container">
            <h3>Draw Signature</h3>
            <canvas id="{viewer_id}_signature_pad" width="400" height="200"></canvas>
            <div class="signature-buttons">
                <button id="{viewer_id}_clear_signature">Clear</button>
                <button id="{viewer_id}_apply_signature">Apply</button>
            </div>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.12.313/pdf.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/signature_pad/4.0.0/signature_pad.min.js"></script>
        <script>
            // Initialize viewer when the page loads
            document.addEventListener('DOMContentLoaded', function() {{
                // Basic viewer controls
                const scaleSelect = document.getElementById('scale-select');
                const prevPageButton = document.getElementById('prev-page');
                const nextPageButton = document.getElementById('next-page');
                const pageNum = document.getElementById('page-num');
                const pageCount = document.getElementById('page-count');
                const iframe = document.getElementById('{viewer_id}_iframe');
                const iframeWindow = iframe.contentWindow;
                
                // Get access to PDF.js viewer
                let PDFViewerApplication;
                
                iframe.onload = function() {{
                    PDFViewerApplication = iframeWindow.PDFViewerApplication;
                    
                    // Wait for the PDF to be loaded
                    PDFViewerApplication.initializedPromise.then(function() {{
                        // Update page count
                        PDFViewerApplication.pdfDocument.getPage(1).then(function() {{
                            const numPages = PDFViewerApplication.pagesCount;
                            pageCount.textContent = numPages;
                        }});
                        
                        // Subscribe to page change events
                        iframeWindow.addEventListener('pagechange', function(e) {{
                            pageNum.textContent = PDFViewerApplication.page;
                        }});
                        
                        // Initial page number
                        pageNum.textContent = PDFViewerApplication.page;
                    }});
                }};
                
                // Handle page navigation
                prevPageButton.addEventListener('click', function() {{
                    iframeWindow.PDFViewerApplication.eventBus.dispatch('previouspage');
                }});
                
                nextPageButton.addEventListener('click', function() {{
                    iframeWindow.PDFViewerApplication.eventBus.dispatch('nextpage');
                }});
                
                // Handle zoom changes
                scaleSelect.addEventListener('change', function() {{
                    iframeWindow.PDFViewerApplication.eventBus.dispatch('scalechanged', {{
                        value: scaleSelect.value
                    }});
                }});
                
                // Handle print button
                document.getElementById('print-pdf').addEventListener('click', function() {{
                    iframeWindow.PDFViewerApplication.eventBus.dispatch('print');
                }});
                
                // Handle download button
                document.getElementById('download-pdf').addEventListener('click', function() {{
                    iframeWindow.PDFViewerApplication.download();
                }});
                
                // Initialize signature pad if enabled
                if ({str(enable_signature).lower()}) {{
                    const signaturePadContainer = document.getElementById('{viewer_id}_signature_container');
                    const signaturePad = new SignaturePad(document.getElementById('{viewer_id}_signature_pad'));
                    
                    // Show signature pad
                    document.getElementById('signature-tool').addEventListener('click', function() {{
                        signaturePadContainer.style.display = 'block';
                    }});
                    
                    // Clear signature
                    document.getElementById('{viewer_id}_clear_signature').addEventListener('click', function() {{
                        signaturePad.clear();
                    }});
                    
                    // Apply signature
                    document.getElementById('{viewer_id}_apply_signature').addEventListener('click', function() {{
                        if (!signaturePad.isEmpty()) {{
                            const signatureImage = signaturePad.toDataURL();
                            
                            // Add signature to the PDF (in a real app, you would add it to the PDF)
                            // For this demo, we'll just notify that it was saved
                            signaturePadContainer.style.display = 'none';
                            
                            // Send to Streamlit that a signature was added
                            window.parent.postMessage({{
                                type: "streamlit:setComponentValue",
                                value: {{
                                    type: "signature",
                                    data: signatureImage,
                                    file: "{file_name}"
                                }}
                            }}, "*");
                        }}
                    }});
                }}
                
                // Handle save annotations button
                document.getElementById('save-annotations').addEventListener('click', function() {{
                    // In a real app, this would save annotations to the server
                    // For this demo, we'll just notify that annotations were saved
                    window.parent.postMessage({{
                        type: "streamlit:setComponentValue",
                        value: {{
                            type: "annotations_saved",
                            file: "{file_name}"
                        }}
                    }}, "*");
                }});
            }});
        </script>
        """
        
        # Display the PDF viewer
        st.components.v1.html(pdf_viewer_html, height=height + 50)  # Add some extra height for the toolbar

def generate_drawing_set(discipline, current_only=True):
    """
    Generate a sample set of construction drawings based on discipline.
    
    Args:
        discipline: Drawing discipline (Architectural, Structural, etc.)
        current_only: Whether to show only current drawings
        
    Returns:
        List of drawing dictionaries
    """
    drawing_data = []
    today = datetime.now()
    
    # Drawing types and counts by discipline
    discipline_info = {
        "Architectural": {
            "prefix": "A",
            "count": 30,
            "types": ["Floor Plans", "Elevations", "Sections", "Details", "Finishes"]
        },
        "Structural": {
            "prefix": "S", 
            "count": 25,
            "types": ["Foundation", "Framing Plans", "Sections", "Details", "Schedules"]
        },
        "MEP": {
            "prefix": "M", 
            "count": 35,
            "types": ["HVAC", "Plumbing", "Electrical", "Fire Protection"]
        },
        "Civil": {
            "prefix": "C", 
            "count": 15,
            "types": ["Site Plan", "Grading", "Utilities", "Details"]
        },
        "Landscape": {
            "prefix": "L", 
            "count": 10,
            "types": ["Layout", "Planting", "Irrigation", "Details"]
        }
    }
    
    # Get discipline data
    info = discipline_info.get(discipline, discipline_info["Architectural"])
    prefix = info["prefix"]
    count = info["count"]
    types = info["types"]
    
    # Generate drawings
    for i in range(1, count + 1):
        # Determine drawing type
        drawing_type = types[min(i // 5, len(types) - 1)]
        
        # Create drawing number with discipline prefix
        number = f"{prefix}{i:02d}"
        
        # Generate title based on number and type
        if i <= 5:
            title = f"General {drawing_type}"
        elif drawing_type == "Floor Plans" or drawing_type == "Framing Plans":
            floor = ((i - 5) % 20) + 1
            title = f"Level {floor} {drawing_type.rstrip('s')}"
        else:
            title = f"{drawing_type} {((i - 5) % 10) + 1}"
        
        # Create realistic revision history
        current_rev = random.randint(0, 4)
        
        # Only include superseded drawings if not filtering for current only
        if current_rev > 0 and not current_only:
            # Add previous revisions
            for rev in range(current_rev):
                rev_date = today - timedelta(days=random.randint(30, 365))
                drawing_data.append({
                    "number": number,
                    "title": title,
                    "discipline": discipline,
                    "type": drawing_type,
                    "revision": rev,
                    "date": rev_date.strftime("%Y-%m-%d"),
                    "status": "Superseded",
                    "size": random.choice(["ARCH D", "ARCH E"]),
                    "is_current": False
                })
        
        # Add current revision
        drawing_data.append({
            "number": number,
            "title": title,
            "discipline": discipline,
            "type": drawing_type,
            "revision": current_rev,
            "date": (today - timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d"),
            "status": random.choice(["Issued for Construction", "Issued for Bid", "Issued for Permit", "Issued for Review"]),
            "size": random.choice(["ARCH D", "ARCH E"]),
            "is_current": True
        })
    
    return drawing_data

def load_pdf_sample(sample_name: str = "contract") -> bytes:
    """
    Load a sample PDF file.
    
    Args:
        sample_name: Name of the sample PDF file
        
    Returns:
        PDF file content as bytes
    """
    # Generate a simple PDF with reportlab if the sample doesn't exist
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    if sample_name == "contract":
        # Create a sample contract
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "CONSTRUCTION CONTRACT AGREEMENT")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, "This Construction Contract Agreement (\"Agreement\") is entered into on")
        c.drawString(50, 705, "May 17, 2025, by and between:")
        
        c.drawString(50, 675, "OWNER:")
        c.drawString(100, 660, "Highland Properties LLC")
        c.drawString(100, 645, "123 Main Street")
        c.drawString(100, 630, "Metro City, State 12345")
        
        c.drawString(50, 600, "CONTRACTOR:")
        c.drawString(100, 585, "ABC Construction Company")
        c.drawString(100, 570, "456 Builder Avenue")
        c.drawString(100, 555, "Metro City, State 12345")
        
        c.drawString(50, 525, "PROJECT:")
        c.drawString(100, 510, "Highland Tower Development")
        c.drawString(100, 495, "1250 Highland Avenue")
        c.drawString(100, 480, "Metro City, State 12345")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 450, "1. SCOPE OF WORK")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 435, "The Contractor agrees to furnish all labor, materials, equipment, and services")
        c.drawString(50, 420, "necessary to complete the construction of a 15-story mixed-use commercial")
        c.drawString(50, 405, "building in accordance with the Contract Documents.")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 375, "2. CONTRACT SUM")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 360, "The Owner shall pay the Contractor the sum of $7,480,000.00 (Seven Million")
        c.drawString(50, 345, "Four Hundred Eighty Thousand Dollars) for the performance of the Contract.")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 315, "3. TIME OF COMPLETION")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 300, "The work to be performed under this Contract shall commence on January 5, 2025")
        c.drawString(50, 285, "and shall be substantially completed by December 15, 2025, subject to")
        c.drawString(50, 270, "adjustments as provided in the Contract Documents.")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 230, "SIGNATURE PAGE")
        
        c.drawString(50, 200, "OWNER:")
        c.drawString(50, 170, "_______________________________")
        c.drawString(50, 155, "Name: Patricia Miller")
        c.drawString(50, 140, "Title: Owner's Representative")
        c.drawString(50, 125, "Date: ___________________")
        
        c.drawString(300, 200, "CONTRACTOR:")
        c.drawString(300, 170, "_______________________________")
        c.drawString(300, 155, "Name: John Smith")
        c.drawString(300, 140, "Title: Project Manager")
        c.drawString(300, 125, "Date: ___________________")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, "Page 1 of 1")
        
    elif sample_name == "submittal":
        # Create a sample submittal
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "SUBMITTAL REVIEW FORM")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, "Project: Highland Tower Development")
        c.drawString(50, 700, "Submittal No: SUB-003")
        c.drawString(50, 680, "Date Submitted: March 15, 2025")
        
        c.drawString(50, 650, "Contractor: ABC Construction Company")
        c.drawString(50, 630, "Specification Section: 05 12 00 - Structural Steel Framing")
        c.drawString(50, 610, "Description: Structural Steel Shop Drawings")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 580, "REVIEW STATUS:")
        
        c.setFont("Helvetica", 12)
        c.drawString(70, 560, "[ ] Approved")
        c.drawString(70, 540, "[X] Approved with Comments")
        c.drawString(70, 520, "[ ] Revise and Resubmit")
        c.drawString(70, 500, "[ ] Rejected")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 470, "COMMENTS:")
        
        c.setFont("Helvetica", 12)
        c.drawString(70, 450, "1. Verify all connection details with structural calculations.")
        c.drawString(70, 430, "2. Coordinate steel beam elevations with MEP drawings.")
        c.drawString(70, 410, "3. Update details at column grid lines B-4 and D-7 per RFI-002 response.")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 370, "REVIEWED BY:")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 350, "Name: Steven Thompson")
        c.drawString(50, 330, "Title: Structural Engineer")
        c.drawString(50, 310, "Date: March 29, 2025")
        
        c.drawString(50, 270, "_______________________________")
        c.drawString(50, 250, "Signature")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, "Page 1 of 1")
        
    elif sample_name == "rfi":
        # Create a sample RFI
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "REQUEST FOR INFORMATION")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, "Project: Highland Tower Development")
        c.drawString(50, 700, "RFI No: RFI-002")
        c.drawString(50, 680, "Date Submitted: April 5, 2025")
        c.drawString(50, 660, "Response Required By: April 12, 2025")
        
        c.drawString(50, 630, "From: John Smith, ABC Construction Company")
        c.drawString(50, 610, "To: Steven Thompson, Thompson Engineering")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 580, "SUBJECT: Steel Connection Details")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 550, "Reference: Drawing S-501, Detail 3")
        c.drawString(50, 530, "Specification Section: 05 12 00 - Structural Steel Framing")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 500, "QUESTION:")
        
        c.setFont("Helvetica", 12)
        c.drawString(70, 480, "The connection detail shown on Drawing S-501, Detail 3 conflicts with the beam")
        c.drawString(70, 460, "size specified in the structural steel schedule. Please clarify the correct")
        c.drawString(70, 440, "connection detail for the W16x40 beam to HSS10x10x5/8 column connection")
        c.drawString(70, 420, "at grid lines B-4 and D-7.")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 390, "RESPONSE:")
        
        c.setFont("Helvetica", 12)
        c.drawString(70, 370, "Use modified connection detail per the attached sketch SK-001. The W16x40")
        c.drawString(70, 350, "beam shall be connected to the HSS column using 5/8\" thick end plates with")
        c.drawString(70, 330, "four (4) 3/4\" diameter A325 bolts in a rectangular pattern. Refer to the")
        c.drawString(70, 310, "attached calculation package for additional information.")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 270, "ANSWERED BY:")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 250, "Name: Steven Thompson")
        c.drawString(50, 230, "Title: Structural Engineer")
        c.drawString(50, 210, "Date: April 10, 2025")
        
        c.drawString(50, 170, "_______________________________")
        c.drawString(50, 150, "Signature")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, "Page 1 of 1")
    
    else:
        # Create a generic document
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "SAMPLE DOCUMENT")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, "This is a sample PDF document for the gcPanel Construction Management Dashboard.")
        c.drawString(50, 700, "Generated on: May 17, 2025")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, "Page 1 of 1")
    
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

def render_pdf_viewer():
    """Render the PDF viewer module."""
    st.title("Document Viewer")
    
    # Create tabs for different document types
    tabs = st.tabs(["Drawings", "Contracts", "Submittals", "RFIs", "Upload Document"])
    
    # Drawings tab
    with tabs[0]:
        st.header("Construction Drawings")
        
        # Create sections for different drawing types
        drawing_types = ["Architectural", "Structural", "MEP", "Civil", "Landscape"]
        drawing_col1, drawing_col2 = st.columns(2)
        
        with drawing_col1:
            selected_drawing_type = st.selectbox("Drawing Discipline", drawing_types)
        
        with drawing_col2:
            st.write(" ")
            st.write(" ")
            show_current_only = st.checkbox("Show current drawings only", value=True)
        
        # Generate sample drawing sets based on discipline
        # Creating the drawing data here to avoid function reference errors
        drawing_data = []
        today = datetime.now()
        
        # Drawing types and counts by discipline
        discipline_info = {
            "Architectural": {
                "prefix": "A",
                "count": 30,
                "types": ["Floor Plans", "Elevations", "Sections", "Details", "Finishes"]
            },
            "Structural": {
                "prefix": "S", 
                "count": 25,
                "types": ["Foundation", "Framing Plans", "Sections", "Details", "Schedules"]
            },
            "MEP": {
                "prefix": "M", 
                "count": 35,
                "types": ["HVAC", "Plumbing", "Electrical", "Fire Protection"]
            },
            "Civil": {
                "prefix": "C", 
                "count": 15,
                "types": ["Site Plan", "Grading", "Utilities", "Details"]
            },
            "Landscape": {
                "prefix": "L", 
                "count": 10,
                "types": ["Layout", "Planting", "Irrigation", "Details"]
            }
        }
        
        # Get discipline data
        discipline = selected_drawing_type
        info = discipline_info.get(discipline, discipline_info["Architectural"])
        prefix = info["prefix"]
        count = info["count"]
        types = info["types"]
        
        # Generate drawings
        for i in range(1, count + 1):
            # Determine drawing type
            drawing_type = types[min(i // 5, len(types) - 1)]
            
            # Create drawing number with discipline prefix
            number = f"{prefix}{i:02d}"
            
            # Generate title based on number and type
            if i <= 5:
                title = f"General {drawing_type}"
            elif drawing_type == "Floor Plans" or drawing_type == "Framing Plans":
                floor = ((i - 5) % 20) + 1
                title = f"Level {floor} {drawing_type.rstrip('s')}"
            else:
                title = f"{drawing_type} {((i - 5) % 10) + 1}"
            
            # Create realistic revision history
            current_rev = random.randint(0, 4)
            
            # Only include superseded drawings if not filtering for current only
            if current_rev > 0 and not show_current_only:
                # Add previous revisions
                for rev in range(current_rev):
                    rev_date = today - timedelta(days=random.randint(30, 365))
                    drawing_data.append({
                        "number": number,
                        "title": title,
                        "discipline": discipline,
                        "type": drawing_type,
                        "revision": rev,
                        "date": rev_date.strftime("%Y-%m-%d"),
                        "status": "Superseded",
                        "size": random.choice(["ARCH D", "ARCH E"]),
                        "is_current": False
                    })
            
            # Add current revision
            drawing_data.append({
                "number": number,
                "title": title,
                "discipline": discipline,
                "type": drawing_type,
                "revision": current_rev,
                "date": (today - timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d"),
                "status": random.choice(["Issued for Construction", "Issued for Bid", "Issued for Permit", "Issued for Review"]),
                "size": random.choice(["ARCH D", "ARCH E"]),
                "is_current": True
            })
        
        drawings = drawing_data
        
        # Display drawings in a table
        drawing_df = pd.DataFrame(drawings)
        
        # Style the dataframe
        if not drawing_df.empty:
            # Add view button column
            styled_df = drawing_df.copy()
            
            # Display the table
            st.dataframe(
                styled_df[["number", "title", "revision", "date", "status"]], 
                use_container_width=True,
                hide_index=True
            )
            
            # Display selected drawing
            selected_drawing = st.selectbox("Select Drawing to View", drawing_df["number"] + " - " + drawing_df["title"])
            if selected_drawing:
                selected_index = selected_drawing.split(" - ")[0]
                drawing_data = drawing_df[drawing_df["number"] == selected_index].iloc[0]
                
                st.markdown(f"### {selected_drawing} (Rev. {drawing_data['revision']})")
                st.markdown(f"**Status:** {drawing_data['status']} | **Date:** {drawing_data['date']} | **Sheet Size:** {drawing_data['size']}")
                
                drawing_pdf = load_pdf_sample("drawing")
                PDFViewer.advanced_pdf_viewer(pdf_bytes=drawing_pdf, enable_annotation=True)
    
    # Contracts tab
    with tabs[1]:
        st.header("Contract Documents")
        
        # Sample contract document
        if st.button("View Sample Contract", key="view_contract"):
            contract_pdf = load_pdf_sample("contract")
            st.markdown("### Construction Contract Agreement")
            PDFViewer.advanced_pdf_viewer(pdf_bytes=contract_pdf, enable_signature=True)
    
    # Submittals tab
    with tabs[1]:
        st.header("Submittal Documents")
        
        # Sample submittal document
        if st.button("View Sample Submittal", key="view_submittal"):
            submittal_pdf = load_pdf_sample("submittal")
            st.markdown("### Structural Steel Shop Drawings Submittal")
            PDFViewer.advanced_pdf_viewer(pdf_bytes=submittal_pdf)
    
    # RFIs tab
    with tabs[2]:
        st.header("RFI Documents")
        
        # Sample RFI document
        if st.button("View Sample RFI", key="view_rfi"):
            rfi_pdf = load_pdf_sample("rfi")
            st.markdown("### Steel Connection Details RFI")
            PDFViewer.advanced_pdf_viewer(pdf_bytes=rfi_pdf)
    
    # Upload tab
    with tabs[3]:
        st.header("Upload Document")
        
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            # Read the file
            pdf_bytes = uploaded_file.read()
            
            st.markdown(f"### {uploaded_file.name}")
            PDFViewer.advanced_pdf_viewer(pdf_bytes=pdf_bytes)