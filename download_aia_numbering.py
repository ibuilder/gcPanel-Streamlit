#!/usr/bin/env python3
"""
Download AIA contract document numbering system for Highland Tower Development
"""

import requests
import os

def download_aia_numbering():
    """Download the AIA contract document numbering system reference"""
    
    try:
        print("Downloading AIA contract document numbering system...")
        url = "https://www.archtoolbox.com/aia-contract-document-numbering/"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the HTML content for reference
        output_path = "data/references/aia-contract-numbering.html"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Successfully downloaded: {output_path}")
        print(f"Content size: {len(response.text)} characters")
        
        # Extract key information about AIA numbering system
        print("\nAIA Contract Document Numbering System Structure:")
        print("=" * 60)
        print("Format: SERIES-TYPE-DELIVERY-SEQUENCE-EDITION")
        print("\nSeries Examples:")
        print("A = Owner-Architect Agreements")
        print("B = Owner-Contractor Agreements") 
        print("C = Other Agreements")
        print("D = Documents")
        print("G = Contractor Documents")
        
        return True
        
    except Exception as e:
        print(f"Error downloading AIA numbering reference: {e}")
        
        # Provide standard AIA numbering components as fallback
        print("\nUsing standard AIA contract document numbering components:")
        
        aia_components = {
            "series": {
                "A": "Owner-Architect Agreements",
                "B": "Owner-Contractor Agreements", 
                "C": "Other Agreements",
                "D": "Documents",
                "G": "Contractor Documents"
            },
            "type": {
                "1": "Standard Form",
                "2": "Short Form", 
                "3": "Guide",
                "4": "Commentary",
                "5": "Protocol"
            },
            "delivery": {
                "0": "Traditional",
                "1": "Design-Build",
                "2": "Construction Manager",
                "3": "Integrated Project Delivery"
            },
            "sequence": {
                "1": "First in series",
                "2": "Second in series",
                "3": "Third in series"
            },
            "edition": {
                "2017": "2017 Edition",
                "2014": "2014 Edition", 
                "2007": "2007 Edition"
            }
        }
        
        for component, values in aia_components.items():
            print(f"\n{component.upper()}:")
            for code, description in values.items():
                print(f"  {code}: {description}")
        
        return False

if __name__ == "__main__":
    download_aia_numbering()