"""
Script to add authentication checks to all construction module pages
"""

import os
import re

def add_authentication_check(file_path):
    """Add authentication check to a page file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if authentication check already exists
    if "check_authentication" in content:
        print(f"Authentication already exists in {file_path}")
        return
    
    # Add import for check_authentication
    if "from utils.helpers import" not in content:
        # Add the import after sys.path.append
        content = re.sub(
            r"(sys\.path\.append\([^)]+\))",
            r"\1\n\nfrom utils.helpers import check_authentication",
            content
        )
    else:
        # Add to existing import
        content = re.sub(
            r"from utils\.helpers import ([^\n]+)",
            r"from utils.helpers import \1, check_authentication",
            content
        )
    
    # Add authentication check after page config
    auth_check = """
# Check authentication
if not check_authentication():
    st.error("🔒 Please log in to access this page")
    st.stop()
"""
    
    # Insert after st.set_page_config
    content = re.sub(
        r"(st\.set_page_config[^)]+\))",
        r"\1" + auth_check,
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Added authentication to {file_path}")

def main():
    """Add authentication to all page files"""
    pages_dir = 'pages'
    
    for filename in os.listdir(pages_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            file_path = os.path.join(pages_dir, filename)
            add_authentication_check(file_path)
    
    print("Authentication checks added to all pages!")

if __name__ == "__main__":
    main()