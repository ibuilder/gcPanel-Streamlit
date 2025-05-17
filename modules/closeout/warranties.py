import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.base_module import BaseModule
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "Warranties"
MODULE_ICON = "award"

# Define module columns
COLUMNS = [
    ('id', 'ID', 'integer'),
    ('warranty_number', 'Warranty #', 'text'),
    ('title', 'Title', 'text'),
    ('description', 'Description', 'text'),
    ('start_date', 'Start Date', 'date'),
    ('end_date', 'End Date', 'date'),
    ('duration_months', 'Duration (Months)', 'integer'),
    ('provider', 'Provider', 'text'),
    ('provider_contact', 'Provider Contact', 'text'),
    ('provider_phone', 'Provider Phone', 'text'),
    ('provider_email', 'Provider Email', 'text'),
    ('category', 'Category', 'text'),
    ('status', 'Status', 'text'),
    ('notes', 'Notes', 'text')
]

# Define form fields
FORM_FIELDS = [
    ('id', 'ID', 'integer', False, None),
    ('warranty_number', 'Warranty #', 'text', True, None),
    ('title', 'Title', 'text', True, None),
    ('description', 'Description', 'textarea', False, None),
    ('start_date', 'Start Date', 'date', True, None),
    ('duration_months', 'Duration (Months)', 'integer', True, None),
    ('provider', 'Provider', 'text', True, None),
    ('provider_contact', 'Provider Contact', 'text', False, None),
    ('provider_phone', 'Provider Phone', 'text', False, None),
    ('provider_email', 'Provider Email', 'text', False, None),
    ('category', 'Category', 'select', True, ['General', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Roofing', 'Exterior', 'Interior', 'Other']),
    ('status', 'Status', 'select', True, ['Active', 'Pending', 'Expired', 'Void']),
    ('notes', 'Notes', 'textarea', False, None)
]

# Create module instance
warranties_module = BaseModule('warranties', 'Warranties', COLUMNS, FORM_FIELDS)

def render_list():
    """Render the list view with additional warranty analytics"""
    # Render the standard list view
    warranties_module.render_list()
    
    # Add warranty analytics
    st.subheader("Warranty Analytics")
    
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        # Get warranty data
        warranty_df = pd.read_sql_query("""
            SELECT 
                category,
                status,
                start_date,
                end_date,
                CURRENT_DATE > end_date as is_expired
            FROM warranties
            ORDER BY start_date
        """, conn)
        
        conn.close()
        
        if not warranty_df.empty:
            # Create two columns for charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Category distribution
                st.subheader("Warranties by Category")
                category_counts = warranty_df['category'].value_counts()
                st.bar_chart(category_counts)
                
                # Status distribution
                st.subheader("Warranties by Status")
                status_counts = warranty_df['status'].value_counts()
                st.bar_chart(status_counts)
            
            with col2:
                # Calculate expiring soon (next 90 days)
                current_date = datetime.now().date()
                expiring_soon = warranty_df[
                    (warranty_df['end_date'] > current_date) & 
                    (warranty_df['end_date'] <= (current_date + timedelta(days=90)))
                ]
                
                # Display expiring soon
                st.subheader("Warranties Expiring Soon (90 Days)")
                if not expiring_soon.empty:
                    expiring_display = expiring_soon[['category', 'end_date']].sort_values('end_date')
                    expiring_display.columns = ['Category', 'Expiration Date']
                    st.dataframe(expiring_display)
                else:
                    st.info("No warranties expiring in the next 90 days")
                
                # Display expired warranties
                st.subheader("Expired Warranties")
                expired = warranty_df[warranty_df['is_expired'] == True]
                if not expired.empty:
                    expired_display = expired[['category', 'end_date']].sort_values('end_date', ascending=False)
                    expired_display.columns = ['Category', 'Expiration Date']
                    st.dataframe(expired_display)
                else:
                    st.info("No expired warranties")
        else:
            st.info("No warranty data available")
            
    except Exception as e:
        st.error(f"Error fetching warranty data: {str(e)}")

def render_view():
    """Render the detail view"""
    warranties_module.render_view()

def render_form():
    """Render the form view with end date calculation"""
    st.title("Warranty Form")
    
    # Check permissions
    editing_id = st.session_state.get('editing_id')
    if editing_id and not check_permission('update'):
        st.error("You don't have permission to update records")
        return
    elif not editing_id and not check_permission('create'):
        st.error("You don't have permission to create records")
        return
    
    # Set title based on mode
    if editing_id:
        st.title(f"Edit Warranty")
    else:
        st.title(f"New Warranty")
    
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
            
            cursor.execute(f"SELECT {columns_str} FROM warranties WHERE id = %s", (editing_id,))
            record = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if record:
                # Create a dictionary of current values
                current_values = {col[0]: val for col, val in zip(COLUMNS, record)}
            else:
                st.error("Record not found")
                return
                
        except Exception as e:
            st.error(f"Error loading record for editing: {str(e)}")
            return
    
    # Create the form
    with st.form(f"warranty_form"):
        # Create form fields
        form_data = {}
        
        # Create columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            form_data['warranty_number'] = st.text_input(
                "Warranty # *",
                value=current_values.get('warranty_number', ''),
                key="form_warranty_number"
            )
            
            form_data['title'] = st.text_input(
                "Title *",
                value=current_values.get('title', ''),
                key="form_title"
            )
            
            form_data['description'] = st.text_area(
                "Description",
                value=current_values.get('description', ''),
                key="form_description"
            )
            
            form_data['start_date'] = st.date_input(
                "Start Date *",
                value=current_values.get('start_date', datetime.now().date()),
                key="form_start_date"
            )
            
            form_data['duration_months'] = st.number_input(
                "Duration (Months) *",
                value=int(current_values.get('duration_months', 12)),
                min_value=1,
                step=1,
                key="form_duration_months"
            )
            
            # Calculate end date
            if form_data['start_date'] and form_data['duration_months']:
                # Calculate end date based on start date and duration
                end_date = form_data['start_date'] + timedelta(days=form_data['duration_months'] * 30)
                form_data['end_date'] = end_date
                st.write(f"End Date: {end_date.strftime('%Y-%m-%d')}")
            
            form_data['category'] = st.selectbox(
                "Category *",
                options=['General', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Roofing', 'Exterior', 'Interior', 'Other'],
                index=0 if 'category' not in current_values else ['General', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Roofing', 'Exterior', 'Interior', 'Other'].index(current_values['category']),
                key="form_category"
            )
            
        with col2:
            form_data['provider'] = st.text_input(
                "Provider *",
                value=current_values.get('provider', ''),
                key="form_provider"
            )
            
            form_data['provider_contact'] = st.text_input(
                "Provider Contact",
                value=current_values.get('provider_contact', ''),
                key="form_provider_contact"
            )
            
            form_data['provider_phone'] = st.text_input(
                "Provider Phone",
                value=current_values.get('provider_phone', ''),
                key="form_provider_phone"
            )
            
            form_data['provider_email'] = st.text_input(
                "Provider Email",
                value=current_values.get('provider_email', ''),
                key="form_provider_email"
            )
            
            form_data['status'] = st.selectbox(
                "Status *",
                options=['Active', 'Pending', 'Expired', 'Void'],
                index=0 if 'status' not in current_values else ['Active', 'Pending', 'Expired', 'Void'].index(current_values['status']),
                key="form_status"
            )
            
            form_data['notes'] = st.text_area(
                "Notes",
                value=current_values.get('notes', ''),
                key="form_notes"
            )
        
        # ID field if editing
        if editing_id:
            form_data['id'] = editing_id
        
        # Submit button
        submit_text = "Update" if editing_id else "Create"
        submitted = st.form_submit_button(submit_text)
        
        if submitted:
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
                    
                    update_sql = f"UPDATE warranties SET {', '.join(update_fields)} WHERE id = %s"
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
                    insert_sql = f"INSERT INTO warranties ({', '.join(field_names)}) VALUES ({', '.join(field_placeholders)})"
                    cursor.execute(insert_sql, field_values)
                
                conn.commit()
                cursor.close()
                conn.close()
                
                st.success(f"Warranty {'updated' if editing_id else 'created'} successfully")
                
                # Reset and go back to list view
                if 'editing_id' in st.session_state:
                    del st.session_state.editing_id
                st.session_state.current_view = "list"
                st.rerun()
                
            except Exception as e:
                st.error(f"Error saving record: {str(e)}")
