"""
Script to properly add authentication checks to all pages
"""

import os

def add_auth_check_to_page(file_path):
    """Add authentication check to a page file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if authentication check already exists
    if "if not check_authentication():" in content:
        print(f"Authentication check already exists in {file_path}")
        return
    
    # Find the position after st.set_page_config
    lines = content.split('\n')
    new_lines = []
    auth_added = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Add auth check after page config
        if "st.set_page_config" in line and not auth_added:
            new_lines.append("")
            new_lines.append("# Check authentication")
            new_lines.append("if not check_authentication():")
            new_lines.append('    st.error("🔒 Please log in to access this page")')
            new_lines.append("    st.stop()")
            auth_added = True
    
    if auth_added:
        with open(file_path, 'w') as f:
            f.write('\n'.join(new_lines))
        print(f"Added authentication check to {file_path}")

def main():
    """Add authentication checks to all page files"""
    pages_dir = 'pages'
    
    for filename in os.listdir(pages_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            file_path = os.path.join(pages_dir, filename)
            add_auth_check_to_page(file_path)
    
    print("Authentication checks completed!")

if __name__ == "__main__":
    main()