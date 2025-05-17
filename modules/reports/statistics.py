import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime, timedelta
from utils.database import get_db_connection, get_sqlalchemy_engine
from utils.auth import check_permission
from utils.helpers import generate_pdf_report

# Module metadata
MODULE_DISPLAY_NAME = "Statistics & Reports"
MODULE_ICON = "bar-chart-2"

def render_list():
    """Render the statistics and reports list view"""
    st.title("Statistics & Reports")
    
    # Check permission
    if not check_permission('read'):
        st.error("You don't have permission to view reports")
        return
    
    # Get database connection
    conn = get_db_connection()
    if not conn:
        st.error("Database connection is not available. Please configure the database settings.")
        return
    
    # Create tabs for different report categories
    tab1, tab2, tab3, tab4 = st.tabs(["Project Overview", "Module Activity", "User Activity", "Custom Reports"])
    
    with tab1:
        render_project_overview()
    
    with tab2:
        render_module_activity()
    
    with tab3:
        render_user_activity()
    
    with tab4:
        render_custom_reports()

def render_project_overview():
    """Render project overview statistics"""
    st.subheader("Project Overview")
    
    try:
        # Get database connection
        conn = get_db_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Get project info
        cursor.execute("""
            SELECT key, value 
            FROM project_info 
            WHERE key IN ('project_name', 'project_start_date', 'project_end_date', 'project_value')
        """)
        
        project_info = {key: value for key, value in cursor.fetchall()}
        
        # Display project header
        project_name = project_info.get('project_name', 'Project')
        st.write(f"**Project:** {project_name}")
        
        # Create metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Count various entities
        try:
            # Get module counts
            tables = [
                ('rfi', 'RFIs'),
                ('daily_reports', 'Daily Reports'),
                ('safety_observations', 'Safety Observations'),
                ('prime_contracts', 'Contracts'),
                ('budget', 'Budget Items')
            ]
            
            for i, (table, label) in enumerate(tables):
                cursor.execute(f"""
                    SELECT COUNT(*) FROM information_schema.tables 
                    WHERE table_name = '{table}'
                """)
                
                table_exists = cursor.fetchone()[0] > 0
                
                if table_exists:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                else:
                    count = 0
                
                with [col1, col2, col3, col4][i % 4]:
                    st.metric(label=label, value=count)
        except Exception as e:
            st.error(f"Error counting modules: {str(e)}")
        
        # Project timeline
        st.subheader("Project Timeline")
        
        start_date = project_info.get('project_start_date', '')
        end_date = project_info.get('project_end_date', '')
        
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                today = datetime.now()
                
                total_days = (end - start).days
                elapsed_days = (today - start).days if today > start else 0
                
                if total_days > 0:
                    progress = min(100, max(0, (elapsed_days / total_days) * 100))
                    
                    # Display progress bar
                    st.progress(progress / 100)
                    st.write(f"**Project Progress:** {progress:.1f}% ({elapsed_days} days of {total_days} total days)")
                    
                    # Calculate days remaining
                    days_remaining = (end - today).days if end > today else 0
                    if days_remaining > 0:
                        st.write(f"**Days Remaining:** {days_remaining} days until completion")
                    else:
                        st.write("**Project is past scheduled completion date**")
            except Exception as e:
                st.error(f"Error calculating project timeline: {str(e)}")
        else:
            st.info("Project start and end dates not set. Configure them in Project Information.")
        
        # Recent activity
        st.subheader("Recent Activity")
        
        # Combine recent activity from multiple tables
        recent_activity = []
        
        for table in ['rfi', 'daily_reports', 'safety_observations', 'prime_contracts', 'budget']:
            try:
                cursor.execute(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = '{table}'
                    )
                """)
                
                if cursor.fetchone()[0]:
                    cursor.execute(f"""
                        SELECT 
                            '{table}' as source, 
                            id,
                            created_at
                        FROM {table}
                        ORDER BY created_at DESC
                        LIMIT 5
                    """)
                    
                    activity = cursor.fetchall()
                    recent_activity.extend(activity)
            except Exception:
                # Table may not exist yet
                pass
        
        # Sort by date
        recent_activity.sort(key=lambda x: x[2], reverse=True)
        
        if recent_activity:
            # Create a DataFrame
            activity_df = pd.DataFrame(
                recent_activity[:10],
                columns=['Module', 'ID', 'Timestamp']
            )
            
            # Format module names
            module_names = {
                'rfi': 'Request for Information',
                'daily_reports': 'Daily Report',
                'safety_observations': 'Safety Observation',
                'prime_contracts': 'Contract',
                'budget': 'Budget Item'
            }
            
            activity_df['Module'] = activity_df['Module'].apply(lambda x: module_names.get(x, x.replace('_', ' ').title()))
            activity_df['Timestamp'] = activity_df['Timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))
            
            st.dataframe(activity_df)
        else:
            st.info("No recent activity found")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        st.error(f"Error rendering project overview: {str(e)}")

def render_module_activity():
    """Render module activity statistics"""
    st.subheader("Module Activity")
    
    try:
        # Get database connection
        conn = get_db_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("""
            SELECT 
                table_name
            FROM 
                information_schema.tables
            WHERE 
                table_schema='public' AND 
                table_name NOT IN ('users', 'sessions', 'sections', 'modules', 'project_info')
            ORDER BY
                table_name
        """)
        
        tables = [table[0] for table in cursor.fetchall()]
        
        if not tables:
            st.info("No module data available yet")
            return
        
        # Allow selecting a module for detailed stats
        selected_module = st.selectbox(
            "Select Module", 
            options=tables,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        if selected_module:
            # Get record count by date
            cursor.execute(f"""
                SELECT 
                    DATE_TRUNC('day', created_at) as date,
                    COUNT(*) as count
                FROM 
                    {selected_module}
                GROUP BY 
                    DATE_TRUNC('day', created_at)
                ORDER BY 
                    date
            """)
            
            daily_counts = cursor.fetchall()
            
            if daily_counts:
                # Create DataFrame
                df = pd.DataFrame(daily_counts, columns=['Date', 'Count'])
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
                
                # Display chart
                st.subheader(f"{selected_module.replace('_', ' ').title()} - Records Created by Date")
                st.line_chart(df)
                
                # Get daily stats
                total_records = df['Count'].sum()
                
                # Calculate average records per day
                if len(df) > 0:
                    avg_records = total_records / len(df)
                else:
                    avg_records = 0
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Records", total_records)
                
                with col2:
                    st.metric("Days with Activity", len(df))
                
                with col3:
                    st.metric("Avg. Records per Day", f"{avg_records:.2f}")
                
                # Show raw data
                with st.expander("Show Raw Data"):
                    st.dataframe(df.reset_index())
                    
                    # Export options
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv = df.reset_index().to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"{selected_module}_activity.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        # Generate PDF
                        if st.button("Generate PDF Report"):
                            pdf_buffer = generate_pdf_report(
                                f"{selected_module.replace('_', ' ').title()} Activity Report",
                                f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                                df.reset_index()
                            )
                            
                            st.download_button(
                                label="Download PDF Report",
                                data=pdf_buffer,
                                file_name=f"{selected_module}_activity_report.pdf",
                                mime="application/pdf"
                            )
            else:
                st.info(f"No activity data found for {selected_module}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        st.error(f"Error rendering module activity: {str(e)}")

def render_user_activity():
    """Render user activity statistics"""
    st.subheader("User Activity")
    
    try:
        # Get database connection
        conn = get_db_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Get user counts
        cursor.execute("""
            SELECT 
                role,
                COUNT(*) as count
            FROM 
                users
            GROUP BY 
                role
            ORDER BY 
                count DESC
        """)
        
        role_counts = cursor.fetchall()
        
        if role_counts:
            # Create DataFrame
            roles_df = pd.DataFrame(role_counts, columns=['Role', 'Count'])
            
            # Display chart
            st.subheader("Users by Role")
            st.bar_chart(roles_df.set_index('Role'))
            
            # Display table
            st.dataframe(roles_df)
        
        # Get login activity
        cursor.execute("""
            SELECT 
                DATE_TRUNC('day', last_login) as login_date,
                COUNT(*) as count
            FROM 
                users
            WHERE 
                last_login IS NOT NULL
            GROUP BY 
                DATE_TRUNC('day', last_login)
            ORDER BY 
                login_date DESC
        """)
        
        login_counts = cursor.fetchall()
        
        if login_counts:
            # Create DataFrame
            login_df = pd.DataFrame(login_counts, columns=['Date', 'Logins'])
            login_df['Date'] = pd.to_datetime(login_df['Date'])
            login_df.set_index('Date', inplace=True)
            
            # Display chart
            st.subheader("User Logins by Date")
            st.line_chart(login_df)
            
            # Display table
            st.dataframe(login_df.reset_index())
            
            # Export options
            col1, col2 = st.columns(2)
            
            with col1:
                csv = login_df.reset_index().to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Login CSV",
                    data=csv,
                    file_name="user_logins.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Generate PDF
                if st.button("Generate User Activity PDF"):
                    # Combine both DataFrames into one report
                    report_content = f"User Activity Report\nGenerated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    report_content += "Users by Role:\n\n"
                    
                    pdf_buffer = generate_pdf_report(
                        "User Activity Report",
                        report_content,
                        login_df.reset_index()
                    )
                    
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_buffer,
                        file_name="user_activity_report.pdf",
                        mime="application/pdf"
                    )
        else:
            st.info("No user login activity found")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        st.error(f"Error rendering user activity: {str(e)}")

def render_custom_reports():
    """Render custom reports"""
    st.subheader("Custom Reports")
    
    # Get database connection
    engine = get_sqlalchemy_engine()
    if not engine:
        st.error("Database connection is not available. Please configure the database settings.")
        return
    
    # Create tabs for different custom reports
    report_tab1, report_tab2, report_tab3 = st.tabs(["Cost Reports", "Safety Reports", "Schedule Reports"])
    
    with report_tab1:
        st.subheader("Cost Reports")
        
        try:
            # Check if budget table exists
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'budget'
                )
            """)
            
            budget_exists = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            if budget_exists:
                # Generate cost report
                budget_df = pd.read_sql_query("""
                    SELECT 
                        division,
                        SUM(original_budget) as original_budget,
                        SUM(current_budget) as current_budget,
                        SUM(actual_costs) as actual_costs,
                        SUM(projected_costs) as projected_costs,
                        SUM(current_budget - projected_costs) as variance
                    FROM 
                        budget
                    GROUP BY 
                        division
                    ORDER BY 
                        division
                """, engine)
                
                # Add totals row
                totals = budget_df.sum(numeric_only=True)
                totals_df = pd.DataFrame([totals], index=['TOTAL'])
                budget_report = pd.concat([budget_df, totals_df])
                
                # Format currencies
                for col in ['original_budget', 'current_budget', 'actual_costs', 'projected_costs', 'variance']:
                    budget_report[col] = budget_report[col].apply(lambda x: f"${x:,.2f}")
                
                st.write("### Budget Summary by Division")
                st.dataframe(budget_report)
                
                # Export options
                col1, col2 = st.columns(2)
                
                with col1:
                    original_df = pd.read_sql_query("""
                        SELECT * FROM budget ORDER BY division, cost_code
                    """, engine)
                    
                    csv = original_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Complete Budget CSV",
                        data=csv,
                        file_name="budget_complete.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Generate PDF
                    if st.button("Generate Budget PDF Report"):
                        pdf_buffer = generate_pdf_report(
                            "Budget Summary Report",
                            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                            budget_report
                        )
                        
                        st.download_button(
                            label="Download Budget PDF Report",
                            data=pdf_buffer,
                            file_name="budget_summary_report.pdf",
                            mime="application/pdf"
                        )
            else:
                st.info("Budget module data not available")
        except Exception as e:
            st.error(f"Error generating cost report: {str(e)}")
    
    with report_tab2:
        st.subheader("Safety Reports")
        
        try:
            # Check if safety_observations table exists
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'safety_observations'
                )
            """)
            
            safety_exists = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            if safety_exists:
                # Generate safety report
                safety_df = pd.read_sql_query("""
                    SELECT 
                        observation_type,
                        severity,
                        status,
                        COUNT(*) as count
                    FROM 
                        safety_observations
                    GROUP BY 
                        observation_type, severity, status
                    ORDER BY 
                        observation_type, severity, status
                """, engine)
                
                st.write("### Safety Observations Summary")
                st.dataframe(safety_df)
                
                # Create pivot table
                pivot = pd.pivot_table(
                    safety_df,
                    values='count',
                    index=['observation_type'],
                    columns=['severity'],
                    aggfunc=np.sum,
                    fill_value=0
                )
                
                st.write("### Safety Observations by Type and Severity")
                st.dataframe(pivot)
                
                # Export options
                col1, col2 = st.columns(2)
                
                with col1:
                    original_df = pd.read_sql_query("""
                        SELECT * FROM safety_observations ORDER BY observation_date DESC
                    """, engine)
                    
                    csv = original_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Safety Observations CSV",
                        data=csv,
                        file_name="safety_observations.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Generate PDF
                    if st.button("Generate Safety PDF Report"):
                        pdf_buffer = generate_pdf_report(
                            "Safety Observations Report",
                            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                            safety_df
                        )
                        
                        st.download_button(
                            label="Download Safety PDF Report",
                            data=pdf_buffer,
                            file_name="safety_report.pdf",
                            mime="application/pdf"
                        )
            else:
                st.info("Safety module data not available")
        except Exception as e:
            st.error(f"Error generating safety report: {str(e)}")
    
    with report_tab3:
        st.subheader("Schedule Reports")
        
        try:
            # Get project timeline info
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if daily_reports table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'daily_reports'
                )
            """)
            
            daily_reports_exist = cursor.fetchone()[0]
            
            if daily_reports_exist:
                # Generate schedule report from daily reports
                daily_df = pd.read_sql_query("""
                    SELECT 
                        report_date,
                        workforce_count,
                        weather_conditions,
                        temperature_high,
                        temperature_low,
                        precipitation
                    FROM 
                        daily_reports
                    ORDER BY 
                        report_date
                """, engine)
                
                # Format dates
                daily_df['report_date'] = pd.to_datetime(daily_df['report_date'])
                
                # Workforce summary
                st.write("### Workforce Summary")
                
                # Calculate workforce metrics
                if not daily_df.empty:
                    avg_workforce = daily_df['workforce_count'].mean()
                    max_workforce = daily_df['workforce_count'].max()
                    total_man_days = daily_df['workforce_count'].sum()
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Avg. Workforce", f"{avg_workforce:.1f}")
                    
                    with col2:
                        st.metric("Max Workforce", max_workforce)
                    
                    with col3:
                        st.metric("Total Man-Days", total_man_days)
                    
                    # Plot workforce chart
                    st.write("### Workforce History")
                    workforce_chart = daily_df.set_index('report_date')[['workforce_count']]
                    st.line_chart(workforce_chart)
                    
                    # Export options
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv = daily_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Daily Reports CSV",
                            data=csv,
                            file_name="daily_reports.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        # Generate PDF
                        if st.button("Generate Schedule PDF Report"):
                            pdf_buffer = generate_pdf_report(
                                "Project Schedule Report",
                                f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                                daily_df
                            )
                            
                            st.download_button(
                                label="Download Schedule PDF Report",
                                data=pdf_buffer,
                                file_name="schedule_report.pdf",
                                mime="application/pdf"
                            )
                else:
                    st.info("No daily reports data available")
            else:
                st.info("Daily reports module data not available")
                
            cursor.close()
            conn.close()
            
        except Exception as e:
            st.error(f"Error generating schedule report: {str(e)}")

