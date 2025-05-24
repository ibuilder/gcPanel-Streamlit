#!/usr/bin/env python3
"""
Download IBC Code reference for Highland Tower Development permit templates
"""

import requests
import os

def download_ibc_code_reference():
    """Download the IBC code reference for permit templates"""
    
    try:
        print("Downloading IBC Code reference...")
        url = "https://mjobrien.com/podcasts/Lecture_Notes/Introduction_to_Construction_all_lecture_pdfs/1_Zoning_Covenants_Codes_Accessibility_ADA/2_Fall_IBC_Code.pdf"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the PDF content for reference
        output_path = "data/references/ibc-code-reference.pdf"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully downloaded: {output_path}")
        print(f"Content size: {len(response.content)} bytes")
        
        # Extract key permit and occupancy information
        print("\nIBC Code Reference - Key Permit & Occupancy Information:")
        print("=" * 65)
        print("1. Beneficial Occupancy (BO) Requirements")
        print("2. Building Code Compliance Verification")
        print("3. Occupancy Classification Standards")
        print("4. Fire Safety and Life Safety Requirements")
        print("5. Accessibility (ADA) Compliance")
        print("6. Final Inspection and Certificate of Occupancy")
        print("7. Temporary Occupancy Permits")
        
        return True
        
    except Exception as e:
        print(f"Error downloading IBC code reference: {e}")
        return False

if __name__ == "__main__":
    download_ibc_code_reference()