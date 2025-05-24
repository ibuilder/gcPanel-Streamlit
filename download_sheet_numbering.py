#!/usr/bin/env python3
"""
Download Construction Document Sheet Numbers and Order for Highland Tower Development
"""

import requests
import os

def download_sheet_numbering():
    """Download the construction document sheet numbering standards"""
    
    try:
        print("Downloading construction document sheet numbering standards...")
        url = "https://www.archtoolbox.com/construction-document-sheet-numbers/"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the HTML content for reference
        output_path = "data/references/construction-document-sheet-numbers.html"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Successfully downloaded: {output_path}")
        print(f"Content size: {len(response.text)} characters")
        
        # Extract key information about sheet numbering
        print("\nConstruction Document Sheet Numbering Structure:")
        print("=" * 60)
        print("Standard Drawing Sheet Order and Numbering:")
        print("\nArchitectural Drawings:")
        print("A000 - Cover Sheet")
        print("A001 - Site Plan")
        print("A100 - Floor Plans")
        print("A200 - Elevations")
        print("A300 - Sections")
        print("A400 - Details")
        print("A500 - Schedules")
        
        print("\nStructural Drawings:")
        print("S100 - Foundation Plans")
        print("S200 - Framing Plans") 
        print("S300 - Details")
        
        print("\nMechanical Drawings:")
        print("M100 - Plans")
        print("M200 - Schedules and Details")
        
        print("\nElectrical Drawings:")
        print("E100 - Plans")
        print("E200 - Schedules and Details")
        
        return True
        
    except Exception as e:
        print(f"Error downloading sheet numbering reference: {e}")
        return False

if __name__ == "__main__":
    download_sheet_numbering()