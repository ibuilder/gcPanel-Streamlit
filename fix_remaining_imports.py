"""
Script to fix remaining import issues in all pages
"""

import os
import re

def fix_page_imports(file_path):
    """Fix imports in a page file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if the page calls check_authentication but doesn't import it
    if "check_authentication()" in content and "from lib.utils.helpers import check_authentication" not in content:
        # Find where to insert the import
        lines = content.split('\n')
        new_lines = []
        import_added = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # Add imports after initial imports but before page config
            if "import os" in line and not import_added:
                new_lines.append("")
                new_lines.append("# Add project root to path for imports")
                new_lines.append("sys.path.append(os.path.dirname(os.path.abspath(__file__)))")
                new_lines.append("")
                new_lines.append("from lib.utils.helpers import check_authentication")
                import_added = True
            elif "st.set_page_config" in line and not import_added:
                # Insert before page config if no os import found
                new_lines.insert(-1, "import sys")
                new_lines.insert(-1, "import os")
                new_lines.insert(-1, "")
                new_lines.insert(-1, "# Add project root to path for imports")
                new_lines.insert(-1, "sys.path.append(os.path.dirname(os.path.abspath(__file__)))")
                new_lines.insert(-1, "")
                new_lines.insert(-1, "from lib.utils.helpers import check_authentication")
                new_lines.insert(-1, "")
                import_added = True
        
        if import_added:
            with open(file_path, 'w') as f:
                f.write('\n'.join(new_lines))
            print(f"Fixed imports in {file_path}")
        else:
            print(f"No changes needed in {file_path}")

def main():
    """Fix imports in all page files"""
    pages_dir = 'pages'
    
    for filename in os.listdir(pages_dir):
        if filename.endswith('.py'):
            file_path = os.path.join(pages_dir, filename)
            fix_page_imports(file_path)
    
    print("Import fixes completed!")

if __name__ == "__main__":
    main()