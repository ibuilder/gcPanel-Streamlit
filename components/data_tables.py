"""
Data tables component for displaying tabular data with filtering and sorting.

This module provides interactive data tables with advanced features like filtering,
sorting, pagination, and export functionality.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional, Callable, Tuple, Union
import json
import base64
from datetime import datetime, date

def data_table(
    data: Union[pd.DataFrame, List[Dict[str, Any]]],
    columns: Optional[List[Dict[str, Any]]] = None,
    title: Optional[str] = None,
    height: Optional[int] = 400,
    filterable: bool = True,
    sortable: bool = True,
    paginate: bool = True,
    page_size: int = 10,
    exportable: bool = True,
    key: Optional[str] = None,
    on_row_click: Optional[Callable] = None
) -> Tuple[pd.DataFrame, Optional[Dict[str, Any]]]:
    """
    Display an interactive data table with filtering, sorting, and export capabilities.
    
    Args:
        data: DataFrame or list of dictionaries containing the data
        columns: Optional list of column configurations with keys 'field', 'title', 'width', etc.
        title: Optional table title
        height: Height of the table in pixels
        filterable: Whether to allow filtering
        sortable: Whether to allow sorting
        paginate: Whether to paginate the data
        page_size: Number of rows per page when paginated
        exportable: Whether to allow data export
        key: Unique key for the table component
        on_row_click: Callback function when a row is clicked
        
    Returns:
        Tuple of (filtered_data, selected_row)
    """
    # Generate a unique key if not provided
    if key is None:
        key = f"table_{id(data)}"
    
    # Convert to DataFrame if list of dictionaries
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data.copy()
    
    # Handle empty dataframe
    if df.empty:
        st.info("No data available to display.")
        return df, None
    
    # Determine columns if not provided
    if columns is None:
        columns = [{"field": col, "title": col.replace("_", " ").title()} for col in df.columns]
    
    # Display title if provided
    if title:
        st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
    
    # Create filter controls
    if filterable:
        with st.expander("Filters", expanded=False):
            # Create columns for filter controls, up to 3 per row
            max_cols = 3
            col_groups = [columns[i:i+max_cols] for i in range(0, len(columns), max_cols)]
            
            # Create filter widgets for each column group
            for col_group in col_groups:
                filter_cols = st.columns(len(col_group))
                
                for i, column in enumerate(col_group):
                    field = column["field"]
                    title = column.get("title", field.replace("_", " ").title())
                    
                    with filter_cols[i]:
                        # Create appropriate filter widget based on data type
                        if field in df.columns:
                            col_type = str(df[field].dtype)
                            
                            if "datetime" in col_type or "date" in col_type:
                                # Date range filter
                                min_date = df[field].min() if not pd.isna(df[field].min()) else None
                                max_date = df[field].max() if not pd.isna(df[field].max()) else None
                                
                                if min_date and max_date:
                                    filter_date = st.date_input(
                                        f"Filter by {title}",
                                        value=(min_date, max_date),
                                        key=f"{key}_filter_{field}"
                                    )
                                    
                                    if len(filter_date) == 2 and filter_date[0] and filter_date[1]:
                                        df = df[(df[field].dt.date >= filter_date[0]) & 
                                                (df[field].dt.date <= filter_date[1])]
                            
                            elif "float" in col_type or "int" in col_type:
                                # Numeric range filter
                                min_val = float(df[field].min()) if not pd.isna(df[field].min()) else 0
                                max_val = float(df[field].max()) if not pd.isna(df[field].max()) else 100
                                
                                filter_range = st.slider(
                                    f"Filter by {title}",
                                    min_value=min_val,
                                    max_value=max_val,
                                    value=(min_val, max_val),
                                    key=f"{key}_filter_{field}"
                                )
                                
                                if filter_range:
                                    df = df[(df[field] >= filter_range[0]) & (df[field] <= filter_range[1])]
                            
                            else:
                                # Text/categorical filter
                                unique_values = df[field].dropna().unique()
                                
                                if len(unique_values) <= 10:  # For fewer unique values, use multiselect
                                    options = ["All"] + sorted([str(x) for x in unique_values])
                                    selected_values = st.multiselect(
                                        f"Filter by {title}",
                                        options=options,
                                        default=["All"],
                                        key=f"{key}_filter_{field}"
                                    )
                                    
                                    if selected_values and "All" not in selected_values:
                                        df = df[df[field].isin(selected_values)]
                                else:  # For many unique values, use text input
                                    filter_text = st.text_input(
                                        f"Filter by {title}",
                                        "",
                                        key=f"{key}_filter_{field}"
                                    )
                                    
                                    if filter_text:
                                        df = df[df[field].astype(str).str.contains(filter_text, case=False, na=False)]
    
    # Create sort controls
    if sortable:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            sort_field = st.selectbox(
                "Sort by",
                [""] + [col["field"] for col in columns],
                key=f"{key}_sort_field"
            )
        
        with col2:
            sort_order = st.selectbox(
                "Order",
                ["Ascending", "Descending"],
                key=f"{key}_sort_order"
            )
        
        if sort_field:
            ascending = sort_order == "Ascending"
            df = df.sort_values(by=sort_field, ascending=ascending)
    
    # Paginate the data
    if paginate and len(df) > page_size:
        total_pages = (len(df) + page_size - 1) // page_size
        
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            page = st.slider(
                "Page",
                min_value=1,
                max_value=max(1, total_pages),
                value=1,
                key=f"{key}_page"
            )
        
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, len(df))
        
        display_df = df.iloc[start_idx:end_idx].copy()
        st.write(f"Showing {start_idx + 1} to {end_idx} of {len(df)} entries")
    else:
        display_df = df.copy()
    
    # Apply formatting to the displayed dataframe
    formatted_df = format_dataframe(display_df, columns)
    
    # Display the table
    st.dataframe(
        formatted_df,
        height=height,
        use_container_width=True,
        key=f"{key}_dataframe"
    )
    
    # Export controls
    if exportable:
        col1, col2 = st.columns([1, 4])
        
        with col1:
            export_format = st.selectbox(
                "Export format",
                ["CSV", "Excel", "JSON"],
                key=f"{key}_export_format"
            )
        
        with col2:
            export_filename = st.text_input(
                "Filename",
                f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                key=f"{key}_export_filename"
            )
        
        if st.button("Export Data", key=f"{key}_export"):
            # Prepare data for export
            if export_format == "CSV":
                export_data = df.to_csv(index=False)
                mime_type = "text/csv"
                file_extension = "csv"
            elif export_format == "Excel":
                # Create Excel file in memory
                from io import BytesIO
                output = BytesIO()
                df.to_excel(output, index=False)
                export_data = output.getvalue()
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                file_extension = "xlsx"
            else:  # JSON
                export_data = df.to_json(orient="records", date_format="iso")
                mime_type = "application/json"
                file_extension = "json"
            
            # Create download link
            if export_format == "Excel":
                b64 = base64.b64encode(export_data).decode()
            else:
                b64 = base64.b64encode(export_data.encode()).decode()
            
            filename = f"{export_filename}.{file_extension}"
            href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">Download {export_format} file</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    # Row selection handling
    selected_row = None
    if on_row_click and not display_df.empty:
        # Create row selector
        row_indices = [f"Row {i+1}" for i in range(len(display_df))]
        selected_index = st.selectbox(
            "Select a row to view details",
            [""] + row_indices,
            key=f"{key}_row_selector"
        )
        
        if selected_index and selected_index != "":
            idx = int(selected_index.replace("Row ", "")) - 1
            selected_row = display_df.iloc[idx].to_dict()
            on_row_click(selected_row)
    
    return df, selected_row

def format_dataframe(df: pd.DataFrame, columns: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Format a DataFrame for display based on column configuration.
    
    Args:
        df: The DataFrame to format
        columns: List of column configurations
        
    Returns:
        Formatted DataFrame
    """
    formatted_df = df.copy()
    
    for column in columns:
        field = column["field"]
        
        if field in formatted_df.columns:
            # Apply formatting based on data type and column config
            dtype = str(formatted_df[field].dtype)
            
            # Format date/datetime columns
            if "datetime" in dtype or "date" in dtype:
                date_format = column.get("format", "%Y-%m-%d")
                formatted_df[field] = formatted_df[field].dt.strftime(date_format)
            
            # Format numeric columns
            elif "float" in dtype:
                precision = column.get("precision", 2)
                prefix = column.get("prefix", "")
                suffix = column.get("suffix", "")
                
                # Apply numeric formatting
                if "currency" in column and column["currency"]:
                    formatted_df[field] = formatted_df[field].apply(
                        lambda x: f"{prefix}${x:,.{precision}f}{suffix}" if pd.notna(x) else ""
                    )
                else:
                    formatted_df[field] = formatted_df[field].apply(
                        lambda x: f"{prefix}{x:,.{precision}f}{suffix}" if pd.notna(x) else ""
                    )
            
            # Format integer columns
            elif "int" in dtype:
                prefix = column.get("prefix", "")
                suffix = column.get("suffix", "")
                
                # Apply integer formatting
                if "currency" in column and column["currency"]:
                    formatted_df[field] = formatted_df[field].apply(
                        lambda x: f"{prefix}${x:,}{suffix}" if pd.notna(x) else ""
                    )
                else:
                    formatted_df[field] = formatted_df[field].apply(
                        lambda x: f"{prefix}{x:,}{suffix}" if pd.notna(x) else ""
                    )
            
            # Apply custom formatter if provided
            elif "formatter" in column and callable(column["formatter"]):
                formatted_df[field] = formatted_df[field].apply(column["formatter"])
    
    return formatted_df


