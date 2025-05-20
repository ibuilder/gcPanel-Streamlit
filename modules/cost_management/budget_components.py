"""
Budget components for the Cost Management module.

This module provides the UI components for budget management including:
- Budget list view
- Budget details view
- Budget form (add/edit)
- Budget analysis view
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Sample data for demonstration
def generate_sample_budgets():
    """Generate sample budget data for demonstration"""
    return [
        {
            "ID": "BDG-2025-001",
            "Title": "Foundation Work",
            "Project": "Highland Tower",
            "Cost Code": "03-3000",
            "Original": 1850000,
            "Current": 1900000,
            "Spent": 1110000,
            "Remaining": 790000,
            "Status": "Active"
        },
        {
            "ID": "BDG-2025-002",
            "Title": "Structural Steel",
            "Project": "Highland Tower",
            "Cost Code": "05-1000",
            "Original": 2100000,
            "Current": 2100000,
            "Spent": 1260000,
            "Remaining": 840000,
            "Status": "Active"
        },
        {
            "ID": "BDG-2025-003",
            "Title": "Electrical Systems",
            "Project": "Highland Tower",
            "Cost Code": "16-1000",
            "Original": 1860000,
            "Current": 1910000,
            "Spent": 744000,
            "Remaining": 1166000,
            "Status": "Active"
        },
        {
            "ID": "BDG-2025-004",
            "Title": "Mechanical Systems",
            "Project": "Highland Tower",
            "Cost Code": "15-1000",
            "Original": 2325000,
            "Current": 2375000,
            "Spent": 930000,
            "Remaining": 1445000,
            "Status": "Active"
        },
        {
            "ID": "BDG-2025-005",
            "Title": "Finishes",
            "Project": "Highland Tower",
            "Cost Code": "09-1000",
            "Original": 1550000,
            "Current": 1550000,
            "Spent": 155000,
            "Remaining": 1395000,
            "Status": "Active"
        },
        {
            "ID": "BDG-2025-006",
            "Title": "Site Preparation",
            "Project": "City Center",
            "Cost Code": "02-2000",
            "Original": 600000,
            "Current": 600000,
            "Spent": 600000,
            "Remaining": 0,
            "Status": "Complete"
        },
        {
            "ID": "BDG-2025-007",
            "Title": "Foundation Work",
            "Project": "Riverside Apartments",
            "Cost Code": "03-3000",
            "Original": 800000,
            "Current": 800000,
            "Spent": 800000,
            "Remaining": 0,
            "Status": "Complete"
        }
    ]

def render_budget_list():
    """Render the budget list view with filtering and sorting"""
    st.subheader("Budget Items")
    
    # Get sample data
    budgets = generate_sample_budgets()
    
    with st.expander("Filters", expanded=True):
        # Create two columns for the filters
        col1, col2 = st.columns(2)
        
        with col1:
            # Project filter
            projects = ["All Projects"] + list(set(b["Project"] for b in budgets))
            selected_project = st.selectbox("Project", projects, key="budget_project_filter")
            
            # Status filter
            statuses = ["All Statuses"] + list(set(b["Status"] for b in budgets))
            selected_status = st.selectbox("Status", statuses, key="budget_status_filter")
        
        with col2:
            # Cost code filter
            cost_codes = ["All Cost Codes"] + list(set(b["Cost Code"] for b in budgets))
            selected_cost_code = st.selectbox("Cost Code", cost_codes, key="budget_costcode_filter")
            
            # Search field
            search_term = st.text_input("Search", key="budget_search", placeholder="Search budgets...")
    
    # Filter the data based on selections
    filtered_budgets = budgets
    
    if selected_project != "All Projects":
        filtered_budgets = [b for b in filtered_budgets if b["Project"] == selected_project]
    
    if selected_status != "All Statuses":
        filtered_budgets = [b for b in filtered_budgets if b["Status"] == selected_status]
    
    if selected_cost_code != "All Cost Codes":
        filtered_budgets = [b for b in filtered_budgets if b["Cost Code"] == selected_cost_code]
    
    if search_term:
        filtered_budgets = [b for b in filtered_budgets if 
                           search_term.lower() in b["Title"].lower() or 
                           search_term.lower() in b["ID"].lower()]

    # Add button
    if st.button("➕ Add Budget Item", use_container_width=True):
        st.session_state.cost_view = "add"
        st.rerun()
    
    # Check if we have any results
    if not filtered_budgets:
        st.info("No budget items match your filters.")
        return
    
    # Show item count
    st.caption(f"Showing {len(filtered_budgets)} budget items")
    
    # Display the filtered budgets
    for budget in filtered_budgets:
        # Create a container for each budget item
        budget_container = st.container()
        
        with budget_container:
            # Create a styled container with border
            st.markdown("""
            <style>
                .budget-item {
                    border: 1px solid #e0e0e0;
                    border-radius: 5px;
                    padding: 10px;
                    margin-bottom: 10px;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Start the custom container
            st.markdown('<div class="budget-item">', unsafe_allow_html=True)
            
            # Create columns for the data display
            col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
            
            with col1:
                st.write(f"**{budget['ID']}**")
                st.caption(f"Project: {budget['Project']}")
            
            with col2:
                st.write(f"📋 **{budget['Title']}**")
                st.caption(f"Cost Code: {budget['Cost Code']}")
            
            with col3:
                st.write(f"**Current Budget:**")
                st.write(f"${budget['Current']:,.0f}")
            
            with col4:
                progress_percentage = int((budget['Spent'] / budget['Current']) * 100) if budget['Current'] > 0 else 0
                
                # Determine color based on percentage
                if progress_percentage > 90:
                    color = "red"
                elif progress_percentage > 75:
                    color = "orange"
                else:
                    color = "green"
                
                st.write(f"**Spent: ${budget['Spent']:,.0f}**")
                st.progress(progress_percentage / 100)
            
            # Add a row for buttons below each budget
            button_cols = st.columns([4, 2, 2])
            
            with button_cols[1]:
                # View button
                if st.button("👁️ View Details", key=f"view_{budget['ID']}", use_container_width=True):
                    # Store budget details in session state
                    st.session_state.selected_budget_id = budget['ID']
                    st.session_state.selected_budget_data = budget
                    # Set view mode
                    st.session_state["cost_view"] = "view"
                    # Force refresh
                    st.rerun()
            
            with button_cols[2]:
                # Edit button
                if st.button("✏️ Edit", key=f"edit_{budget['ID']}", use_container_width=True):
                    # Store budget data for editing
                    st.session_state.edit_budget_id = budget['ID']
                    st.session_state.edit_budget_data = budget
                    # Set edit mode
                    st.session_state["cost_view"] = "edit"
                    # Force refresh
                    st.rerun()
            
            # End the custom container
            st.markdown('</div>', unsafe_allow_html=True)


def render_budget_details():
    """Render the budget details view (single record view)"""
    st.subheader("Budget Details")
    
    # Ensure we have a selected budget
    if not st.session_state.get("selected_budget_id"):
        st.error("No budget selected. Please select a budget from the list.")
        # Return to list view
        st.session_state.cost_view = "list"
        st.rerun()
        return
    
    # Get the selected budget data
    budget = st.session_state.get("selected_budget_data", None)
    
    if not budget:
        # If somehow we have an ID but no data, try to find it
        budgets = generate_sample_budgets()
        budget = next((b for b in budgets if b["ID"] == st.session_state.selected_budget_id), None)
        
        if not budget:
            st.error(f"Budget with ID {st.session_state.selected_budget_id} not found.")
            # Return to list view
            st.session_state.cost_view = "list"
            st.rerun()
            return
    
    # Display budget details
    with st.container():
        # Style for budget details
        st.markdown("""
        <style>
            .budget-details {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            .budget-header {
                margin-bottom: 20px;
            }
            .budget-section {
                margin-top: 15px;
                margin-bottom: 15px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Start budget details container
        st.markdown('<div class="budget-details">', unsafe_allow_html=True)
        
        # Header section
        st.markdown(f'<div class="budget-header">', unsafe_allow_html=True)
        st.markdown(f"# {budget['Title']}")
        st.markdown(f"#### ID: {budget['ID']} | Project: {budget['Project']} | Status: {budget['Status']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Budget information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<div class="budget-section">', unsafe_allow_html=True)
            st.markdown("### Budget Values")
            st.markdown(f"**Original Budget:** ${budget['Original']:,.0f}")
            st.markdown(f"**Current Budget:** ${budget['Current']:,.0f}")
            
            # Calculate if over/under original
            if budget['Current'] > budget['Original']:
                difference = budget['Current'] - budget['Original']
                st.markdown(f"**Change from Original:** <span style='color:red'>+${difference:,.0f}</span>", unsafe_allow_html=True)
            elif budget['Current'] < budget['Original']:
                difference = budget['Original'] - budget['Current']
                st.markdown(f"**Change from Original:** <span style='color:green'>-${difference:,.0f}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"**Change from Original:** $0")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="budget-section">', unsafe_allow_html=True)
            st.markdown("### Spend Status")
            st.markdown(f"**Spent to Date:** ${budget['Spent']:,.0f}")
            st.markdown(f"**Remaining:** ${budget['Remaining']:,.0f}")
            
            # Calculate percentage spent
            percent_spent = (budget['Spent'] / budget['Current']) * 100 if budget['Current'] > 0 else 0
            st.markdown(f"**Percent Spent:** {percent_spent:.1f}%")
            
            # Progress bar
            if percent_spent > 90:
                color = "red"
            elif percent_spent > 75:
                color = "orange"
            else:
                color = "green"
                
            # Custom progress bar
            st.markdown(
                f"""
                <div style="width:100%; background-color:#eee; height:20px; border-radius:10px; margin-top:10px;">
                    <div style="width:{percent_spent}%; background-color:{color}; height:20px; border-radius:10px;">
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Historical spending (placeholder)
        st.markdown(f'<div class="budget-section">', unsafe_allow_html=True)
        st.markdown("### Monthly Spending")
        
        # Generate some random monthly data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_budget = [budget['Current']/12 for _ in range(12)]
        
        # Create some random spending data that adds up to the spent amount
        total_spent = budget['Spent']
        monthly_spent = []
        
        # Generate random values for past months (assuming we're in May)
        for i in range(5):  # Jan to May
            if i < 4:  # Jan to Apr
                if total_spent > 0:
                    spent = random.uniform(0.1, 0.3) * total_spent
                    total_spent -= spent
                    monthly_spent.append(spent)
                else:
                    monthly_spent.append(0)
            else:  # May
                monthly_spent.append(total_spent)
        
        # Future months have no spending yet
        monthly_spent.extend([0] * 7)  # Jun to Dec
        
        # Create a DataFrame for the chart
        monthly_data = pd.DataFrame({
            'Month': months,
            'Budget': monthly_budget,
            'Actual': monthly_spent
        })
        
        # Plot the chart
        st.line_chart(monthly_data.set_index('Month'))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Actions
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Edit Budget", use_container_width=True):
                st.session_state.edit_budget_id = budget['ID']
                st.session_state.edit_budget_data = budget
                st.session_state.cost_view = "edit"
                st.rerun()
        
        with col2:
            if st.button("📊 View Analysis", use_container_width=True):
                st.session_state.cost_view = "analysis"
                st.rerun()
        
        # End the budget details container
        st.markdown('</div>', unsafe_allow_html=True)


def render_budget_form(is_edit=False):
    """Render the budget creation/edit form"""
    if is_edit:
        st.subheader("Edit Budget")
        # Ensure we have a budget to edit
        if not st.session_state.get("edit_budget_id"):
            st.error("No budget selected for editing. Please select a budget from the list.")
            # Return to list view
            st.session_state.cost_view = "list"
            st.rerun()
            return
        
        # Get the budget data for editing
        budget = st.session_state.get("edit_budget_data", {})
    else:
        st.subheader("Add New Budget Item")
        # Initialize empty budget for new entries
        budget = {
            "ID": f"BDG-{datetime.now().year}-{random.randint(100, 999)}",
            "Title": "",
            "Project": "Highland Tower",
            "Cost Code": "",
            "Original": 0,
            "Current": 0,
            "Spent": 0,
            "Remaining": 0,
            "Status": "Draft"
        }
    
    # Create the form
    with st.form(key="budget_form"):
        # Basic information
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title *", value=budget.get("Title", ""))
            
            # Project dropdown
            projects = ["Highland Tower", "City Center", "Riverside Apartments", "Metro Office Complex"]
            selected_project = st.selectbox(
                "Project *", 
                projects, 
                index=projects.index(budget.get("Project")) if budget.get("Project") in projects else 0
            )
        
        with col2:
            # For display only
            if is_edit:
                st.text_input("Budget ID", value=budget.get("ID", ""), disabled=True)
            
            # Cost code dropdown
            cost_codes = ["01-1000", "02-2000", "03-3000", "05-1000", "07-1000", "08-1000", "09-1000", "15-1000", "16-1000"]
            selected_cost_code = st.selectbox(
                "Cost Code *",
                cost_codes,
                index=cost_codes.index(budget.get("Cost Code")) if budget.get("Cost Code") in cost_codes else 0
            )
        
        # Financial information
        st.subheader("Financial Information")
        col1, col2 = st.columns(2)
        
        with col1:
            original_budget = st.number_input(
                "Original Budget ($) *", 
                min_value=0, 
                value=int(budget.get("Original", 0))
            )
            
            current_budget = st.number_input(
                "Current Budget ($) *", 
                min_value=0, 
                value=int(budget.get("Current", 0))
            )
        
        with col2:
            spent = st.number_input(
                "Spent to Date ($)", 
                min_value=0, 
                value=int(budget.get("Spent", 0))
            )
            
            # Calculate remaining
            remaining = current_budget - spent
            st.number_input(
                "Remaining ($)",
                value=int(remaining),
                disabled=True
            )
        
        # Status
        status_options = ["Draft", "Active", "Complete", "On Hold"]
        selected_status = st.selectbox(
            "Status *",
            status_options,
            index=status_options.index(budget.get("Status")) if budget.get("Status") in status_options else 0
        )
        
        # Notes (optional)
        notes = st.text_area("Notes", value=budget.get("Notes", ""), height=100)
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(
                "Save Budget" if is_edit else "Create Budget",
                use_container_width=True
            )
        
        with col2:
            cancel_button = st.form_submit_button(
                "Cancel",
                use_container_width=True
            )
    
    # Handle form submission
    if submit_button:
        # Validate required fields
        if not title:
            st.error("Please enter a budget title.")
            return
        
        # In a real app, this would save to database
        if is_edit:
            st.success(f"Budget '{title}' updated successfully!")
        else:
            st.success(f"Budget '{title}' created successfully!")
        
        # Return to list view
        st.session_state.cost_view = "list"
        st.rerun()
    
    if cancel_button:
        # Return to previous view
        st.session_state.cost_view = "list"
        st.rerun()


def render_budget_analysis():
    """Render the budget analysis view with charts and metrics"""
    st.subheader("Budget Analysis")
    
    # Get sample data
    budgets = generate_sample_budgets()
    
    # Project selector
    projects = ["All Projects"] + list(set(b["Project"] for b in budgets))
    selected_project = st.selectbox("Select Project", projects, key="analysis_project_filter")
    
    # Filter by project if selected
    if selected_project != "All Projects":
        filtered_budgets = [b for b in budgets if b["Project"] == selected_project]
    else:
        filtered_budgets = budgets
    
    # Calculate summary metrics
    total_original = sum(b["Original"] for b in filtered_budgets)
    total_current = sum(b["Current"] for b in filtered_budgets)
    total_spent = sum(b["Spent"] for b in filtered_budgets)
    total_remaining = sum(b["Remaining"] for b in filtered_budgets)
    pct_spent = (total_spent / total_current) * 100 if total_current > 0 else 0
    
    # Summary metrics
    st.subheader("Budget Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Original Budget", f"${total_original:,.0f}")
    
    with col2:
        # Show the difference from original to current
        delta = total_current - total_original
        delta_pct = (delta / total_original) * 100 if total_original > 0 else 0
        delta_str = f"{delta_pct:+.1f}%" if delta != 0 else None
        st.metric("Total Current Budget", f"${total_current:,.0f}", delta_str)
    
    with col3:
        st.metric("Total Spent", f"${total_spent:,.0f}", f"{pct_spent:.1f}% of budget")
    
    with col4:
        st.metric("Total Remaining", f"${total_remaining:,.0f}")
    
    # Budget Distribution Charts
    st.subheader("Budget Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution by cost code
        cost_code_data = {}
        for budget in filtered_budgets:
            cost_code = budget["Cost Code"]
            if cost_code in cost_code_data:
                cost_code_data[cost_code] += budget["Current"]
            else:
                cost_code_data[cost_code] = budget["Current"]
        
        # Create a DataFrame for the chart
        cost_code_df = pd.DataFrame({
            'Cost Code': list(cost_code_data.keys()),
            'Budget': list(cost_code_data.values())
        })
        
        st.write("#### Distribution by Cost Code")
        st.bar_chart(cost_code_df.set_index('Cost Code'))
    
    with col2:
        # Spent vs Remaining
        st.write("#### Spent vs Remaining")
        
        budget_status = pd.DataFrame({
            'Status': ['Spent', 'Remaining'],
            'Amount': [total_spent, total_remaining]
        })
        
        st.bar_chart(budget_status.set_index('Status'))
    
    # Budget vs Actual Table
    st.subheader("Budget vs Actual by Item")
    
    # Create a table with variance information
    budget_table = []
    for budget in filtered_budgets:
        variance = budget["Current"] - budget["Spent"] - budget["Remaining"]
        pct_variance = (variance / budget["Current"]) * 100 if budget["Current"] > 0 else 0
        
        budget_table.append({
            "ID": budget["ID"],
            "Title": budget["Title"],
            "Project": budget["Project"],
            "Original": f"${budget['Original']:,.0f}",
            "Current": f"${budget['Current']:,.0f}",
            "Spent": f"${budget['Spent']:,.0f}",
            "Remaining": f"${budget['Remaining']:,.0f}",
            "Variance": f"${variance:,.0f}",
            "Variance %": f"{pct_variance:+.1f}%"
        })
    
    # Display the table
    st.dataframe(pd.DataFrame(budget_table), use_container_width=True)