import streamlit as st
import pandas as pd
from utils.database import get_db_connection
from utils.auth import check_permission
from utils.helpers import df_to_csv, create_download_link, generate_pdf_report
import io

class BaseModule:
    """Base class for all modules"""
    
    def __init__(self, table_name, display_name, columns, form_fields):
        self.table_name = table_name
        self.display_name = display_name
        self.columns = columns  # List of (name, display_name, type) tuples
        self.form_fields = form_fields  # List of (name, display_name, type, required, options) tuples
        
        # Initialize database table if it doesn't exist
        self._initialize_table()
    
    def _initialize_table(self):
        """Initialize the database table for this module"""
        try:
            conn = get_db_connection()
            if not conn:
                return
                
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} ("
            create_table_sql += "id SERIAL PRIMARY KEY,"
            
            for name, _, col_type in self.columns:
                if name != 'id':  # Skip ID column as it's already defined
                    if col_type == 'text':
                        sql_type = 'TEXT'
                    elif col_type == 'integer':
                        sql_type = 'INTEGER'
                    elif col_type == 'float':
                        sql_type = 'NUMERIC'
                    elif col_type == 'date':
                        sql_type = 'DATE'
                    elif col_type == 'boolean':
                        sql_type = 'BOOLEAN'
                    else:
                        sql_type = 'TEXT'
                    
                    create_table_sql += f"{name} {sql_type},"
            
            # Add audit fields
            create_table_sql += """
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_by INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_table_sql)
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            st.error(f"Error initializing table for {self.display_name}: {str(e)}")
    
    def render_list(self):
        """Render the list view of the module"""
        st.title(f"{self.display_name} List")
        
        # Check read permission
        if not check_permission('read'):
            st.error("You don't have permission to view this data")
            return
        
        # Fetch data from the database
        try:
            conn = get_db_connection()
            if not conn:
                return
                
            # Get column names for SELECT
            column_names = [col[0] for col in self.columns]
            columns_str = ', '.join(column_names)
            
            # Execute query
            query = f"SELECT {columns_str} FROM {self.table_name} ORDER BY id DESC"
            
            # Load into DataFrame
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            # Display data
            if df.empty:
                st.info(f"No {self.display_name} records found")
            else:
                # Rename columns for display
                column_map = {col[0]: col[1] for col in self.columns}
                df_display = df.rename(columns=column_map)
                
                # Show data
                st.dataframe(df_display)
                
                # Allow CSV download
                csv = df_to_csv(df_display)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{self.table_name}.csv",
                    mime="text/csv"
                )
                
                # Allow PDF report download
                if st.button("Generate PDF Report"):
                    pdf_buffer = generate_pdf_report(
                        f"{self.display_name} Report",
                        f"Report generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        df_display.head(100)  # Limit to prevent overly large PDFs
                    )
                    
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_buffer,
                        file_name=f"{self.table_name}_report.pdf",
                        mime="application/pdf"
                    )
            
            # Add new button
            if check_permission('create'):
                if st.button("Add New"):
                    st.session_state.current_view = "form"
                    st.session_state.editing_id = None
                    st.rerun()
            
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
    
    def render_view(self):
        """Render the detail view of a single record"""
        st.title(f"{self.display_name} Details")
        
        # Check read permission
        if not check_permission('read'):
            st.error("You don't have permission to view this data")
            return
        
        # Show a selector for the record
        try:
            conn = get_db_connection()
            if not conn:
                return
                
            cursor = conn.cursor()
            
            # Get a list of records for selection
            cursor.execute(f"SELECT id, {self.columns[1][0]} FROM {self.table_name} ORDER BY id DESC")
            records = cursor.fetchall()
            
            if not records:
                st.info(f"No {self.display_name} records found")
                return
            
            # Create a selection box
            record_options = {f"{r[0]} - {r[1]}": r[0] for r in records}
            selected_record = st.selectbox(
                f"Select {self.display_name}",
                options=list(record_options.keys())
            )
            
            selected_id = record_options[selected_record]
            
            # Get the complete record
            column_names = [col[0] for col in self.columns]
            columns_str = ', '.join(column_names)
            
            cursor.execute(f"SELECT {columns_str} FROM {self.table_name} WHERE id = %s", (selected_id,))
            record = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if record:
                # Display the record
                st.subheader(f"{self.display_name} #{record[0]}")
                
                # Create columns for layout
                col1, col2 = st.columns(2)
                
                # Display fields in two columns
                fields = list(zip(self.columns, record))
                half = len(fields) // 2
                
                for i, ((name, display_name, _), value) in enumerate(fields):
                    if i < half:
                        with col1:
                            st.markdown(f"**{display_name}:**")
                            st.write(value)
                    else:
                        with col2:
                            st.markdown(f"**{display_name}:**")
                            st.write(value)
                
                # Action buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if check_permission('update'):
                        if st.button("Edit"):
                            st.session_state.current_view = "form"
                            st.session_state.editing_id = selected_id
                            st.rerun()
                
                with col2:
                    if check_permission('delete'):
                        if st.button("Delete"):
                            # Confirm deletion
                            st.warning("Are you sure you want to delete this record?")
                            if st.button("Confirm Delete"):
                                try:
                                    conn = get_db_connection()
                                    cursor = conn.cursor()
                                    cursor.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (selected_id,))
                                    conn.commit()
                                    cursor.close()
                                    conn.close()
                                    st.success("Record deleted successfully")
                                    st.session_state.current_view = "list"
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error deleting record: {str(e)}")
            
        except Exception as e:
            st.error(f"Error loading record: {str(e)}")
    
    def render_form(self):
        """Render the form for creating or editing a record"""
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
            st.title(f"Edit {self.display_name}")
        else:
            st.title(f"New {self.display_name}")
        
        # If editing, fetch the current record
        current_values = {}
        if editing_id:
            try:
                conn = get_db_connection()
                if not conn:
                    return
                    
                cursor = conn.cursor()
                
                # Get column names for SELECT
                column_names = [col[0] for col in self.columns]
                columns_str = ', '.join(column_names)
                
                cursor.execute(f"SELECT {columns_str} FROM {self.table_name} WHERE id = %s", (editing_id,))
                record = cursor.fetchone()
                
                cursor.close()
                conn.close()
                
                if record:
                    # Create a dictionary of current values
                    current_values = {col[0]: val for col, val in zip(self.columns, record)}
                else:
                    st.error("Record not found")
                    return
                    
            except Exception as e:
                st.error(f"Error loading record for editing: {str(e)}")
                return
        
        # Create the form
        with st.form(f"{self.table_name}_form"):
            # Create form fields
            form_data = {}
            
            # Create columns for layout
            col1, col2 = st.columns(2)
            
            # Display fields in two columns
            half = len(self.form_fields) // 2
            
            for i, (name, display_name, field_type, required, options) in enumerate(self.form_fields):
                # Skip ID field when creating a new record
                if name == 'id' and not editing_id:
                    continue
                
                # Get the current value if editing
                current_value = current_values.get(name, None)
                
                # Display field in the appropriate column
                with col1 if i < half else col2:
                    if field_type == 'text':
                        form_data[name] = st.text_input(
                            f"{display_name}{' *' if required else ''}",
                            value=current_value or "",
                            key=f"form_{name}"
                        )
                    elif field_type == 'textarea':
                        form_data[name] = st.text_area(
                            f"{display_name}{' *' if required else ''}",
                            value=current_value or "",
                            key=f"form_{name}"
                        )
                    elif field_type == 'number':
                        form_data[name] = st.number_input(
                            f"{display_name}{' *' if required else ''}",
                            value=float(current_value) if current_value is not None else 0.0,
                            key=f"form_{name}"
                        )
                    elif field_type == 'integer':
                        form_data[name] = st.number_input(
                            f"{display_name}{' *' if required else ''}",
                            value=int(current_value) if current_value is not None else 0,
                            step=1,
                            key=f"form_{name}"
                        )
                    elif field_type == 'date':
                        form_data[name] = st.date_input(
                            f"{display_name}{' *' if required else ''}",
                            value=pd.to_datetime(current_value).date() if current_value else None,
                            key=f"form_{name}"
                        )
                    elif field_type == 'boolean':
                        form_data[name] = st.checkbox(
                            f"{display_name}",
                            value=current_value or False,
                            key=f"form_{name}"
                        )
                    elif field_type == 'select':
                        form_data[name] = st.selectbox(
                            f"{display_name}{' *' if required else ''}",
                            options=options,
                            index=options.index(current_value) if current_value in options else 0,
                            key=f"form_{name}"
                        )
                    elif field_type == 'multiselect':
                        form_data[name] = st.multiselect(
                            f"{display_name}{' *' if required else ''}",
                            options=options,
                            default=current_value or [],
                            key=f"form_{name}"
                        )
                    elif field_type == 'file':
                        # File handling is more complex, for simplicity we're not implementing it fully
                        st.file_uploader(
                            f"{display_name}{' *' if required else ''}",
                            key=f"form_{name}"
                        )
                        form_data[name] = current_value or ""
            
            # Submit button
            submit_text = "Update" if editing_id else "Create"
            submitted = st.form_submit_button(submit_text)
            
            if submitted:
                # Validate required fields
                missing_fields = []
                for name, display_name, _, required, _ in self.form_fields:
                    if required and not form_data.get(name):
                        missing_fields.append(display_name)
                
                if missing_fields:
                    st.error(f"Please fill in the following required fields: {', '.join(missing_fields)}")
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
                            
                            for name in form_data:
                                if name != 'id':  # Skip ID field for update
                                    update_fields.append(f"{name} = %s")
                                    update_values.append(form_data[name])
                            
                            # Add audit fields
                            update_fields.append("updated_by = %s")
                            update_values.append(st.session_state.get('user_id'))
                            update_fields.append("updated_at = CURRENT_TIMESTAMP")
                            
                            # Add ID for WHERE clause
                            update_values.append(editing_id)
                            
                            update_sql = f"UPDATE {self.table_name} SET {', '.join(update_fields)} WHERE id = %s"
                            cursor.execute(update_sql, update_values)
                            
                        else:
                            # Insert new record
                            field_names = []
                            field_placeholders = []
                            field_values = []
                            
                            for name in form_data:
                                if name != 'id':  # Skip ID field for insert
                                    field_names.append(name)
                                    field_placeholders.append("%s")
                                    field_values.append(form_data[name])
                            
                            # Add audit fields
                            field_names.append("created_by")
                            field_placeholders.append("%s")
                            field_values.append(st.session_state.get('user_id'))
                            
                            # Create SQL
                            insert_sql = f"INSERT INTO {self.table_name} ({', '.join(field_names)}) VALUES ({', '.join(field_placeholders)})"
                            cursor.execute(insert_sql, field_values)
                        
                        conn.commit()
                        cursor.close()
                        conn.close()
                        
                        st.success(f"{self.display_name} {'updated' if editing_id else 'created'} successfully")
                        
                        # Reset and go back to list view
                        if 'editing_id' in st.session_state:
                            del st.session_state.editing_id
                        st.session_state.current_view = "list"
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error saving record: {str(e)}")
