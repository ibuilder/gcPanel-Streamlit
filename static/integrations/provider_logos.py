"""
Provider logos for integration services.

This module contains SVG logos for integration services to be displayed
in the UI without embedding large chunks of HTML in Python code.
"""

def get_provider_logo(provider_id):
    """
    Get the logo SVG for a specific provider.
    
    Args:
        provider_id (str): The provider identifier
        
    Returns:
        str: SVG markup for the provider logo
    """
    logos = {
        "procore": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 24C18.6274 24 24 18.6274 24 12C24 5.37258 18.6274 0 12 0C5.37258 0 0 5.37258 0 12C0 18.6274 5.37258 24 12 24Z" fill="#F3751D"/>
            <path d="M12 5.5C8.41015 5.5 5.5 8.41015 5.5 12C5.5 15.5899 8.41015 18.5 12 18.5C15.5899 18.5 18.5 15.5899 18.5 12C18.5 8.41015 15.5899 5.5 12 5.5ZM12 15.5C10.067 15.5 8.5 13.933 8.5 12C8.5 10.067 10.067 8.5 12 8.5C13.933 8.5 15.5 10.067 15.5 12C15.5 13.933 13.933 15.5 12 15.5Z" fill="white"/>
        </svg>""",
        
        "plangrid": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="24" height="24" rx="4" fill="#2E2E2E"/>
            <path d="M12.5 5L19 8.5V15.5L12.5 19L6 15.5V8.5L12.5 5Z" stroke="#00AEFF" stroke-width="1.5"/>
            <path d="M12.5 12L19 8.5M12.5 12L6 8.5M12.5 12V19" stroke="#00AEFF" stroke-width="1.5"/>
        </svg>""",
        
        "google_calendar": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19.5 3H18V1.5H16.5V3H7.5V1.5H6V3H4.5C3.675 3 3 3.675 3 4.5V19.5C3 20.325 3.675 21 4.5 21H19.5C20.325 21 21 20.325 21 19.5V4.5C21 3.675 20.325 3 19.5 3ZM19.5 19.5H4.5V7.5H19.5V19.5Z" fill="#4285F4"/>
            <path d="M6 10.5H9V13.5H6V10.5Z" fill="#4285F4"/>
            <path d="M10.5 10.5H13.5V13.5H10.5V10.5Z" fill="#4285F4"/>
            <path d="M15 10.5H18V13.5H15V10.5Z" fill="#4285F4"/>
            <path d="M6 15H9V18H6V15Z" fill="#4285F4"/>
            <path d="M10.5 15H13.5V18H10.5V15Z" fill="#4285F4"/>
        </svg>""",
        
        "outlook": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M13.5 4.5H6C5.175 4.5 4.5 5.175 4.5 6V18C4.5 18.825 5.175 19.5 6 19.5H18C18.825 19.5 19.5 18.825 19.5 18V10.5" fill="#0078D4"/>
            <path d="M19.5 4.5L13.5 10.5H19.5V4.5Z" fill="#0078D4"/>
            <path d="M4.5 9L12 12L19.5 9V6L12 9L4.5 6V9Z" fill="#0078D4"/>
        </svg>""",
        
        "dropbox": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 6.375L7.5 9.375L12 12.375L7.5 15.375L3 12.375L7.5 9.375L3 6.375L7.5 3.375L12 6.375Z" fill="#0061FF"/>
            <path d="M12 6.375L16.5 3.375L21 6.375L16.5 9.375L21 12.375L16.5 15.375L12 12.375L16.5 9.375L12 6.375Z" fill="#0061FF"/>
            <path d="M12 12.375V15.375L7.5 18.375L3 15.375V12.375L7.5 15.375L12 12.375Z" fill="#0061FF"/>
            <path d="M12 12.375L16.5 15.375L21 12.375V15.375L16.5 18.375L12 15.375V12.375Z" fill="#0061FF"/>
        </svg>""",
        
        "google_drive": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4.5 15L9 6H15L10.5 15H4.5Z" fill="#0066DA"/>
            <path d="M10.5 15L15 6L19.5 15H10.5Z" fill="#00AC47"/>
            <path d="M4.5 15L7.5 20.25H16.5L19.5 15H4.5Z" fill="#EA4335"/>
        </svg>""",
        
        "onedrive": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14.25 8.25C13.2 6.9 11.55 6 9.75 6C6.6 6 4.05 8.55 4.05 11.7C4.05 11.85 4.05 12 4.05 12.15C2.25 12.6 0.9 14.25 0.9 16.2C0.9 18.45 2.7 20.25 4.95 20.25H14.4C17.1 20.25 19.2 18.15 19.2 15.45C19.2 12.9 17.1 10.8 14.4 10.8C14.4 10.8 14.325 8.325 14.25 8.25Z" fill="#0364B8"/>
            <path d="M14.25 8.25C14.325 8.325 14.4 10.8 14.4 10.8C17.1 10.8 19.2 12.9 19.2 15.45C19.2 18.15 17.1 20.25 14.4 20.25H14.325L19.425 13.2C20.25 12 19.8 10.35 18.45 9.6L14.25 8.25Z" fill="#0078D4"/>
            <path d="M14.25 8.25L18.45 9.6C19.8 10.35 20.25 12 19.425 13.2L14.325 20.25H14.4C17.1 20.25 19.2 18.15 19.2 15.45C19.2 12.9 17.1 10.8 14.4 10.8C14.4 10.8 14.325 8.325 14.25 8.25Z" fill="#1490DF"/>
            <path d="M9.75 12.975L4.05 12.15C4.05 12 4.05 11.85 4.05 11.7C4.05 8.55 6.6 6 9.75 6C11.55 6 13.2 6.9 14.25 8.25L9.75 12.975Z" fill="#28A8EA"/>
        </svg>"""
    }
    
    return logos.get(provider_id, "")