#!/usr/bin/env python3
"""
Script to enhance CRUD functionality by adding view and edit capabilities to data tables
"""

import os
import re

def add_crud_enhancements():
    # Define the pages that need CRUD enhancements
    pages_to_enhance = [
        "pages/05_📑_Contracts.py",
        "pages/06_🦺_Safety.py", 
        "pages/04_📨_Submittals.py",
        "pages/03_📄_RFIs.py",
        "pages/15_📅_Scheduling.py",
        "pages/18_👷_Subcontractor_Management.py"
    ]
    
    for file_path in pages_to_enhance:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Add view mode toggle and card view functionality
            if 'view_mode = st.radio("View Mode:"' not in content:
                # Find the dataframe display section and enhance it
                pattern = r'st\.write\(f"\*\*Total [^:]+:\*\* \{len\(filtered_df\)\}"\)\s+if not filtered_df\.empty:'
                replacement = '''st.write(f"**Total {item_type}:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            # Add view mode toggle
            view_mode = st.radio("View Mode:", ["📊 Table View", "📋 Card View"], horizontal=True, key=f"{module_name}_view_mode")
            
            if view_mode == "📋 Card View":
                # Display as cards with action buttons
                for idx, row in filtered_df.iterrows():
                    with st.container():
                        st.markdown("---")
                        col1, col2, col3 = st.columns([3, 2, 1])
                        
                        with col1:
                            st.subheader(f"📋 {row.get('title', row.get('id', 'Record'))}")
                            # Display key fields
                            for key, value in row.items():
                                if key in ['id', 'status', 'type'] and key != 'title':
                                    st.write(f"**{key.title()}:** {value}")
                                    if len([k for k in row.items() if k[0] in ['id', 'status', 'type']]) >= 3:
                                        break
                        
                        with col2:
                            # Display additional fields
                            other_fields = [k for k in row.items() if k[0] not in ['id', 'title', 'status', 'type']]
                            for key, value in other_fields[:3]:
                                st.write(f"**{key.title()}:** {value}")
                        
                        with col3:
                            if st.button("👁️ View", key=f"view_{module_name}_{row.get('id', idx)}", help="View details", use_container_width=True):
                                st.session_state[f'selected_{module_name}'] = row.to_dict()
                                st.session_state[f'show_{module_name}_detail'] = True
                            if st.button("✏️ Edit", key=f"edit_{module_name}_{row.get('id', idx)}", help="Edit record", use_container_width=True):
                                st.session_state[f'edit_{module_name}'] = row.to_dict()
                                st.session_state[f'show_{module_name}_edit'] = True
            
            else:  # Table View
                # Original table display
                if not filtered_df.empty:'''
                
                # This is a complex transformation, let's do it manually for key pages
                print(f"Would enhance {file_path}")
    
    print("CRUD enhancements planned for key modules")

if __name__ == "__main__":
    add_crud_enhancements()