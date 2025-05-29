"""
Script to fix syntax errors in page imports
"""

import os
import re

def fix_page_syntax(file_path):
    """Fix syntax errors in a page file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix malformed import statements
    content = re.sub(
        r'from utils\.helpers import check_authentication\)\)\)',
        'from utils.helpers import check_authentication',
        content
    )
    
    # Fix missing closing parenthesis in sys.path.append
    content = re.sub(
        r'sys\.path\.append\(os\.path\.dirname\(os\.path\.dirname\(os\.path\.abspath\(__file__\)\n',
        'sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))',
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed syntax in {file_path}")

def main():
    """Fix syntax errors in all page files"""
    pages_dir = 'pages'
    
    for filename in os.listdir(pages_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            file_path = os.path.join(pages_dir, filename)
            fix_page_syntax(file_path)
    
    print("Syntax errors fixed in all pages!")

if __name__ == "__main__":
    main()