def get_downloadable_link(df: pd.DataFrame, filename: str, format_type: str = "csv") -> str:
    """
    Generate a downloadable link for a DataFrame.
    
    Args:
        df: The DataFrame to download
        filename: The base filename (without extension)
        format_type: The export format (csv, excel, json)
        
    Returns:
        HTML string with download link
    """
    if format_type.lower() == "csv":
        data = df.to_csv(index=False)
        b64 = base64.b64encode(data.encode()).decode()
        mime_type = "text/csv"
        file_extension = "csv"
    elif format_type.lower() == "excel":
        # Create Excel file in memory
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        excel_data = output.read()
        b64 = base64.b64encode(excel_data).decode()
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        file_extension = "xlsx"
    elif format_type.lower() == "json":
        data = df.to_json(orient="records", date_format="iso")
        b64 = base64.b64encode(data.encode()).decode()
        mime_type = "application/json"
        file_extension = "json"
    else:
        raise ValueError(f"Unsupported format type: {format_type}")
    
    full_filename = f"{filename}.{file_extension}"
    href = f'<a href="data:{mime_type};base64,{b64}" download="{full_filename}">Download {format_type.upper()} file</a>'
    
    return href

def repeatable_fieldset(
    label: str,
    fields: List[Dict[str, Any]],
    data: Optional[List[Dict[str, Any]]] = None,
    min_items: int = 1,
    max_items: Optional[int] = None,
    key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Create a repeatable fieldset for collecting multiple sets of related data.
    
    Args:
        label: The fieldset label
        fields: List of field definitions, each with keys 'key', 'label', 'type', etc.
        data: Optional initial data for the fields
        min_items: Minimum number of items
        max_items: Maximum number of items (None for unlimited)
        key: Unique key for the component
        
    Returns:
        List of dictionaries with collected data
    """
    # Generate a unique key if not provided
    if key is None:
        key = f"fieldset_{id(fields)}"
    
    # Initialize session state for this fieldset
    if f"{key}_items" not in st.session_state:
        initial_items = max(min_items, len(data) if data else 0)
        st.session_state[f"{key}_items"] = initial_items
    
    st.markdown(f"## {label}")
    
    # Create container for the fieldset items
    items_data = []
    
    for i in range(st.session_state[f"{key}_items"]):
        with st.expander(f"{label} #{i+1}", expanded=True):
            item_data = {}
            
            for field in fields:
                field_key = field["key"]
                field_label = field.get("label", field_key.replace("_", " ").title())
                field_type = field.get("type", "text")
                field_required = field.get("required", False)
                field_help = field.get("help", "")
                
                # Get initial value from data if available
                initial_value = None
                if data and i < len(data) and field_key in data[i]:
                    initial_value = data[i][field_key]
                
                # Render appropriate field type
                if field_type == "text":
                    value = st.text_input(
                        field_label,
                        value=initial_value or "",
                        help=field_help,
                        key=f"{key}_{i}_{field_key}"
                    )
                    
                elif field_type == "number":
                    min_val = field.get("min", 0)
                    max_val = field.get("max", 100)
                    step = field.get("step", 1)
                    
                    value = st.number_input(
                        field_label,
                        min_value=min_val,
                        max_value=max_val,
                        value=initial_value if initial_value is not None else min_val,
                        step=step,
                        help=field_help,
                        key=f"{key}_{i}_{field_key}"
                    )
                    
                elif field_type == "date":
                    value = st.date_input(
                        field_label,
                        value=initial_value if initial_value else datetime.now().date(),
                        help=field_help,
                        key=f"{key}_{i}_{field_key}"
                    )
                    
                elif field_type == "select":
                    options = field.get("options", [])
                    value = st.selectbox(
                        field_label,
                        options=options,
                        index=options.index(initial_value) if initial_value in options else 0,
                        help=field_help,
                        key=f"{key}_{i}_{field_key}"
                    )
                    
                elif field_type == "multiselect":
                    options = field.get("options", [])
                    value = st.multiselect(
                        field_label,
                        options=options,
                        default=initial_value if initial_value else [],
                        help=field_help,
                        key=f"{key}_{i}_{field_key}"
                    )
                    
                elif field_type == "textarea":
                    value = st.text_area(
                        field_label,
                        value=initial_value or "",
                        help=field_help,
                        key=f"{key}_{i}_{field_key}"
                    )
                    
                elif field_type == "checkbox":
                    value = st.checkbox(
                        field_label,
                        value=initial_value if initial_value is not None else False,
                        help=field_help,
                        key=f"{key}_{i}_{field_key}"
                    )
                
                item_data[field_key] = value
            
            # Add option to remove this item
            if st.session_state[f"{key}_items"] > min_items:
                if st.button(f"Remove {label} #{i+1}", key=f"{key}_remove_{i}"):
                    # Remove this item
                    st.session_state[f"{key}_items"] -= 1
                    # Need to rerun to update the UI
                    st.experimental_rerun()
            
            items_data.append(item_data)
    
    # Add button to add another item
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if max_items is None or st.session_state[f"{key}_items"] < max_items:
            if st.button(f"Add {label}", key=f"{key}_add"):
                st.session_state[f"{key}_items"] += 1
                st.experimental_rerun()
    
    return items_data