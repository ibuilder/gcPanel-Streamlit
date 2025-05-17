import streamlit as st
import pandas as pd
import numpy as np
from modules.base_module import BaseModule
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "Budget and Forecast"
MODULE_ICON = "dollar-sign"

# Define module columns
COLUMNS = [
    ('id', 'ID', 'integer'),
    ('cost_code', 'Cost Code', 'text'),
    ('description', 'Description', 'text'),
    ('original_budget', 'Original Budget', 'float'),
    ('approved_changes', 'Approved Changes', 'float'),
    ('current_budget', 'Current Budget', 'float'),
    ('committed_costs', 'Committed Costs', 'float'),
    ('actual_costs', 'Actual Costs', 'float'),
    ('projected_costs', 'Projected Costs', 'float'),
    ('variance', 'Variance', 'float'),
    ('percent_complete', 'Percent Complete', 'float'),
    ('division', 'Division', 'text'),
    ('phase', 'Phase', 'text'),
    ('notes', 'Notes', 'text')
]

# Define form fields
FORM_FIELDS = [
    ('id', 'ID', 'integer', False, None),
    ('cost_code', 'Cost Code', 'text', True, None),
    ('description', 'Description', 'text', True, None),
    ('original_budget', 'Original Budget', 'number', True, None),
    ('approved_changes', 'Approved Changes', 'number', False, None),
    ('current_budget', 'Current Budget', 'number', True, None),
    ('committed_costs', 'Committed Costs', 'number', False, None),
    ('actual_costs', 'Actual Costs', 'number', False, None),
    ('projected_costs', 'Projected Costs', 'number', False, None),
    ('variance', 'Variance', 'number', False, None),
    ('percent_complete', 'Percent Complete', 'number', False, None),
    ('division', 'Division', 'text', True, None),
    ('phase', 'Phase', 'text', False, None),
    ('notes', 'Notes', 'textarea', False, None)
]

# Create module instance
budget_module = BaseModule('budget', 'Budget and Forecast', COLUMNS, FORM_FIELDS)

def render_list():
    """Render the list view with additional budget analytics"""
    # Render the standard list view
    budget_module.render_list()
    
    # Add budget analytics
    st.subheader("Budget Analytics")
    
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        # Get budget data
        budget_df = pd.read_sql_query("""
            SELECT 
                division,
                SUM(original_budget) as original_budget,
                SUM(current_budget) as current_budget,
                SUM(committed_costs) as committed_costs,
                SUM(actual_costs) as actual_costs,
                SUM(projected_costs) as projected_costs,
                SUM(variance) as variance
            FROM budget
            GROUP BY division
            ORDER BY division
        """, conn)
        
        conn.close()
        
        if not budget_df.empty:
            # Create budget summary
            st.subheader("Budget Summary by Division")
            
            # Format as currency
            currency_cols = ['original_budget', 'current_budget', 'committed_costs', 
                            'actual_costs', 'projected_costs', 'variance']
            for col in currency_cols:
                budget_df[col] = budget_df[col].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "$0.00")
            
            st.dataframe(budget_df)
            
            # Get overall summary
            conn = get_db_connection()
            summary_df = pd.read_sql_query("""
                SELECT 
                    SUM(original_budget) as original_budget,
                    SUM(current_budget) as current_budget,
                    SUM(committed_costs) as committed_costs,
                    SUM(actual_costs) as actual_costs,
                    SUM(projected_costs) as projected_costs,
                    SUM(variance) as variance
                FROM budget
            """, conn)
            conn.close()
            
            # Display summary metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Original Budget", f"${summary_df['original_budget'].iloc[0]:,.2f}")
                st.metric("Current Budget", f"${summary_df['current_budget'].iloc[0]:,.2f}")
            
            with col2:
                st.metric("Committed Costs", f"${summary_df['committed_costs'].iloc[0]:,.2f}")
                st.metric("Actual Costs", f"${summary_df['actual_costs'].iloc[0]:,.2f}")
            
            with col3:
                st.metric("Projected Costs", f"${summary_df['projected_costs'].iloc[0]:,.2f}")
                variance = summary_df['variance'].iloc[0]
                variance_color = "normal" if variance >= 0 else "inverse"
                st.metric("Variance", f"${variance:,.2f}", delta_color=variance_color)
            
            # Create budget visualization
            st.subheader("Budget vs. Actual by Division")
            
            # Prepare data for chart
            conn = get_db_connection()
            chart_data = pd.read_sql_query("""
                SELECT 
                    division,
                    SUM(current_budget) as budget,
                    SUM(actual_costs) as actual
                FROM budget
                GROUP BY division
                ORDER BY division
            """, conn)
            conn.close()
            
            # Create chart
            budget_chart = pd.DataFrame({
                'Division': chart_data['division'],
                'Budget': chart_data['budget'],
                'Actual': chart_data['actual']
            }).set_index('Division')
            
            st.bar_chart(budget_chart)
            
        else:
            st.info("No budget data available")
            
    except Exception as e:
        st.error(f"Error fetching budget data: {str(e)}")

