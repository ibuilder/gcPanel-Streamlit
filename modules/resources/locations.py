import streamlit as st
import pandas as pd
from modules.base_module import BaseModule
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "Locations"
MODULE_ICON = "map-pin"

# Define module columns
COLUMNS = [
    ('id', 'ID', 'integer'),
    ('location_name', 'Location Name', 'text'),
    ('location_code', 'Location Code', 'text'),
    ('location_type', 'Location Type', 'text'),
    ('parent_location_id', 'Parent Location ID', 'integer'),
    ('level', 'Level', 'text'),
    ('area_sqft', 'Area (sq ft)', 'float'),
    ('description', 'Description', 'text'),
    ('coordinates', 'Coordinates', 'text'),
    ('is_active', 'Active', 'boolean')
]

# Define form fields
FORM_FIELDS = [
    ('id', 'ID', 'integer', False, None),
    ('location_name', 'Location Name', 'text', True, None),
    ('location_code', 'Location Code', 'text', True, None),
    ('location_type', 'Location Type', 'select', True, ['Building', 'Floor', 'Room', 'Area', 'Zone', 'Other']),
    ('parent_location_id', 'Parent Location', 'integer', False, None),
    ('level', 'Level', 'text', False, None),
    ('area_sqft', 'Area (sq ft)', 'number', False, None),
    ('description', 'Description', 'textarea', False, None),
    ('coordinates', 'Coordinates', 'text', False, None),
    ('is_active', 'Active', 'boolean', False, None)
]

# Create module instance
locations_module = BaseModule('locations', 'Locations', COLUMNS, FORM_FIELDS)

def get_location_tree():
    """Get hierarchical location tree for display"""
    try:
        conn = get_db_connection()
        if not conn:
            return {}
            
        cursor = conn.cursor()
        
        # Get all locations
        cursor.execute("""
            SELECT id, location_name, location_code, parent_location_id, location_type
            FROM locations
            ORDER BY parent_location_id NULLS FIRST, location_name
        """)
        
        locations = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Build location tree
        location_tree = {}
        location_map = {}
        
        # First, build a map of all locations
        for loc in locations:
            loc_id, name, code, parent_id, loc_type = loc
            location_map[loc_id] = {
                'name': name,
                'code': code,
                'type': loc_type,
                'children': []
            }
        
        # Then build the tree
        for loc in locations:
            loc_id, name, code, parent_id, loc_type = loc
            
            if parent_id is None:
                # Root location
                location_tree[loc_id] = location_map[loc_id]
            else:
                # Child location - add to parent's children if parent exists
                if parent_id in location_map:
                    location_map[parent_id]['children'].append(location_map[loc_id])
        
        return location_tree
        
    except Exception as e:
        st.error(f"Error building location tree: {str(e)}")
        return {}

def render_location_tree(tree, level=0):
    """Recursively render the location tree"""
    for loc_id, loc_data in tree.items():
        prefix = "    " * level
        st.markdown(f"{prefix}📍 **{loc_data['name']}** ({loc_data['code']}) - {loc_data['type']}")
        
        if loc_data['children']:
            for child in loc_data['children']:
                prefix_child = "    " * (level + 1)
                st.markdown(f"{prefix_child}🔹 **{child['name']}** ({child['code']}) - {child['type']}")
                
                # Recursive render for child's children
                if child['children']:
                    render_child_location_tree(child['children'], level + 2)

def render_child_location_tree(children, level=0):
    """Recursively render children of a location"""
    for child in children:
        prefix = "    " * level
        st.markdown(f"{prefix}🔸 **{child['name']}** ({child['code']}) - {child['type']}")
        
        if child['children']:
            render_child_location_tree(child['children'], level + 1)

def render_list():
    """Render the list view with hierarchical location tree"""
    st.title("Project Locations")
    
    # Check permission
    if not check_permission('read'):
        st.error("You don't have permission to view locations")
        return
    
    # Standard list view
    locations_module.render_list()
    
    # Display location hierarchy
    st.subheader("Location Hierarchy")
    
    # Get location tree
    location_tree = get_location_tree()
    
    if location_tree:
        render_location_tree(location_tree)
    else:
        st.info("No location hierarchy defined")

def render_view():
    """Render the detail view"""
    locations_module.render_view()

