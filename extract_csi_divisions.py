#!/usr/bin/env python3
"""
Extract CSI MasterFormat divisions from the downloaded PDF for Highland Tower Development
"""

import PyPDF2
import re

def extract_csi_divisions():
    """Extract CSI divisions from the downloaded PDF"""
    
    try:
        with open("data/documents/specifications/CSI-MasterFormat-Specification-Divisions.pdf", 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            print("Extracting CSI MasterFormat Divisions...")
            print("=" * 50)
            
            # Look for division patterns
            division_pattern = r'Division\s+(\d{2})\s*[-–]\s*(.+?)(?=\n|$)'
            divisions = re.findall(division_pattern, text, re.MULTILINE | re.IGNORECASE)
            
            if divisions:
                print("Found CSI Divisions:")
                for div_num, div_name in divisions:
                    print(f"Division {div_num}: {div_name.strip()}")
            else:
                # Try alternative patterns
                print("Searching for alternative division formats...")
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if 'division' in line.lower() and any(char.isdigit() for char in line):
                        print(f"Found: {line}")
            
            print("=" * 50)
            print(f"Total text extracted: {len(text)} characters")
            
            # Save extracted text for review
            with open("extracted_csi_text.txt", 'w') as f:
                f.write(text)
            print("Full text saved to: extracted_csi_text.txt")
            
    except Exception as e:
        print(f"Error extracting CSI divisions: {e}")
        
        # Provide standard CSI divisions as fallback
        print("\nUsing standard CSI MasterFormat divisions:")
        standard_divisions = {
            "00": "Procurement and Contracting Requirements",
            "01": "General Requirements",
            "02": "Existing Conditions",
            "03": "Concrete",
            "04": "Masonry",
            "05": "Metals",
            "06": "Wood, Plastics, and Composites",
            "07": "Thermal and Moisture Protection",
            "08": "Openings",
            "09": "Finishes",
            "10": "Specialties",
            "11": "Equipment",
            "12": "Furnishings",
            "13": "Special Construction",
            "14": "Conveying Equipment",
            "21": "Fire Suppression",
            "22": "Plumbing",
            "23": "Heating, Ventilating, and Air Conditioning (HVAC)",
            "25": "Integrated Automation",
            "26": "Electrical",
            "27": "Communications",
            "28": "Electronic Safety and Security",
            "31": "Earthwork",
            "32": "Exterior Improvements",
            "33": "Utilities",
            "34": "Transportation",
            "35": "Waterway and Marine Construction"
        }
        
        for div_num, div_name in standard_divisions.items():
            print(f"Division {div_num}: {div_name}")

if __name__ == "__main__":
    extract_csi_divisions()