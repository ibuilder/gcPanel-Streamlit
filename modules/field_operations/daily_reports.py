"""
Daily Reports Module for gcPanel

This module implements the Daily Reports functionality for the Field Operations section,
using the standardized CRUD template for consistent styling and behavior.
"""

import streamlit as st
import os
import json
from datetime import datetime, timedelta
import random
import pandas as pd

from modules.crud_template import CrudModule
from assets.crud_styler import (
    apply_crud_styles, 
    render_form_actions, 
    render_crud_fieldset
)

class DailyReportModule(CrudModule):
    def __init__(self):
        """Initialize the Daily Reports module with configuration."""
        super().__init__(
            module_name="Daily Reports",
            data_file_path="data/field_operations/daily_reports.json",
            id_field="report_id",
            list_columns=["report_id", "report_date", "weather", "temperature", "work_completed", "submitted_by"],
            default_sort_field="report_date",
            default_sort_direction="desc",
            status_field=None,
            filter_options=None
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        weather_conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain", "Windy"]
        work_completed = [
            "Concrete pour for level 3 east wing", 
            "Steel erection for levels 5-6", 
            "Framing on levels 1-2",
            "MEP rough-in on level 4", 
            "Window installation on south facade", 
            "Drywall installation on level 7",
            "Site clearing and excavation", 
            "Foundation waterproofing", 
            "Interior painting on level 2",
            "Plumbing fixture installation on level 3"
        ]
        
        demo_items = []
        
        # Create sample daily reports for the past 30 days
        for i in range(30, 0, -1):
            report_date = datetime.now() - timedelta(days=i)
            
            # Generate random data
            temp_min = random.randint(50, 80)
            temp_max = temp_min + random.randint(5, 15)
            weather = random.choice(weather_conditions)
            
            # Generate random workforce numbers
            workers = {
                "Concrete": random.randint(0, 15),
                "Steel": random.randint(0, 12),
                "Carpentry": random.randint(0, 20),
                "Electrical": random.randint(0, 10),
                "Plumbing": random.randint(0, 8),
                "HVAC": random.randint(0, 6),
                "Drywall": random.randint(0, 15),
                "Painting": random.randint(0, 10),
                "Flooring": random.randint(0, 8),
                "Other": random.randint(0, 5)
            }
            
            # Calculate total workers
            total_workers = sum(workers.values())
            
            # Select work completed items (1-3 items per day)
            num_work_items = random.randint(1, 3)
            day_work_completed = []
            
            for _ in range(num_work_items):
                item = random.choice(work_completed)
                if item not in day_work_completed:
                    day_work_completed.append(item)
            
            # Create the daily report
            report = {
                'report_id': f"DR-{report_date.strftime('%Y%m%d')}",
                'report_date': report_date.strftime('%Y-%m-%d'),
                'weather': weather,
                'temperature': f"{temp_min}°F - {temp_max}°F",
                'workers': workers,
                'total_workers': total_workers,
                'work_completed': ", ".join(day_work_completed),
                'materials_delivered': "None" if random.random() < 0.7 else "Steel beams, Electrical conduit",
                'equipment_on_site': "Crane, Excavator, Forklifts" if random.random() < 0.7 else "Concrete pump, Scissor lifts",
                'delays': "None" if random.random() < 0.8 else "2-hour rain delay in the morning",
                'safety_incidents': "None" if random.random() < 0.95 else "Minor incident: worker slip without injury",
                'visitors': "None" if random.random() < 0.9 else "Owner representative, Building inspector",
                'notes': "" if random.random() < 0.7 else "Additional crew needed for next week to maintain schedule",
                'submitted_by': "John Doe" if i % 2 == 0 else "Jane Smith",
                'submission_time': report_date.replace(hour=16, minute=random.randint(0, 59)).strftime('%Y-%m-%d %H:%M'),
                'photos': []
            }
            
            demo_items.append(report)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new daily report with default values."""
        today = datetime.now()
        
        return {
            'report_id': f"DR-{today.strftime('%Y%m%d')}",
            'report_date': today.strftime('%Y-%m-%d'),
            'weather': "Sunny",
            'temperature': "70°F - 75°F",
            'workers': {
                "Concrete": 0,
                "Steel": 0,
                "Carpentry": 0,
                "Electrical": 0,
                "Plumbing": 0,
                "HVAC": 0,
                "Drywall": 0,
                "Painting": 0,
                "Flooring": 0,
                "Other": 0
            },
            'total_workers': 0,
            'work_completed': "",
            'materials_delivered': "",
            'equipment_on_site': "",
            'delays': "None",
            'safety_incidents': "None",
            'visitors': "None",
            'notes': "",
            'submitted_by': "Current User",
            'submission_time': today.strftime('%Y-%m-%d %H:%M'),
            'photos': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for daily reports based on date."""
        today = datetime.now()
        return f"DR-{today.strftime('%Y%m%d')}"
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing a daily report."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = f"Daily Report for {item['report_date']}"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Daily Report with ID {item_id} not found")
                return
            detail_title = f"Daily Report for {item['report_date']}"
        
        # Render the detail container
        from assets.crud_styler import render_crud_detail_container, end_crud_detail_container
        
        mode_prefix = "New" if is_new else "Edit" if is_edit_mode else "View"
        container_title = f"{mode_prefix}: {detail_title}"
        
        detail_actions = render_crud_detail_container(
            title=container_title,
            is_new=is_new,
            back_button=True
        )
        
        # Check if back button was clicked
        if detail_actions['back_clicked']:
            st.session_state[f'{base_key}_view'] = 'list'
            st.rerun()
        
        # Display top action buttons for view mode
        if not is_new and not is_edit_mode:
            col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
            with col1:
                if st.button("✏️ Edit", type="primary", key=f"edit_{base_key}_action"):
                    st.session_state[f'{base_key}_edit_mode'] = True
                    st.rerun()
            with col2:
                if st.button("📄 PDF", type="secondary", key=f"pdf_{base_key}_action"):
                    st.info("This would generate a PDF version of the daily report in a production environment.")
            with col3:
                if st.button("🗑️ Delete", type="secondary", key=f"delete_{base_key}_action"):
                    st.warning("Are you sure you want to delete this daily report?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key=f"confirm_delete_{base_key}"):
                            self._delete_item(item['report_id'])
                            st.success("Daily report deleted successfully")
                            st.session_state[f'{base_key}_view'] = 'list'
                            st.rerun()
                    with confirm_col2:
                        if st.button("Cancel", key=f"cancel_delete_{base_key}"):
                            st.rerun()
        
        # Create form for editing or read-only view for viewing
        if is_edit_mode or is_new:
            with st.form(f"{base_key}_form"):
                # Basic Information Section
                def render_basic_info():
                    col1, col2 = st.columns(2)
                    with col1:
                        report_date = st.date_input(
                            "Report Date", 
                            value=datetime.strptime(item['report_date'], '%Y-%m-%d') if item['report_date'] else datetime.now()
                        )
                    with col2:
                        submitted_by = st.text_input("Submitted By", value=item['submitted_by'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        weather = st.selectbox(
                            "Weather", 
                            options=["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain", "Windy", "Snow", "Fog"],
                            index=["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain", "Windy", "Snow", "Fog"].index(
                                item['weather'] if item['weather'] in ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain", "Windy", "Snow", "Fog"] 
                                else "Sunny"
                            )
                        )
                    with col2:
                        temperature = st.text_input("Temperature", value=item['temperature'])
                
                render_crud_fieldset("Basic Information", render_basic_info)
                
                # Workforce Section
                def render_workforce():
                    st.markdown("Enter the number of workers on site for each trade:")
                    
                    workers = item['workers']
                    updated_workers = {}
                    total_workers = 0
                    
                    # Create two columns for worker counts
                    col1, col2 = st.columns(2)
                    
                    # Process trades in two columns
                    trades = list(workers.keys())
                    half = len(trades) // 2
                    
                    for i, trade in enumerate(trades[:half]):
                        with col1:
                            count = st.number_input(
                                f"{trade}", 
                                value=int(workers.get(trade, 0)),
                                min_value=0,
                                step=1,
                                key=f"workers_{trade}_{base_key}"
                            )
                            updated_workers[trade] = count
                            total_workers += count
                    
                    for i, trade in enumerate(trades[half:]):
                        with col2:
                            count = st.number_input(
                                f"{trade}", 
                                value=int(workers.get(trade, 0)),
                                min_value=0,
                                step=1,
                                key=f"workers_{trade}_{base_key}_2"
                            )
                            updated_workers[trade] = count
                            total_workers += count
                    
                    st.markdown(f"**Total Workers on Site:** {total_workers}")
                    
                    return updated_workers, total_workers
                
                workers_data, total_workers = render_crud_fieldset("Workforce", render_workforce)
                
                # Work Details Section
                def render_work_details():
                    work_completed = st.text_area("Work Completed Today", value=item['work_completed'], height=100)
                    materials_delivered = st.text_area("Materials Delivered", value=item['materials_delivered'], height=75)
                    equipment_on_site = st.text_area("Equipment on Site", value=item['equipment_on_site'], height=75)
                    
                    return work_completed, materials_delivered, equipment_on_site
                
                work_completed, materials_delivered, equipment_on_site = render_crud_fieldset("Work Details", render_work_details)
                
                # Issues and Notes Section
                def render_issues_notes():
                    delays = st.text_area("Delays and Issues", value=item['delays'], height=75)
                    safety_incidents = st.text_area("Safety Incidents", value=item['safety_incidents'], height=75)
                    visitors = st.text_area("Site Visitors", value=item['visitors'], height=75)
                    notes = st.text_area("Additional Notes", value=item['notes'], height=100)
                    
                    return delays, safety_incidents, visitors, notes
                
                delays, safety_incidents, visitors, notes = render_crud_fieldset("Issues and Notes", render_issues_notes)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Daily Report",
                    cancel_label="Cancel",
                    delete_label="Delete Daily Report",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'report_id': item['report_id'] if not is_new else f"DR-{report_date.strftime('%Y%m%d')}",
                        'report_date': report_date.strftime('%Y-%m-%d'),
                        'weather': weather,
                        'temperature': temperature,
                        'workers': workers_data,
                        'total_workers': total_workers,
                        'work_completed': work_completed,
                        'materials_delivered': materials_delivered,
                        'equipment_on_site': equipment_on_site,
                        'delays': delays,
                        'safety_incidents': safety_incidents,
                        'visitors': visitors,
                        'notes': notes,
                        'submitted_by': submitted_by,
                        'submission_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'photos': item.get('photos', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Daily report saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['report_id'])
                    st.success("Daily report deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Basic Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Basic Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Report Date:** {item['report_date']}")
            with col2:
                st.markdown(f"**Submitted By:** {item['submitted_by']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Weather:** {item['weather']}")
            with col2:
                st.markdown(f"**Temperature:** {item['temperature']}")
            
            st.markdown(f"**Submission Time:** {item['submission_time']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Workforce Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Workforce")
            
            workers = item['workers']
            trades = list(workers.keys())
            
            # Display workforce in two columns
            col1, col2 = st.columns(2)
            half = len(trades) // 2
            
            with col1:
                for trade in trades[:half]:
                    st.markdown(f"**{trade}:** {workers[trade]}")
            
            with col2:
                for trade in trades[half:]:
                    st.markdown(f"**{trade}:** {workers[trade]}")
            
            st.markdown(f"**Total Workers on Site:** {item['total_workers']}")
            
            # Display workforce as a bar chart
            if workers:
                chart_data = pd.DataFrame({
                    'Trade': list(workers.keys()),
                    'Workers': list(workers.values())
                })
                
                # Only show trades with workers > 0
                chart_data = chart_data[chart_data['Workers'] > 0]
                
                if not chart_data.empty:
                    st.bar_chart(chart_data.set_index('Trade'))
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Work Details Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Work Details")
            
            st.markdown("**Work Completed Today:**")
            st.markdown(f"```{item['work_completed']}```")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Materials Delivered:**")
                st.markdown(f"```{item['materials_delivered']}```")
            
            with col2:
                st.markdown("**Equipment on Site:**")
                st.markdown(f"```{item['equipment_on_site']}```")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Issues and Notes Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Issues and Notes")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Delays and Issues:**")
                st.markdown(f"```{item['delays']}```")
            
            with col2:
                st.markdown("**Safety Incidents:**")
                st.markdown(f"```{item['safety_incidents']}```")
            
            st.markdown("**Site Visitors:**")
            st.markdown(f"```{item['visitors']}```")
            
            if item.get('notes'):
                st.markdown("**Additional Notes:**")
                st.markdown(f"```{item['notes']}```")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Photos Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Site Photos")
            
            if not item.get('photos'):
                st.info("No photos uploaded for this report.")
                
                # Add photo button
                if st.button("➕ Add Photo", key=f"add_photo_{base_key}"):
                    st.session_state[f'{base_key}_add_photo'] = True
                    
                if st.session_state.get(f'{base_key}_add_photo', False):
                    with st.form(f"photo_form_{base_key}"):
                        photo_title = st.text_input("Photo Title")
                        photo_description = st.text_input("Description")
                        
                        photo_actions = st.columns([1, 1])
                        with photo_actions[0]:
                            save_photo = st.form_submit_button("Save Photo")
                        with photo_actions[1]:
                            cancel_photo = st.form_submit_button("Cancel")
                        
                        if save_photo and photo_title:
                            # Add photo to the item
                            new_photo = {
                                'title': photo_title,
                                'description': photo_description,
                                'date_added': datetime.now().strftime('%Y-%m-%d'),
                                'added_by': "Current User",
                                'file_name': "demo_construction_photo.jpg"  # Demo mode only
                            }
                            
                            photos = item.get('photos', [])
                            photos.append(new_photo)
                            
                            # Update item with new photo
                            item['photos'] = photos
                            self._save_item(item)
                            
                            st.success("Photo added successfully")
                            st.session_state[f'{base_key}_add_photo'] = False
                            st.rerun()
                        
                        if cancel_photo:
                            st.session_state[f'{base_key}_add_photo'] = False
                            st.rerun()
            else:
                # Display photos
                photos = item.get('photos', [])
                photo_cols = st.columns(min(len(photos), 3))
                
                for i, photo in enumerate(photos):
                    with photo_cols[i % len(photo_cols)]:
                        st.markdown(f"**{photo['title']}**")
                        st.image("https://via.placeholder.com/300x200.png?text=Construction+Photo", caption=photo['description'])
                        st.markdown(f"Added: {photo['date_added']} by {photo['added_by']}")
                
                # Add photo button
                if st.button("➕ Add Photo", key=f"add_photo_{base_key}"):
                    st.session_state[f'{base_key}_add_photo'] = True
                    
                if st.session_state.get(f'{base_key}_add_photo', False):
                    with st.form(f"photo_form_{base_key}"):
                        photo_title = st.text_input("Photo Title")
                        photo_description = st.text_input("Description")
                        
                        photo_actions = st.columns([1, 1])
                        with photo_actions[0]:
                            save_photo = st.form_submit_button("Save Photo")
                        with photo_actions[1]:
                            cancel_photo = st.form_submit_button("Cancel")
                        
                        if save_photo and photo_title:
                            # Add photo to the item
                            new_photo = {
                                'title': photo_title,
                                'description': photo_description,
                                'date_added': datetime.now().strftime('%Y-%m-%d'),
                                'added_by': "Current User",
                                'file_name': "demo_construction_photo.jpg"  # Demo mode only
                            }
                            
                            photos = item.get('photos', [])
                            photos.append(new_photo)
                            
                            # Update item with new photo
                            item['photos'] = photos
                            self._save_item(item)
                            
                            st.success("Photo added successfully")
                            st.session_state[f'{base_key}_add_photo'] = False
                            st.rerun()
                        
                        if cancel_photo:
                            st.session_state[f'{base_key}_add_photo'] = False
                            st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        end_crud_detail_container()

def render():
    """Render the Daily Reports module."""
    st.title("Daily Reports")
    
    # Create and render the Daily Reports module
    daily_reports = DailyReportModule()
    daily_reports.render()