def render_form():
    """Render the form view with parent location selection"""
    st.title("Location Form")
    
    # Check permissions
    editing_id = st.session_state.get('editing_id')
    if editing_id and not check_permission('update'):
        st.error("You don't have permission to update locations")
        return
    elif not editing_id and not check_permission('create'):
        st.error("You don't have permission to create locations")
        return
    
    # Set title based on mode
    if editing_id:
        st.title(f"Edit Location")
    else:
        st.title(f"New Location")
    
    # If editing, fetch the current record
    current_values = {}
    if editing_id:
        try:
            conn = get_db_connection()
            if not conn:
                return
                
            cursor = conn.cursor()
            
            # Get column names for SELECT
            column_names = [col[0] for col in COLUMNS]
            columns_str = ', '.join(column_names)
            
            cursor.execute(f"SELECT {columns_str} FROM locations WHERE id = %s", (editing_id,))
            record = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if record:
                # Create a dictionary of current values
                current_values = {col[0]: val for col, val in zip(COLUMNS, record)}
            else:
                st.error("Location not found")
                return
                
        except Exception as e:
            st.error(f"Error loading location for editing: {str(e)}")
            return
    
    # Get all locations for parent selection
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        
        # Get locations that can be parents (exclude current location if editing)
        if editing_id:
            cursor.execute("""
                SELECT id, location_name, location_code 
                FROM locations 
                WHERE id != %s
                ORDER BY location_name
            """, (editing_id,))
        else:
            cursor.execute("""
                SELECT id, location_name, location_code 
                FROM locations 
                ORDER BY location_name
            """)
            
        parent_options = cursor.fetchall()
        cursor.close()
        conn.close()
        
    except Exception as e:
        st.error(f"Error fetching parent locations: {str(e)}")
        parent_options = []
    
    # Create the form
    with st.form(f"location_form"):
        # Create form fields
        form_data = {}
        
        # Create columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            form_data['location_name'] = st.text_input(
                "Location Name *",
                value=current_values.get('location_name', ''),
                key="form_location_name"
            )
            
            form_data['location_code'] = st.text_input(
                "Location Code *",
                value=current_values.get('location_code', ''),
                key="form_location_code"
            )
            
            form_data['location_type'] = st.selectbox(
                "Location Type *",
                options=['Building', 'Floor', 'Room', 'Area', 'Zone', 'Other'],
                index=0 if 'location_type' not in current_values else ['Building', 'Floor', 'Room', 'Area', 'Zone', 'Other'].index(current_values['location_type']),
                key="form_location_type"
            )
            
            # Parent location select
            parent_options_dict = {f"{p[0]} - {p[1]} ({p[2]})": p[0] for p in parent_options}
            parent_options_dict["None"] = None
            
            selected_parent = "None"
            if 'parent_location_id' in current_values and current_values['parent_location_id'] is not None:
                for key, value in parent_options_dict.items():
                    if value == current_values['parent_location_id']:
                        selected_parent = key
                        break
            
            parent_selection = st.selectbox(
                "Parent Location",
                options=list(parent_options_dict.keys()),
                index=list(parent_options_dict.keys()).index(selected_parent) if selected_parent in parent_options_dict else 0,
                key="form_parent_location"
            )
            
            form_data['parent_location_id'] = parent_options_dict[parent_selection]
            
            form_data['level'] = st.text_input(
                "Level",
                value=current_values.get('level', ''),
                key="form_level"
            )
            
        with col2:
            form_data['area_sqft'] = st.number_input(
                "Area (sq ft)",
                value=float(current_values.get('area_sqft', 0)),
                min_value=0.0,
                key="form_area_sqft"
            )
            
            form_data['coordinates'] = st.text_input(
                "Coordinates",
                value=current_values.get('coordinates', ''),
                key="form_coordinates"
            )
            
            form_data['is_active'] = st.checkbox(
                "Active",
                value=current_values.get('is_active', True),
                key="form_is_active"
            )
            
            form_data['description'] = st.text_area(
                "Description",
                value=current_values.get('description', ''),
                key="form_description"
            )
        
        # ID field if editing
        if editing_id:
            form_data['id'] = editing_id
        
        # Submit button
        submit_text = "Update" if editing_id else "Create"
        submitted = st.form_submit_button(submit_text)
        
        if submitted:
            # Validate required fields
            if not form_data['location_name'] or not form_data['location_code']:
                st.error("Location Name and Location Code are required")
            else:
                # Save the record
                try:
                    conn = get_db_connection()
                    if not conn:
                        return
                        
                    cursor = conn.cursor()
                    
                    if editing_id:
                        # Update existing record
                        update_fields = []
                        update_values = []
                        
                        for name, value in form_data.items():
                            if name != 'id':  # Skip ID field for update
                                update_fields.append(f"{name} = %s")
                                update_values.append(value)
                        
                        # Add audit fields
                        update_fields.append("updated_by = %s")
                        update_values.append(st.session_state.get('user_id'))
                        update_fields.append("updated_at = CURRENT_TIMESTAMP")
                        
                        # Add ID for WHERE clause
                        update_values.append(editing_id)
                        
                        update_sql = f"UPDATE locations SET {', '.join(update_fields)} WHERE id = %s"
                        cursor.execute(update_sql, update_values)
                        
                    else:
                        # Insert new record
                        field_names = list(form_data.keys())
                        field_placeholders = ["%s"] * len(field_names)
                        field_values = list(form_data.values())
                        
                        # Add audit fields
                        field_names.append("created_by")
                        field_placeholders.append("%s")
                        field_values.append(st.session_state.get('user_id'))
                        
                        # Create SQL
                        insert_sql = f"INSERT INTO locations ({', '.join(field_names)}) VALUES ({', '.join(field_placeholders)})"
                        cursor.execute(insert_sql, field_values)
                    
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    st.success(f"Location {'updated' if editing_id else 'created'} successfully")
                    
                    # Reset and go back to list view
                    if 'editing_id' in st.session_state:
                        del st.session_state.editing_id
                    st.session_state.current_view = "list"
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error saving location: {str(e)}")
