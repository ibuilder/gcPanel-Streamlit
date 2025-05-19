"""
Smart Suggestions and Predictive Typing for gcPanel.

This module provides AI-powered suggestions and predictive typing
capabilities for input fields throughout the application.
"""

import streamlit as st
import json
import re
from datetime import datetime

class PredictiveTyping:
    """Predictive typing and smart suggestions for form fields."""
    
    def __init__(self):
        """Initialize the predictive typing system."""
        # Load suggestion corpus
        self.suggestion_corpus = self.load_suggestion_corpus()
    
    def load_suggestion_corpus(self):
        """
        Load the suggestion corpus.
        
        In a production system, this would be learned from actual user inputs
        and stored in a database. For this demo, we'll use a static corpus.
        
        Returns:
            dict: Suggestion corpus organized by field type
        """
        # Check if we have a cached corpus in session state
        if "suggestion_corpus" in st.session_state:
            return st.session_state.suggestion_corpus
        
        # Categories of suggestions
        corpus = {
            "person_names": [
                "John Smith", "Sarah Johnson", "Michael Chen", "Lisa Rodriguez", 
                "David Kim", "Emma Wilson", "Robert Garcia", "Maria Patel",
                "James Lee", "Jennifer Martinez", "Daniel Cohen", "Emily Taylor"
            ],
            "company_names": [
                "Highland Construction", "ABC Electrical", "Metro Concrete Solutions",
                "Pinnacle Structural Engineering", "Elite HVAC Systems", "City Glass & Glazing",
                "Blue Ridge Excavation", "Summit Plumbing", "Precision Drywall",
                "Western Roofing", "Ace Elevator Company", "United Steel Fabricators"
            ],
            "job_titles": [
                "Project Manager", "Superintendent", "Field Engineer", "Safety Manager",
                "Quality Control Manager", "Project Executive", "Foreman", "Estimator",
                "Scheduler", "Design Manager", "BIM Coordinator", "Site Engineer"
            ],
            "materials": [
                "Concrete", "Steel Reinforcement", "Structural Steel", "Glass Curtain Wall",
                "Metal Stud Framing", "Gypsum Wallboard", "Electrical Conduit", "Copper Wiring",
                "HVAC Ductwork", "Plumbing Pipe", "Spray Fireproofing", "Acoustic Ceiling Tile"
            ],
            "locations": [
                "Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5", 
                "Floor 6", "Floor 7", "Floor 8", "Floor 9", "Floor 10", 
                "Floor 11", "Floor 12", "Floor 13", "Floor 14", "Floor 15",
                "Basement 1", "Basement 2", "Roof", "East Wing", "West Wing",
                "North Tower", "South Tower", "Parking Garage", "Mechanical Room"
            ],
            "specifications": [
                "ACI 318", "ASTM A615", "AISC 360", "ASCE 7", "NFPA 13",
                "ASHRAE 90.1", "IBC 2018", "ASME A17.1", "AWS D1.1", "UL 263"
            ],
            "documents": [
                "Architectural Drawings", "Structural Plans", "MEP Drawings", 
                "Specifications", "Shop Drawings", "RFIs", "Submittals", 
                "Change Orders", "Daily Reports", "Inspection Reports", 
                "Meeting Minutes", "Project Schedule"
            ],
            "issue_types": [
                "RFI", "Submittal", "Change Order", "Construction Defect",
                "Safety Hazard", "Quality Issue", "Design Conflict", "Material Defect",
                "Schedule Delay", "Cost Overrun", "Permitting Issue", "Weather Delay"
            ],
            "common_phrases": [
                "Please review and approve", 
                "Per our discussion yesterday",
                "As shown in the attached document",
                "This requires immediate attention",
                "According to the specifications",
                "Please provide clarification on",
                "This is critical for the schedule",
                "We need a response by",
                "This has been resolved as discussed",
                "Let me know if you have any questions"
            ]
        }
        
        # Cache corpus in session state
        st.session_state.suggestion_corpus = corpus
        
        return corpus
    
    def get_suggestions(self, field_id, current_text="", max_suggestions=5):
        """
        Get auto-complete suggestions for a field.
        
        Args:
            field_id (str): Identifier for the field type
            current_text (str): Current text in the field
            max_suggestions (int): Maximum number of suggestions to return
            
        Returns:
            list: Suggested completions
        """
        # If no text entered, return empty list
        if not current_text:
            return []
        
        # Map field_id to corpus category
        category_mapping = {
            "person_name": "person_names",
            "company": "company_names",
            "job_title": "job_titles",
            "material": "materials",
            "location": "locations",
            "specification": "specifications",
            "document": "documents",
            "issue_type": "issue_types",
            "comment": "common_phrases",
            "description": "common_phrases"
        }
        
        # Default to using multiple categories if field type not recognized
        categories = []
        
        if field_id in category_mapping:
            categories = [category_mapping[field_id]]
        else:
            # For unknown field types, try multiple categories
            categories = ["person_names", "company_names", "locations", "materials"]
        
        # Get suggestions from all relevant categories
        suggestions = []
        
        for category in categories:
            if category in self.suggestion_corpus:
                # Filter corpus entries that contain the current text
                matches = [item for item in self.suggestion_corpus[category] 
                          if current_text.lower() in item.lower()]
                suggestions.extend(matches)
        
        # Sort suggestions by relevance (starting with input has higher relevance)
        suggestions.sort(key=lambda x: 0 if x.lower().startswith(current_text.lower()) else 1)
        
        return suggestions[:max_suggestions]
    
    def render_predictive_input(self, label, field_id, key=None, value="", placeholder=None):
        """
        Render a text input with predictive typing.
        
        Args:
            label (str): Input label
            field_id (str): Field identifier for suggestion corpus
            key (str): Streamlit key for the input
            value (str): Initial value
            placeholder (str): Placeholder text
            
        Returns:
            str: Entered text
        """
        # Generate a unique key if not provided
        if key is None:
            key = f"predictive_{field_id}_{id(label)}"
        
        # Initialize session state for this input
        if key not in st.session_state:
            st.session_state[key] = value
        
        # Create text input
        entered_text = st.text_input(
            label,
            value=st.session_state[key],
            key=f"input_{key}",
            placeholder=placeholder
        )
        
        # Get suggestions based on current input
        suggestions = self.get_suggestions(field_id, entered_text)
        
        if suggestions:
            # Create a radio group for suggestions
            st.markdown("**Suggestions:**")
            
            selected_suggestion = st.radio(
                "Select a suggestion",
                options=suggestions,
                key=f"suggestions_{key}",
                label_visibility="collapsed"
            )
            
            # Use button to apply suggestion
            if st.button("Use Suggestion", key=f"use_{key}"):
                st.session_state[key] = selected_suggestion
                entered_text = selected_suggestion
                st.rerun()
        
        return entered_text
    
    def render_predictive_textarea(self, label, field_id, key=None, value="", placeholder=None, height=100):
        """
        Render a text area with predictive typing.
        
        Args:
            label (str): Input label
            field_id (str): Field identifier for suggestion corpus
            key (str): Streamlit key for the input
            value (str): Initial value
            placeholder (str): Placeholder text
            height (int): Height of the text area
            
        Returns:
            str: Entered text
        """
        # Generate a unique key if not provided
        if key is None:
            key = f"predictive_area_{field_id}_{id(label)}"
        
        # Initialize session state for this input
        if key not in st.session_state:
            st.session_state[key] = value
        
        # Create text area
        entered_text = st.text_area(
            label,
            value=st.session_state[key],
            key=f"input_{key}",
            placeholder=placeholder,
            height=height
        )
        
        # Get suggestions for the last word being typed
        words = entered_text.split()
        current_word = words[-1] if words else ""
        
        # Only show suggestions if current word has at least 3 characters
        if len(current_word) >= 3:
            suggestions = self.get_suggestions(field_id, current_word)
            
            if suggestions:
                # Create a select box for suggestions
                st.markdown("**Complete current word with:**")
                
                selected_suggestion = st.selectbox(
                    "Select a suggestion",
                    options=suggestions,
                    key=f"suggestions_{key}",
                    label_visibility="collapsed"
                )
                
                # Use button to apply suggestion
                if st.button("Insert", key=f"use_{key}"):
                    # Replace the last word with the suggestion
                    if words:
                        words[-1] = selected_suggestion
                    else:
                        words = [selected_suggestion]
                    
                    st.session_state[key] = " ".join(words)
                    entered_text = st.session_state[key]
                    st.rerun()
        
        # Also offer completing common phrases
        common_phrases = self.suggestion_corpus["common_phrases"]
        
        with st.expander("Insert common phrase"):
            selected_phrase = st.selectbox(
                "Select a phrase",
                options=common_phrases,
                key=f"phrases_{key}"
            )
            
            if st.button("Insert Phrase", key=f"use_phrase_{key}"):
                if entered_text:
                    st.session_state[key] = entered_text + " " + selected_phrase
                else:
                    st.session_state[key] = selected_phrase
                
                entered_text = st.session_state[key]
                st.rerun()
        
        return entered_text


