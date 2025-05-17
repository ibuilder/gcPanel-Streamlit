import streamlit as st
import pandas as pd
from modules.base_module import BaseModule
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "Prime Contracts"
MODULE_ICON = "file-text"

# Define module columns
COLUMNS = [
    ('id', 'ID', 'integer'),
    ('contract_number', 'Contract #', 'text'),
    ('contract_title', 'Title', 'text'),
    ('contract_type', 'Type', 'text'),
    ('owner_name', 'Owner', 'text'),
    ('contractor_name', 'Contractor', 'text'),
    ('execution_date', 'Execution Date', 'date'),
    ('commencement_date', 'Commencement Date', 'date'),
    ('substantial_completion_date', 'Substantial Completion', 'date'),
    ('final_completion_date', 'Final Completion', 'date'),
    ('original_contract_sum', 'Original Contract Sum', 'float'),
    ('current_contract_sum', 'Current Contract Sum', 'float'),
    ('retainage_percentage', 'Retainage %', 'float'),
    ('status', 'Status', 'text'),
    ('description', 'Description', 'text')
]

# Define form fields
FORM_FIELDS = [
    ('id', 'ID', 'integer', False, None),
    ('contract_number', 'Contract #', 'text', True, None),
    ('contract_title', 'Title', 'text', True, None),
    ('contract_type', 'Type', 'select', True, ['GMP', 'Cost Plus', 'Lump Sum', 'CMAR', 'Design-Build']),
    ('owner_name', 'Owner', 'text', True, None),
    ('contractor_name', 'Contractor', 'text', True, None),
    ('execution_date', 'Execution Date', 'date', True, None),
    ('commencement_date', 'Commencement Date', 'date', True, None),
    ('substantial_completion_date', 'Substantial Completion', 'date', True, None),
    ('final_completion_date', 'Final Completion', 'date', False, None),
    ('original_contract_sum', 'Original Contract Sum', 'number', True, None),
    ('current_contract_sum', 'Current Contract Sum', 'number', True, None),
    ('retainage_percentage', 'Retainage %', 'number', True, None),
    ('status', 'Status', 'select', True, ['Draft', 'Issued', 'Executed', 'Active', 'Complete', 'Terminated']),
    ('description', 'Description', 'textarea', False, None)
]

# Create module instance
prime_contracts_module = BaseModule('prime_contracts', 'Prime Contracts', COLUMNS, FORM_FIELDS)

def render_list():
    """Render the list view"""
    prime_contracts_module.render_list()
    
    # Add contract summary
    st.subheader("Contract Summary")
    
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        # Get contract summary data
        summary_df = pd.read_sql_query("""
            SELECT 
                contract_type,
                COUNT(*) as count,
                SUM(original_contract_sum) as original_total,
                SUM(current_contract_sum) as current_total
            FROM prime_contracts
            GROUP BY contract_type
        """, conn)
        
        conn.close()
        
        if not summary_df.empty:
            # Format currency
            summary_df['original_total'] = summary_df['original_total'].apply(lambda x: f"${x:,.2f}")
            summary_df['current_total'] = summary_df['current_total'].apply(lambda x: f"${x:,.2f}")
            
            # Display summary
            st.dataframe(summary_df)
            
            # Calculate overall totals
            conn = get_db_connection()
            totals_df = pd.read_sql_query("""
                SELECT 
                    SUM(original_contract_sum) as original_total,
                    SUM(current_contract_sum) as current_total,
                    SUM(current_contract_sum - original_contract_sum) as change_amount,
                    (SUM(current_contract_sum) - SUM(original_contract_sum)) / NULLIF(SUM(original_contract_sum), 0) * 100 as change_percentage
                FROM prime_contracts
            """, conn)
            conn.close()
            
            # Display overall summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Original Contract Total", f"${totals_df['original_total'].iloc[0]:,.2f}")
            
            with col2:
                st.metric("Current Contract Total", f"${totals_df['current_total'].iloc[0]:,.2f}")
            
            with col3:
                change_amount = totals_df['change_amount'].iloc[0]
                change_percentage = totals_df['change_percentage'].iloc[0]
                st.metric("Change Amount", f"${change_amount:,.2f}", f"{change_percentage:.2f}%")
            
        else:
            st.info("No contract data available")
            
    except Exception as e:
        st.error(f"Error fetching contract summary data: {str(e)}")

def render_view():
    """Render the detail view"""
    prime_contracts_module.render_view()

def render_form():
    """Render the form view"""
    prime_contracts_module.render_form()