def render_view():
    """Render the detail view"""
    budget_module.render_view()

def render_form():
    """Render the form view with some calculated fields"""
    st.title("Budget and Forecast")
    
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
        st.title(f"Edit Budget Item")
    else:
        st.title(f"New Budget Item")
    
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
            
            cursor.execute(f"SELECT {columns_str} FROM budget WHERE id = %s", (editing_id,))
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
    
    # Get divisions from resources if available
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if csi_divisions table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'csi_divisions'
            )
        """)
        
        if cursor.fetchone()[0]:
            cursor.execute("SELECT division_code, division_name FROM csi_divisions ORDER BY division_code")
            divisions = cursor.fetchall()
            division_options = [f"{div[0]} - {div[1]}" for div in divisions]
        else:
            # Default CSI divisions
            division_options = [
                "01 - General Requirements", 
                "02 - Existing Conditions",
                "03 - Concrete",
                "04 - Masonry",
                "05 - Metals",
                "06 - Wood, Plastics, and Composites",
                "07 - Thermal and Moisture Protection",
                "08 - Openings",
                "09 - Finishes",
                "10 - Specialties",
                "11 - Equipment",
                "12 - Furnishings",
                "13 - Special Construction",
                "14 - Conveying Equipment",
                "21 - Fire Suppression",
                "22 - Plumbing",
                "23 - HVAC",
                "26 - Electrical",
                "27 - Communications",
                "28 - Electronic Safety and Security",
                "31 - Earthwork",
                "32 - Exterior Improvements",
                "33 - Utilities"
            ]
        
        cursor.close()
        conn.close()
        
    except Exception:
        # Default CSI divisions if database query fails
        division_options = [f"{i:02d} - Division {i:02d}" for i in range(1, 34)]
    
    # Create the form
    with st.form(f"budget_form"):
        # Create form fields
        form_data = {}
        
        # Create columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            form_data['cost_code'] = st.text_input(
                "Cost Code *",
                value=current_values.get('cost_code', ''),
                key="form_cost_code"
            )
            
            form_data['description'] = st.text_input(
                "Description *",
                value=current_values.get('description', ''),
                key="form_description"
            )
            
            form_data['division'] = st.selectbox(
                "Division *",
                options=division_options,
                index=0 if 'division' not in current_values else division_options.index(current_values['division']),
                key="form_division"
            )
            
            form_data['phase'] = st.text_input(
                "Phase",
                value=current_values.get('phase', ''),
                key="form_phase"
            )
            
            form_data['original_budget'] = st.number_input(
                "Original Budget *",
                value=float(current_values.get('original_budget', 0)),
                min_value=0.0,
                key="form_original_budget"
            )
            
            form_data['approved_changes'] = st.number_input(
                "Approved Changes",
                value=float(current_values.get('approved_changes', 0)),
                key="form_approved_changes"
            )
            
            # Calculate current budget
            current_budget = form_data['original_budget'] + form_data['approved_changes']
            form_data['current_budget'] = current_budget
            st.write(f"Current Budget: ${current_budget:,.2f}")
            
        with col2:
            form_data['committed_costs'] = st.number_input(
                "Committed Costs",
                value=float(current_values.get('committed_costs', 0)),
                min_value=0.0,
                key="form_committed_costs"
            )
            
            form_data['actual_costs'] = st.number_input(
                "Actual Costs",
                value=float(current_values.get('actual_costs', 0)),
                min_value=0.0,
                key="form_actual_costs"
            )
            
            form_data['projected_costs'] = st.number_input(
                "Projected Costs",
                value=float(current_values.get('projected_costs', 0)),
                min_value=0.0,
                key="form_projected_costs"
            )
            
            # Calculate variance
            variance = current_budget - form_data['projected_costs']
            form_data['variance'] = variance
            variance_color = "green" if variance >= 0 else "red"
            st.markdown(f"Variance: <span style='color:{variance_color}'>${variance:,.2f}</span>", unsafe_allow_html=True)
            
            form_data['percent_complete'] = st.slider(
                "Percent Complete",
                min_value=0.0,
                max_value=100.0,
                value=float(current_values.get('percent_complete', 0)),
                step=0.1,
                key="form_percent_complete"
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
                    
                    update_sql = f"UPDATE budget SET {', '.join(update_fields)} WHERE id = %s"
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
                    insert_sql = f"INSERT INTO budget ({', '.join(field_names)}) VALUES ({', '.join(field_placeholders)})"
                    cursor.execute(insert_sql, field_values)
                
                conn.commit()
                cursor.close()
                conn.close()
                
                st.success(f"Budget item {'updated' if editing_id else 'created'} successfully")
                
                # Reset and go back to list view
                if 'editing_id' in st.session_state:
                    del st.session_state.editing_id
                st.session_state.current_view = "list"
                st.rerun()
                
            except Exception as e:
                st.error(f"Error saving record: {str(e)}")