class IntelligentAlerts:
    """Intelligent alerts based on project patterns."""
    
    def __init__(self):
        """Initialize the intelligent alerts system."""
        # Load alerts data
        self.alerts = self.load_alerts()
        
        # Set alert thresholds
        self.thresholds = {
            "schedule_delay": 5,  # days
            "budget_overrun": 5,  # percent
            "safety_incidents": 1,  # count
            "quality_issues": 3,  # count
            "weather_risk": 70  # percent
        }
    
    def load_alerts(self):
        """
        Load alerts data.
        
        In a production system, this would analyze real project data.
        For this demo, we'll simulate alerts.
        
        Returns:
            dict: Alerts data by type
        """
        # Check if we have cached alerts in session state
        if "intelligent_alerts" in st.session_state:
            return st.session_state.intelligent_alerts
        
        # Generate mock alerts
        alerts = {
            "high_priority": [
                {
                    "id": "alert1",
                    "type": "schedule_delay",
                    "title": "Critical Path Delay Risk",
                    "description": "The curtain wall installation is 3 days behind schedule, which may impact the building envelope completion milestone.",
                    "affected_areas": ["Floors 8-12", "Building Envelope"],
                    "impact": "High",
                    "recommendation": "Authorize overtime work for the glazing contractor to accelerate installation.",
                    "timestamp": "2025-05-16T10:30:00"
                },
                {
                    "id": "alert2",
                    "type": "budget_overrun",
                    "title": "MEP Budget Risk",
                    "description": "The MEP package is trending 7.5% over budget due to material price increases and additional scope.",
                    "affected_areas": ["MEP Systems", "Budget"],
                    "impact": "High",
                    "recommendation": "Review value engineering options for the mechanical systems on floors 10-15.",
                    "timestamp": "2025-05-15T15:45:00"
                }
            ],
            "medium_priority": [
                {
                    "id": "alert3",
                    "type": "quality_issues",
                    "title": "Recurring Drywall Quality Issues",
                    "description": "Multiple quality issues reported with drywall finishing on floors 5-7.",
                    "affected_areas": ["Interior Finishes", "Floors 5-7"],
                    "impact": "Medium",
                    "recommendation": "Schedule quality control inspection with drywall subcontractor foreman.",
                    "timestamp": "2025-05-17T09:15:00"
                },
                {
                    "id": "alert4",
                    "type": "weather_risk",
                    "title": "Upcoming Weather Risk",
                    "description": "Heavy rain forecasted for next week may impact exterior work. 70% probability of delays.",
                    "affected_areas": ["Exterior Work", "Roof"],
                    "impact": "Medium",
                    "recommendation": "Prepare temporary weather protection and adjust schedule for interior work during this period.",
                    "timestamp": "2025-05-18T08:30:00"
                }
            ],
            "low_priority": [
                {
                    "id": "alert5",
                    "type": "documentation",
                    "title": "Missing Inspection Documents",
                    "description": "Some electrical inspection documentation for floor 3 appears to be missing from the system.",
                    "affected_areas": ["Documentation", "Electrical"],
                    "impact": "Low",
                    "recommendation": "Contact electrical subcontractor to resubmit inspection reports for floor 3.",
                    "timestamp": "2025-05-16T14:20:00"
                }
            ]
        }
        
        # Cache alerts in session state
        st.session_state.intelligent_alerts = alerts
        
        return alerts
    
    def analyze_project_data(self, project_data):
        """
        Analyze project data for potential issues.
        
        In a production system, this would use ML to analyze real data.
        For this demo, we'll simulate analysis.
        
        Args:
            project_data (dict): Project data to analyze
            
        Returns:
            list: New alerts generated from analysis
        """
        # Simulated analysis
        new_alerts = []
        
        # Check for schedule delays
        if "schedule" in project_data:
            delay = project_data["schedule"].get("delay_days", 0)
            if delay > self.thresholds["schedule_delay"]:
                new_alerts.append({
                    "id": f"alert_schedule_{len(new_alerts)}",
                    "type": "schedule_delay",
                    "title": f"Schedule Delay: {delay} Days",
                    "description": f"Project is {delay} days behind schedule based on latest progress update.",
                    "affected_areas": project_data["schedule"].get("affected_areas", ["Schedule"]),
                    "impact": "High" if delay > 10 else "Medium",
                    "recommendation": "Review critical path and consider schedule recovery options.",
                    "timestamp": datetime.now().isoformat()
                })
        
        # Check for budget overruns
        if "budget" in project_data:
            overrun_pct = project_data["budget"].get("overrun_pct", 0)
            if overrun_pct > self.thresholds["budget_overrun"]:
                new_alerts.append({
                    "id": f"alert_budget_{len(new_alerts)}",
                    "type": "budget_overrun",
                    "title": f"Budget Overrun: {overrun_pct}%",
                    "description": f"Project is {overrun_pct}% over budget based on latest cost report.",
                    "affected_areas": project_data["budget"].get("affected_areas", ["Budget"]),
                    "impact": "High" if overrun_pct > 10 else "Medium",
                    "recommendation": "Review cost report and identify mitigation strategies.",
                    "timestamp": datetime.now().isoformat()
                })
        
        # Check for safety incidents
        if "safety" in project_data:
            incidents = project_data["safety"].get("incidents", 0)
            if incidents >= self.thresholds["safety_incidents"]:
                new_alerts.append({
                    "id": f"alert_safety_{len(new_alerts)}",
                    "type": "safety_incidents",
                    "title": f"Safety Incidents: {incidents}",
                    "description": f"{incidents} safety incidents reported in the last period.",
                    "affected_areas": project_data["safety"].get("affected_areas", ["Safety"]),
                    "impact": "High",
                    "recommendation": "Schedule safety stand-down and review procedures.",
                    "timestamp": datetime.now().isoformat()
                })
        
        # Additional analysis could be added here
        
        return new_alerts
    
    def get_all_alerts(self):
        """
        Get all current alerts.
        
        Returns:
            list: All alerts from all priority levels
        """
        all_alerts = []
        
        for priority in ["high_priority", "medium_priority", "low_priority"]:
            all_alerts.extend(self.alerts.get(priority, []))
        
        # Sort by timestamp (most recent first)
        all_alerts.sort(key=lambda a: a["timestamp"], reverse=True)
        
        return all_alerts
    
    def get_alerts_by_priority(self, priority):
        """
        Get alerts for a specific priority level.
        
        Args:
            priority (str): Priority level ('high_priority', 'medium_priority', 'low_priority')
            
        Returns:
            list: Alerts for the specified priority
        """
        return self.alerts.get(priority, [])
    
    def get_alerts_by_type(self, alert_type):
        """
        Get alerts for a specific type.
        
        Args:
            alert_type (str): Alert type
            
        Returns:
            list: Alerts of the specified type
        """
        matching_alerts = []
        
        for priority in ["high_priority", "medium_priority", "low_priority"]:
            for alert in self.alerts.get(priority, []):
                if alert["type"] == alert_type:
                    matching_alerts.append(alert)
        
        return matching_alerts
    
    def dismiss_alert(self, alert_id):
        """
        Dismiss an alert.
        
        Args:
            alert_id (str): Alert ID to dismiss
            
        Returns:
            bool: True if alert was found and dismissed, False otherwise
        """
        for priority in ["high_priority", "medium_priority", "low_priority"]:
            for i, alert in enumerate(self.alerts.get(priority, [])):
                if alert["id"] == alert_id:
                    # Remove the alert
                    self.alerts[priority].pop(i)
                    return True
        
        return False
    
    def render_alerts_dashboard(self):
        """Render an intelligent alerts dashboard."""
        st.title("Intelligent Alerts")
        
        # Get counts by priority
        high_count = len(self.alerts.get("high_priority", []))
        medium_count = len(self.alerts.get("medium_priority", []))
        low_count = len(self.alerts.get("low_priority", []))
        total_count = high_count + medium_count + low_count
        
        # Display summary
        st.markdown(f"### Project Alert Summary")
        
        # Create metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Alerts", total_count)
        
        with col2:
            st.metric("High Priority", high_count, delta=f"{high_count} active", delta_color="inverse" if high_count > 0 else "normal")
        
        with col3:
            st.metric("Medium Priority", medium_count)
        
        with col4:
            st.metric("Low Priority", low_count)
        
        # Alert filter
        filter_options = ["All Alerts", "High Priority", "Medium Priority", "Low Priority", 
                           "Schedule", "Budget", "Quality", "Safety", "Weather"]
        
        selected_filter = st.selectbox("Filter Alerts", filter_options)
        
        # Get filtered alerts
        if selected_filter == "All Alerts":
            alerts_to_show = self.get_all_alerts()
        elif selected_filter == "High Priority":
            alerts_to_show = self.get_alerts_by_priority("high_priority")
        elif selected_filter == "Medium Priority":
            alerts_to_show = self.get_alerts_by_priority("medium_priority")
        elif selected_filter == "Low Priority":
            alerts_to_show = self.get_alerts_by_priority("low_priority")
        elif selected_filter == "Schedule":
            alerts_to_show = self.get_alerts_by_type("schedule_delay")
        elif selected_filter == "Budget":
            alerts_to_show = self.get_alerts_by_type("budget_overrun")
        elif selected_filter == "Quality":
            alerts_to_show = self.get_alerts_by_type("quality_issues")
        elif selected_filter == "Safety":
            alerts_to_show = self.get_alerts_by_type("safety_incidents")
        elif selected_filter == "Weather":
            alerts_to_show = self.get_alerts_by_type("weather_risk")
        else:
            alerts_to_show = self.get_all_alerts()
        
        # Display alerts
        if not alerts_to_show:
            st.info(f"No alerts match the selected filter: {selected_filter}")
        else:
            st.markdown(f"### {len(alerts_to_show)} Alerts")
            
            for alert in alerts_to_show:
                # Determine alert color
                alert_color = ""
                if alert["impact"] == "High":
                    alert_color = "#f8d7da"  # light red
                elif alert["impact"] == "Medium":
                    alert_color = "#fff3cd"  # light yellow
                else:
                    alert_color = "#d1e7dd"  # light green
                
                # Create expandable alert card
                with st.expander(f"{alert['title']} ({alert['impact']} Impact)"):
                    st.markdown(f"""
                    <div style="background-color: {alert_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <div style="font-weight: bold; margin-bottom: 5px;">{alert['title']}</div>
                        <div style="margin-bottom: 10px;">{alert['description']}</div>
                        <div style="font-size: 0.9em; margin-bottom: 5px;"><b>Affected Areas:</b> {', '.join(alert['affected_areas'])}</div>
                        <div style="font-size: 0.9em; margin-bottom: 5px;"><b>Recommendation:</b> {alert['recommendation']}</div>
                        <div style="font-size: 0.8em; color: #666;">Generated: {alert['timestamp'].split('T')[0]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Actions
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("Dismiss", key=f"dismiss_{alert['id']}"):
                            if self.dismiss_alert(alert['id']):
                                st.success("Alert dismissed")
                                st.rerun()
                    
                    with col2:
                        if st.button("Assign", key=f"assign_{alert['id']}"):
                            st.info("Would assign the alert to a team member")
                    
                    with col3:
                        if st.button("View Details", key=f"details_{alert['id']}"):
                            st.info("Would show detailed information about this issue")
        
        # Simulation controls
        with st.expander("Simulation Controls (Demo Only)"):
            st.markdown("Use these controls to simulate new alerts for demonstration purposes.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                sim_type = st.selectbox(
                    "Alert Type",
                    ["schedule_delay", "budget_overrun", "quality_issues", "safety_incidents", "weather_risk"]
                )
            
            with col2:
                sim_impact = st.selectbox(
                    "Impact Level",
                    ["High", "Medium", "Low"]
                )
            
            # Form for simulation data
            sim_title = st.text_input("Alert Title", value=f"Simulated {sim_type.replace('_', ' ').title()}")
            sim_description = st.text_area("Description", value="This is a simulated alert for demonstration purposes.")
            sim_areas = st.text_input("Affected Areas (comma-separated)", value="Simulation, Demo")
            sim_recommendation = st.text_area("Recommendation", value="This is a simulated recommendation.")
            
            if st.button("Generate Simulated Alert"):
                # Create new alert with simulation data
                new_alert = {
                    "id": f"sim_alert_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "type": sim_type,
                    "title": sim_title,
                    "description": sim_description,
                    "affected_areas": [area.strip() for area in sim_areas.split(",")],
                    "impact": sim_impact,
                    "recommendation": sim_recommendation,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Add to appropriate priority list
                if sim_impact == "High":
                    self.alerts["high_priority"].append(new_alert)
                elif sim_impact == "Medium":
                    self.alerts["medium_priority"].append(new_alert)
                else:
                    self.alerts["low_priority"].append(new_alert)
                
                st.success("Simulated alert generated!")
                st.rerun()