#!/usr/bin/env python3
"""
Download construction project delivery methods for Highland Tower Development
"""

import requests
import os

def download_project_delivery_methods():
    """Download the construction project delivery methods reference"""
    
    try:
        print("Downloading construction project delivery methods...")
        url = "https://www.archtoolbox.com/construction-project-delivery-methods/"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the HTML content for reference
        output_path = "data/references/construction-project-delivery-methods.html"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Successfully downloaded: {output_path}")
        print(f"Content size: {len(response.text)} characters")
        
        # Extract key project delivery methods
        print("\nConstruction Project Delivery Methods:")
        print("=" * 60)
        print("1. Design-Bid-Build (Traditional)")
        print("2. Design-Build (D-B)")
        print("3. Construction Manager at Risk (CMAR)")
        print("4. Construction Manager as Advisor (CMA)")
        print("5. Integrated Project Delivery (IPD)")
        print("6. Public-Private Partnership (P3)")
        print("7. Build-Operate-Transfer (BOT)")
        
        return True
        
    except Exception as e:
        print(f"Error downloading project delivery methods reference: {e}")
        return False

if __name__ == "__main__":
    download_project_delivery_methods()