def render_view():
    """Render a specific report view"""
    # For now, we'll just redirect to the list view
    # In a real application, we would implement specific report views
    render_list()

def render_form():
    """Render the form for creating a custom report"""
    st.title("Create Custom Report")
    
    # Check permission
    if not check_permission('create'):
        st.error("You don't have permission to create reports")
        return
    
    # Get database connection
    engine = get_sqlalchemy_engine()
    if not engine:
        st.error("Database connection is not available. Please configure the database settings.")
        return
    
    # Get available tables
    try:
        # Get database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("""
            SELECT 
                table_name
            FROM 
                information_schema.tables
            WHERE 
                table_schema='public' AND 
                table_name NOT IN ('users', 'sessions', 'sections', 'modules', 'project_info')
            ORDER BY
                table_name
        """)
        
        tables = [table[0] for table in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        if not tables:
            st.info("No module data available yet")
            return
        
        # Create report builder form
        with st.form("custom_report_form"):
            # Select table
            selected_table = st.selectbox(
                "Select Table/Module", 
                options=tables,
                format_func=lambda x: x.replace('_', ' ').title()
            )
            
            # Get columns for selected table
            if selected_table:
                # Get columns
                columns_df = pd.read_sql_query(f"""
                    SELECT 
                        column_name,
                        data_type
                    FROM 
                        information_schema.columns
                    WHERE 
                        table_name = '{selected_table}'
                    ORDER BY 
                        ordinal_position
                """, engine)
                
                column_options = columns_df['column_name'].tolist()
                
                # Select columns
                selected_columns = st.multiselect(
                    "Select Columns",
                    options=column_options,
                    default=column_options[:5]  # Default to first 5 columns
                )
                
                # Date range filter (if date columns exist)
                date_columns = columns_df[columns_df['data_type'].str.contains('date|time')]['column_name'].tolist()
                
                if date_columns:
                    # Allow date filtering
                    use_date_filter = st.checkbox("Filter by Date")
                    
                    if use_date_filter:
                        # Select date column
                        date_column = st.selectbox(
                            "Date Column",
                            options=date_columns
                        )
                        
                        # Date range
                        col1, col2 = st.columns(2)
                        with col1:
                            start_date = st.date_input(
                                "Start Date",
                                value=(datetime.now() - timedelta(days=30)).date()
                            )
                        
                        with col2:
                            end_date = st.date_input(
                                "End Date",
                                value=datetime.now().date()
                            )
                    else:
                        date_column = None
                        start_date = None
                        end_date = None
                else:
                    use_date_filter = False
                    date_column = None
                    start_date = None
                    end_date = None
                
                # Sorting
                sort_column = st.selectbox(
                    "Sort By",
                    options=column_options,
                    index=0
                )
                
                sort_direction = st.radio(
                    "Sort Direction",
                    options=["Ascending", "Descending"],
                    index=1
                )
                
                # Export format
                export_format = st.radio(
                    "Export Format",
                    options=["Display Only", "CSV", "PDF"],
                    index=0
                )
                
                # Report title
                report_title = st.text_input(
                    "Report Title",
                    value=f"{selected_table.replace('_', ' ').title()} Report"
                )
            
            submitted = st.form_submit_button("Generate Report")
            
            if submitted and selected_table and selected_columns:
                # Build query
                columns_str = ", ".join(selected_columns)
                query = f"SELECT {columns_str} FROM {selected_table}"
                
                # Add date filter if enabled
                if use_date_filter and date_column and start_date and end_date:
                    query += f" WHERE {date_column} BETWEEN '{start_date}' AND '{end_date}'"
                
                # Add sorting
                query += f" ORDER BY {sort_column} {'DESC' if sort_direction == 'Descending' else 'ASC'}"
                
                # Execute query
                result_df = pd.read_sql_query(query, engine)
                
                # Display results
                st.write(f"### {report_title}")
                st.write(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                st.dataframe(result_df)
                
                # Export if requested
                if export_format == "CSV":
                    csv = result_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download CSV Report",
                        data=csv,
                        file_name=f"{selected_table}_report.csv",
                        mime="text/csv"
                    )
                elif export_format == "PDF":
                    pdf_buffer = generate_pdf_report(
                        report_title,
                        f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        result_df
                    )
                    
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_buffer,
                        file_name=f"{selected_table}_report.pdf",
                        mime="application/pdf"
                    )
        
    except Exception as e:
        st.error(f"Error creating custom report: {str(e)}")
