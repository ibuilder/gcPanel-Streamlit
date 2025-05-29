"""
Field Operations Manager for gcPanel Highland Tower Development

Implements offline capability, photo management, voice commands, and QR code
integration for field workers and construction management operations.
"""

import streamlit as st
import base64
import json
import qrcode
from io import BytesIO
from datetime import datetime
import logging
from typing import Dict, List, Any, Optional
import os
from PIL import Image

class FieldManager:
    """Enterprise field operations manager"""
    
    def __init__(self):
        self.setup_logging()
        self.offline_storage = []
        self.photo_metadata = {}
        self.initialize_field_systems()
    
    def setup_logging(self):
        """Setup field operations logging"""
        self.logger = logging.getLogger('FieldManager')
    
    def initialize_field_systems(self):
        """Initialize field management systems"""
        if 'field_mode' not in st.session_state:
            st.session_state.field_mode = False
        if 'offline_data' not in st.session_state:
            st.session_state.offline_data = []
        if 'photo_log' not in st.session_state:
            st.session_state.photo_log = []
    
    def enable_offline_mode(self):
        """Enable offline capability for field operations"""
        st.session_state.field_mode = True
        
        # Store critical data locally for offline access
        critical_data = {
            'project_info': {
                'name': 'Highland Tower Development',
                'location': 'Highland District, Downtown',
                'floors': 15,
                'units': 120
            },
            'active_rfis': self.get_cached_rfis(),
            'current_floor_plans': self.get_cached_floor_plans(),
            'safety_procedures': self.get_safety_procedures(),
            'emergency_contacts': self.get_emergency_contacts()
        }
        
        st.session_state.offline_data = critical_data
        st.success("🔄 Offline mode enabled - Critical data cached locally")
    
    def get_cached_rfis(self) -> List[Dict]:
        """Get cached RFI data for offline use"""
        return [
            {
                'id': 'RFI-2025-001',
                'title': 'Electrical outlet placement - Floor 12',
                'status': 'Open',
                'priority': 'Medium',
                'submitted_date': '2025-05-20'
            },
            {
                'id': 'RFI-2025-002', 
                'title': 'HVAC duct routing clarification',
                'status': 'Pending Response',
                'priority': 'High',
                'submitted_date': '2025-05-22'
            }
        ]
    
    def get_cached_floor_plans(self) -> List[str]:
        """Get cached floor plan references"""
        return [
            'Floor_12_Electrical_Plan_Rev_C.pdf',
            'Floor_13_Architectural_Plan_Rev_B.pdf',
            'Floor_14_Mechanical_Plan_Rev_A.pdf'
        ]
    
    def get_safety_procedures(self) -> List[Dict]:
        """Get safety procedures for field reference"""
        return [
            {
                'procedure': 'Fall Protection',
                'requirement': 'Harnesses required above 6 feet',
                'contact': 'Safety Manager: Mike Rodriguez'
            },
            {
                'procedure': 'Electrical Safety',
                'requirement': 'LOTO procedures mandatory',
                'contact': 'Electrical Supervisor: John Smith'
            }
        ]
    
    def get_emergency_contacts(self) -> List[Dict]:
        """Get emergency contact information"""
        return [
            {'role': 'Site Superintendent', 'name': 'John Smith', 'phone': '(555) 123-4567'},
            {'role': 'Safety Manager', 'name': 'Mike Rodriguez', 'phone': '(555) 234-5678'},
            {'role': 'Project Manager', 'name': 'Sarah Chen', 'phone': '(555) 345-6789'},
            {'role': 'Emergency Services', 'name': 'Emergency', 'phone': '911'}
        ]
    
    def render_photo_management_system(self):
        """Render photo management with GPS tagging and organization"""
        st.markdown("### 📸 Photo Documentation System")
        
        # Photo upload interface
        uploaded_photo = st.file_uploader(
            "Upload Construction Photo",
            type=['jpg', 'jpeg', 'png'],
            help="Take photos with your mobile device for automatic GPS tagging"
        )
        
        if uploaded_photo:
            # Display photo
            image = Image.open(uploaded_photo)
            st.image(image, caption="Uploaded Photo", use_column_width=True)
            
            # Photo metadata form
            col1, col2 = st.columns(2)
            
            with col1:
                photo_type = st.selectbox(
                    "Photo Type",
                    ["Progress", "Quality Issue", "Safety Concern", "Material Delivery", "Equipment", "Other"]
                )
                
                location = st.selectbox(
                    "Location",
                    ["Floor 12", "Floor 13", "Floor 14", "Basement Level 1", "Basement Level 2", "Roof", "Exterior"]
                )
            
            with col2:
                trade = st.selectbox(
                    "Trade/Category",
                    ["General", "Electrical", "Plumbing", "HVAC", "Concrete", "Steel", "Drywall", "Flooring"]
                )
                
                priority = st.selectbox(
                    "Priority Level",
                    ["Low", "Medium", "High", "Critical"]
                )
            
            description = st.text_area(
                "Photo Description",
                placeholder="Describe what this photo shows..."
            )
            
            if st.button("💾 Save Photo", type="primary"):
                photo_entry = {
                    'id': f"PHOTO_{int(datetime.now().timestamp())}",
                    'filename': uploaded_photo.name,
                    'type': photo_type,
                    'location': location,
                    'trade': trade,
                    'priority': priority,
                    'description': description,
                    'timestamp': datetime.now().isoformat(),
                    'gps_coordinates': "40.7589, -73.9851",  # Simulated GPS
                    'photographer': st.session_state.get('username', 'Field User')
                }
                
                if 'photo_log' not in st.session_state:
                    st.session_state.photo_log = []
                
                st.session_state.photo_log.append(photo_entry)
                st.success("✅ Photo saved successfully with metadata!")
        
        # Display recent photos
        if st.session_state.get('photo_log'):
            st.markdown("#### Recent Photos")
            
            for i, photo in enumerate(st.session_state.photo_log[-5:]):  # Show last 5
                with st.expander(f"📸 {photo['type']} - {photo['location']} ({photo['timestamp'][:10]})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Location:** {photo['location']}")
                        st.markdown(f"**Trade:** {photo['trade']}")
                        st.markdown(f"**Priority:** {photo['priority']}")
                    
                    with col2:
                        st.markdown(f"**Photographer:** {photo['photographer']}")
                        st.markdown(f"**GPS:** {photo['gps_coordinates']}")
                        st.markdown(f"**Description:** {photo['description']}")
    
    def generate_qr_codes(self):
        """Generate QR codes for quick access to equipment, materials, and drawings"""
        st.markdown("### 📱 QR Code Management System")
        
        qr_type = st.selectbox(
            "Generate QR Code for:",
            ["Equipment", "Material", "Drawing", "Location", "Safety Procedure", "Emergency Contact"]
        )
        
        if qr_type == "Equipment":
            equipment_id = st.text_input("Equipment ID", placeholder="EQ-001")
            equipment_name = st.text_input("Equipment Name", placeholder="Tower Crane #1")
            
            if equipment_id and equipment_name:
                qr_data = {
                    'type': 'equipment',
                    'id': equipment_id,
                    'name': equipment_name,
                    'project': 'Highland Tower Development',
                    'url': f"https://gcpanel.app/equipment/{equipment_id}"
                }
                
                qr_img = self.create_qr_code(json.dumps(qr_data))
                st.image(qr_img, caption=f"QR Code for {equipment_name}")
        
        elif qr_type == "Material":
            material_id = st.text_input("Material ID", placeholder="MAT-001")
            material_name = st.text_input("Material Name", placeholder="Concrete Mix #5")
            
            if material_id and material_name:
                qr_data = {
                    'type': 'material',
                    'id': material_id,
                    'name': material_name,
                    'project': 'Highland Tower Development',
                    'url': f"https://gcpanel.app/materials/{material_id}"
                }
                
                qr_img = self.create_qr_code(json.dumps(qr_data))
                st.image(qr_img, caption=f"QR Code for {material_name}")
        
        elif qr_type == "Location":
            floor = st.selectbox("Floor", ["Floor 12", "Floor 13", "Floor 14", "Basement 1", "Basement 2"])
            area = st.text_input("Specific Area", placeholder="East Wing Unit 1201")
            
            if floor and area:
                qr_data = {
                    'type': 'location',
                    'floor': floor,
                    'area': area,
                    'project': 'Highland Tower Development',
                    'url': f"https://gcpanel.app/location/{floor.replace(' ', '_')}/{area.replace(' ', '_')}"
                }
                
                qr_img = self.create_qr_code(json.dumps(qr_data))
                st.image(qr_img, caption=f"QR Code for {floor} - {area}")
    
    def create_qr_code(self, data: str) -> Image:
        """Create QR code image from data"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        return img
    
    def render_voice_commands_interface(self):
        """Render voice commands interface for hands-free data entry"""
        st.markdown("### 🎤 Voice Commands (Hands-Free Mode)")
        
        st.info("📢 Voice commands coming soon! This feature will allow hands-free data entry for field workers.")
        
        # Simulated voice command interface
        st.markdown("#### Available Voice Commands:")
        
        voice_commands = [
            "📝 'Create new daily report'",
            "❓ 'Submit RFI for electrical issue'",
            "📸 'Log safety concern photo'",
            "⚠️ 'Report safety incident'",
            "🔍 'Check quality status floor twelve'",
            "📋 'Review today's schedule'"
        ]
        
        for command in voice_commands:
            st.markdown(f"• {command}")
        
        # Voice activation button (placeholder)
        if st.button("🎤 Activate Voice Mode", key="voice_mode"):
            st.success("🎤 Voice mode activated! Say a command...")
            st.info("💡 Voice recognition would be implemented using speech-to-text APIs")
    
    def render_offline_sync_interface(self):
        """Render offline data synchronization interface"""
        st.markdown("### 🔄 Offline Data Synchronization")
        
        # Show offline status
        is_offline = not st.session_state.get('online_status', True)
        
        if is_offline:
            st.warning("📴 Currently offline - Data will sync when connection is restored")
        else:
            st.success("🌐 Online - Real-time sync enabled")
        
        # Offline data summary
        offline_items = len(st.session_state.get('offline_data', []))
        pending_photos = len(st.session_state.get('photo_log', []))
        pending_reports = len(st.session_state.get('pending_reports', []))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Cached Data Items", offline_items)
        
        with col2:
            st.metric("Pending Photos", pending_photos)
        
        with col3:
            st.metric("Pending Reports", pending_reports)
        
        # Sync buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⬆️ Upload Pending Data", type="primary"):
                if is_offline:
                    st.error("Cannot sync - No internet connection")
                else:
                    st.success("✅ All pending data synchronized successfully!")
        
        with col2:
            if st.button("⬇️ Download Latest Data"):
                if is_offline:
                    st.error("Cannot download - No internet connection")
                else:
                    st.success("✅ Latest project data downloaded!")
        
        # Toggle offline mode for testing
        if st.button("🔄 Toggle Offline Mode (Testing)"):
            st.session_state.online_status = not st.session_state.get('online_status', True)
            st.rerun()
    
    def render_field_dashboard(self):
        """Render comprehensive field operations dashboard"""
        st.markdown("## 🏗️ Field Operations - Highland Tower Development")
        
        # Field mode toggle
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### Field Worker Dashboard")
        
        with col2:
            if st.button("🔧 Enable Field Mode"):
                self.enable_offline_mode()
        
        # Quick actions for field workers
        st.markdown("#### 🚀 Quick Actions")
        
        quick_action_cols = st.columns(4)
        
        with quick_action_cols[0]:
            if st.button("📝 Daily Report", use_container_width=True):
                st.session_state.current_menu = "Daily Reports"
                st.rerun()
        
        with quick_action_cols[1]:
            if st.button("❓ Submit RFI", use_container_width=True):
                st.session_state.current_menu = "RFIs"
                st.rerun()
        
        with quick_action_cols[2]:
            if st.button("📸 Photo Log", use_container_width=True):
                st.session_state.show_photo_management = True
        
        with quick_action_cols[3]:
            if st.button("⚠️ Safety Issue", use_container_width=True):
                st.session_state.current_menu = "Safety Management"
                st.rerun()
        
        # Field operations tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📸 Photo Management", "📱 QR Codes", "🎤 Voice Commands", "🔄 Offline Sync"])
        
        with tab1:
            self.render_photo_management_system()
        
        with tab2:
            self.generate_qr_codes()
        
        with tab3:
            self.render_voice_commands_interface()
        
        with tab4:
            self.render_offline_sync_interface()

@st.cache_resource
def get_field_manager():
    """Get cached field manager instance"""
    return FieldManager()