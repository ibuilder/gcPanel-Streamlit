"""
Schedule importer module for handling Microsoft Project and XER file formats.

This module provides functions for:
1. Importing Microsoft Project (.mpp) files
2. Importing Primavera P6 (.xer) files
3. Converting schedule data to a standard format for display
"""

import streamlit as st
import os
import tempfile
import uuid
import pandas as pd
from datetime import datetime, timedelta
import random

class ScheduleImporter:
    """Import and process schedule files from various formats."""
    
    @staticmethod
    def handle_schedule_upload(uploaded_file, project_id=None):
        """
        Handle uploaded schedule files (Microsoft Project or XER).
        
        Args:
            uploaded_file: The uploaded file from st.file_uploader
            project_id: Optional project ID to associate with the schedule
            
        Returns:
            dict: Information about the processed schedule including tasks
        """
        if uploaded_file is None:
            return None
        
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Create a unique identifier for this schedule
        schedule_id = str(uuid.uuid4())
        
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_path = tmp_file.name
        
        schedule_info = {
            "id": schedule_id,
            "original_filename": uploaded_file.name,
            "file_type": file_ext.lstrip('.'),
            "upload_date": datetime.now(),
            "file_size": len(uploaded_file.getvalue()),
            "temp_path": temp_path,
            "project_id": project_id
        }
        
        # Process based on file type
        if file_ext == '.mpp':
            return ScheduleImporter.process_ms_project_file(schedule_info)
        elif file_ext == '.xer':
            return ScheduleImporter.process_xer_file(schedule_info)
        else:
            os.unlink(temp_path)  # Remove temp file
            return {"error": f"Unsupported file type: {file_ext}"}
    
    @staticmethod
    def process_ms_project_file(schedule_info):
        """
        Process a Microsoft Project file.
        
        Args:
            schedule_info: Dictionary with information about the schedule
            
        Returns:
            dict: Updated information with tasks extracted from the file
        """
        # In a real implementation, this would use a library to extract data from MPP files
        # For this demo, we'll generate sample tasks
        
        st.info("In a production environment, this would use a Microsoft Project API or library to extract schedule data.")
        
        # Create sample schedule data
        schedule_info["tasks"] = ScheduleImporter.generate_sample_tasks()
        schedule_info["processing_status"] = "simulated"
        
        return schedule_info
    
    @staticmethod
    def process_xer_file(schedule_info):
        """
        Process a Primavera P6 XER file.
        
        Args:
            schedule_info: Dictionary with information about the schedule
            
        Returns:
            dict: Updated information with tasks extracted from the file
        """
        # In a real implementation, this would parse XER file format
        # For this demo, we'll generate sample tasks
        
        st.info("In a production environment, this would parse the XER file to extract schedule data.")
        
        # Create sample schedule data with more complex dependencies for XER
        schedule_info["tasks"] = ScheduleImporter.generate_sample_tasks(more_complex=True)
        schedule_info["processing_status"] = "simulated"
        
        return schedule_info
    
    @staticmethod
    def generate_sample_tasks(more_complex=False):
        """
        Generate sample task data for demonstration.
        
        Args:
            more_complex: Whether to generate a more complex schedule
            
        Returns:
            list: Sample task data
        """
        # Construction phases
        phases = [
            "Preconstruction",
            "Site Preparation",
            "Foundation",
            "Structural",
            "Exterior",
            "Interior Rough-in",
            "Interior Finishes",
            "Landscaping",
            "Closeout"
        ]
        
        # Task templates for each phase
        task_templates = {
            "Preconstruction": [
                "Design Development", 
                "Construction Documents", 
                "Permitting", 
                "Bidding",
                "Contracts"
            ],
            "Site Preparation": [
                "Site Survey",
                "Demolition",
                "Site Clearing",
                "Grading",
                "Temporary Facilities",
                "Erosion Control"
            ],
            "Foundation": [
                "Excavation",
                "Footings",
                "Foundation Walls",
                "Waterproofing",
                "Backfill",
                "Concrete Slab"
            ],
            "Structural": [
                "Steel Erection",
                "Framing",
                "Roof Trusses",
                "Sheathing",
                "Concrete Floors",
                "Stairwells"
            ],
            "Exterior": [
                "Roofing",
                "Windows",
                "Exterior Doors",
                "Siding/Cladding",
                "Brick/Masonry",
                "Exterior Trim"
            ],
            "Interior Rough-in": [
                "Plumbing Rough-in",
                "Electrical Rough-in",
                "HVAC Rough-in",
                "Fire Sprinkler",
                "Insulation",
                "Drywall"
            ],
            "Interior Finishes": [
                "Taping and Finishing",
                "Painting",
                "Flooring",
                "Cabinetry",
                "Trim",
                "Fixtures",
                "Appliances"
            ],
            "Landscaping": [
                "Hardscaping",
                "Irrigation",
                "Planting",
                "Exterior Lighting",
                "Fencing"
            ],
            "Closeout": [
                "Final Cleaning",
                "Punch List",
                "Inspections",
                "Owner Training",
                "Commissioning",
                "Project Closeout"
            ]
        }
        
        # Generate project timeline
        project_start = datetime.now() - timedelta(days=30)  # Start 30 days ago
        
        tasks = []
        task_id = 1
        
        for phase_index, phase in enumerate(phases):
            # Create phase summary task
            phase_duration = sum(random.randint(3, 10) for _ in range(len(task_templates[phase])))
            phase_task = {
                "id": task_id,
                "wbs": f"{phase_index + 1}",
                "name": phase,
                "start_date": project_start + timedelta(days=phase_index * 20),
                "end_date": project_start + timedelta(days=phase_index * 20 + phase_duration),
                "duration": phase_duration,
                "progress": random.randint(0, 100) if phase_index < 4 else 0,
                "resources": [],
                "is_summary": True,
                "predecessors": [] if phase_index == 0 else [phases[phase_index - 1]],
                "phase": phase
            }
            tasks.append(phase_task)
            task_id += 1
            
            # Add tasks for this phase
            phase_tasks = task_templates[phase]
            current_date = phase_task["start_date"]
            
            for task_index, task_name in enumerate(phase_tasks):
                task_duration = random.randint(3, 10)
                
                # Calculate predecessor tasks
                predecessors = []
                if task_index > 0:
                    # Previous task in same phase
                    predecessors.append(task_id - 1)
                elif phase_index > 0 and more_complex:
                    # Last task of previous phase for complex schedules
                    for prev_task in reversed(tasks):
                        if prev_task["phase"] == phases[phase_index - 1] and not prev_task["is_summary"]:
                            predecessors.append(prev_task["id"])
                            break
                
                task = {
                    "id": task_id,
                    "wbs": f"{phase_index + 1}.{task_index + 1}",
                    "name": task_name,
                    "start_date": current_date,
                    "end_date": current_date + timedelta(days=task_duration),
                    "duration": task_duration,
                    "progress": random.randint(0, 100) if current_date < datetime.now() else 0,
                    "resources": random.sample(["John Smith", "Mary Johnson", "Bob Williams", "Sarah Davis", "Michael Brown"], random.randint(1, 2)),
                    "is_summary": False,
                    "predecessors": predecessors,
                    "phase": phase
                }
                tasks.append(task)
                task_id += 1
                
                # Move date forward for next task (with some tasks in parallel for complex)
                if more_complex and random.random() > 0.7 and task_index < len(phase_tasks) - 1:
                    # Some tasks start in parallel
                    pass
                else:
                    current_date = task["end_date"]
        
        return tasks