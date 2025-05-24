"""
Owner Change Orders (OCOs) Module
Manages change orders that affect the owner contract and automatically updates SOV
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date

class OwnerChangeOrdersModule:
    def __init__(self):
        """Initialize Owner Change Orders module"""
        self.oco_file_path = "data/contracts/owner_change_orders.json"
        self.sov_file_path = "data/cost_management/aia_billing.json"
        self._ensure_data_directories()
        self._initialize_demo_data()
    
    def _ensure_data_directories(self):
        """Ensure data directories exist"""
        os.makedirs(os.path.dirname(self.oco_file_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.sov_file_path), exist_ok=True)
    
    def _initialize_demo_data(self):
        """Initialize demo OCO data if it doesn't exist"""
        if not os.path.exists(self.oco_file_path):
            demo_data = {
                "change_orders": [
                    {
                        "oco_number": "OCO-001",
                        "title": "Additional Elevator Shaft Fireproofing",
                        "description": "Owner requested additional fireproofing in elevator shafts per new fire marshal requirements",
                        "amount": 125000.00,
                        "type": "Addition",
                        "status": "Approved",
                        "date_issued": "2024-03-15",
                        "date_approved": "2024-03-22",
                        "reason": "Code Compliance",
                        "affected_sov_items": ["07 00 00"],
                        "justification": "Required by updated fire code for high-rise buildings",
                        "approved_by": "Highland Development LLC",
                        "contractor_acceptance": "Accepted"
                    },
                    {
                        "oco_number": "OCO-002", 
                        "title": "Upgraded HVAC Controls System",
                        "description": "Upgrade to smart building automation system for energy efficiency",
                        "amount": 275000.00,
                        "type": "Addition",
                        "status": "Approved",
                        "date_issued": "2024-04-08",
                        "date_approved": "2024-04-15",
                        "reason": "Owner Enhancement",
                        "affected_sov_items": ["15 00 00"],
                        "justification": "Owner requested upgrade for LEED certification and operating cost reduction",
                        "approved_by": "Highland Development LLC",
                        "contractor_acceptance": "Accepted"
                    },
                    {
                        "oco_number": "OCO-003",
                        "title": "Premium Lobby Finishes",
                        "description": "Upgrade lobby finishes from standard to premium materials",
                        "amount": 185000.00,
                        "type": "Addition",
                        "status": "Approved", 
                        "date_issued": "2024-04-20",
                        "date_approved": "2024-04-28",
                        "reason": "Design Enhancement",
                        "affected_sov_items": ["09 00 00"],
                        "justification": "Owner upgrade to attract premium tenants",
                        "approved_by": "Highland Development LLC",
                        "contractor_acceptance": "Accepted"
                    },
                    {
                        "oco_number": "OCO-004",
                        "title": "Rooftop Solar Panel Infrastructure",
                        "description": "Add structural support and electrical infrastructure for future solar installation",
                        "amount": 95000.00,
                        "type": "Addition",
                        "status": "Pending Approval",
                        "date_issued": "2024-05-10",
                        "date_approved": None,
                        "reason": "Future Proofing",
                        "affected_sov_items": ["05 00 00", "16 00 00"],
                        "justification": "Owner wants future solar capability without roof modifications",
                        "approved_by": None,
                        "contractor_acceptance": "Under Review"
                    },
                    {
                        "oco_number": "OCO-005",
                        "title": "Delete Alternate Paving Option",
                        "description": "Remove decorative paving upgrade, use standard concrete",
                        "amount": -45000.00,
                        "type": "Deletion",
                        "status": "Approved",
                        "date_issued": "2024-05-05",
                        "date_approved": "2024-05-12",
                        "reason": "Cost Reduction",
                        "affected_sov_items": ["03 00 00"],
                        "justification": "Owner cost savings measure",
                        "approved_by": "Highland Development LLC",
                        "contractor_acceptance": "Accepted"
                    }
                ]
            }
            
            with open(self.oco_file_path, 'w') as f:
                json.dump(demo_data, f, indent=2)
    
    def _load_oco_data(self):
        """Load OCO data"""
        try:
            with open(self.oco_file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"change_orders": []}
    
    def _save_oco_data(self, data):
        """Save OCO data"""
        with open(self.oco_file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _update_sov_from_oco(self, oco_data):
        """Update Schedule of Values based on approved change orders"""
        try:
            # Load current SOV data
            with open(self.sov_file_path, 'r') as f:
                sov_data = json.load(f)
            
            # Calculate total approved change orders
            approved_cos = [co for co in oco_data["change_orders"] if co["status"] == "Approved"]
            total_change_orders = sum([co["amount"] for co in approved_cos])
            
            # Update project info
            original_amount = 45500000.00  # Base contract amount
            sov_data["project_info"]["change_order_amount"] = total_change_orders
            sov_data["project_info"]["adjusted_contract_amount"] = original_amount + total_change_orders
            
            # Save updated SOV
            with open(self.sov_file_path, 'w') as f:
                json.dump(sov_data, f, indent=2)
                
            return True
        except Exception as e:
            st.error(f"Error updating SOV: {str(e)}")
            return False
    
    def render_oco_dashboard(self):
        """Render OCO dashboard with summary metrics"""
        st.markdown("### 💼 Owner Change Orders (OCOs)")
        
        data = self._load_oco_data()
        change_orders = data.get("change_orders", [])
        
        if not change_orders:
            st.info("No owner change orders found.")
            return
        
        # Calculate summary metrics
        approved_cos = [co for co in change_orders if co["status"] == "Approved"]
        pending_cos = [co for co in change_orders if co["status"] == "Pending Approval"]
        
        total_approved_amount = sum([co["amount"] for co in approved_cos])
        total_pending_amount = sum([co["amount"] for co in pending_cos])
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total OCOs", len(change_orders))
        
        with col2:
            st.metric("Approved Amount", f"${total_approved_amount:,.2f}")
        
        with col3:
            st.metric("Pending Amount", f"${total_pending_amount:,.2f}")
        
        with col4:
            st.metric("Approved Count", len(approved_cos))
        
        # OCO Table
        st.markdown("#### Change Orders List")
        
        if change_orders:
            # Create DataFrame for display
            df = pd.DataFrame(change_orders)
            
            # Format for display
            display_df = df.copy()
            display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:,.2f}")
            
            # Status color coding
            def status_color(status):
                if status == "Approved":
                    return "🟢 Approved"
                elif status == "Pending Approval":
                    return "🟡 Pending"
                else:
                    return f"⚪ {status}"
            
            display_df['status'] = display_df['status'].apply(status_color)
            
            # Select columns for display
            display_columns = ['oco_number', 'title', 'type', 'amount', 'status', 'date_issued']
            display_df = display_df[display_columns]
            
            # Rename columns
            display_df.columns = ['OCO #', 'Title', 'Type', 'Amount', 'Status', 'Date Issued']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    def render_new_oco_form(self):
        """Render form for creating new OCO"""
        st.markdown("#### ➕ Create New Owner Change Order")
        
        with st.form("new_oco_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                oco_number = st.text_input("OCO Number*", placeholder="OCO-006")
                title = st.text_input("Title*", placeholder="Description of change")
                oco_type = st.selectbox("Type*", ["Addition", "Deletion", "Modification"])
                amount = st.number_input("Amount*", step=1000.0, format="%.2f")
            
            with col2:
                reason = st.selectbox("Reason*", [
                    "Code Compliance", "Owner Enhancement", "Design Enhancement", 
                    "Cost Reduction", "Future Proofing", "Design Error", "Other"
                ])
                date_issued = st.date_input("Date Issued*", value=date.today())
                approved_by = st.text_input("Approved By", placeholder="Highland Development LLC")
                contractor_acceptance = st.selectbox("Contractor Status", [
                    "Under Review", "Accepted", "Rejected", "Negotiating"
                ])
            
            description = st.text_area("Description*", placeholder="Detailed description of the change order")
            justification = st.text_area("Justification*", placeholder="Business justification for this change")
            
            # SOV Items affected
            sov_items = st.multiselect("Affected SOV Items", [
                "01 00 00 - General Requirements",
                "02 00 00 - Existing Conditions", 
                "03 00 00 - Concrete",
                "04 00 00 - Masonry",
                "05 00 00 - Metals",
                "06 00 00 - Wood, Plastics, and Composites",
                "07 00 00 - Thermal and Moisture Protection",
                "08 00 00 - Openings",
                "09 00 00 - Finishes",
                "10 00 00 - Specialties",
                "11 00 00 - Equipment",
                "12 00 00 - Furnishings",
                "13 00 00 - Special Construction",
                "14 00 00 - Conveying Equipment",
                "15 00 00 - Mechanical",
                "16 00 00 - Electrical"
            ])
            
            submit_button = st.form_submit_button("Create OCO", type="primary")
            
            if submit_button:
                if oco_number and title and amount != 0 and description and justification:
                    # Create new OCO
                    new_oco = {
                        "oco_number": oco_number,
                        "title": title,
                        "description": description,
                        "amount": amount,
                        "type": oco_type,
                        "status": "Pending Approval",
                        "date_issued": date_issued.strftime("%Y-%m-%d"),
                        "date_approved": None,
                        "reason": reason,
                        "affected_sov_items": [item.split(" - ")[0] for item in sov_items],
                        "justification": justification,
                        "approved_by": approved_by if approved_by else None,
                        "contractor_acceptance": contractor_acceptance
                    }
                    
                    # Load current data and add new OCO
                    data = self._load_oco_data()
                    data["change_orders"].append(new_oco)
                    self._save_oco_data(data)
                    
                    st.success(f"Owner Change Order {oco_number} created successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields marked with *")
    
    def render_oco_approval_workflow(self):
        """Render OCO approval workflow"""
        st.markdown("#### ⚡ OCO Approval Workflow")
        
        data = self._load_oco_data()
        pending_cos = [co for co in data["change_orders"] if co["status"] == "Pending Approval"]
        
        if pending_cos:
            for co in pending_cos:
                with st.expander(f"🟡 {co['oco_number']} - {co['title']} (${co['amount']:,.2f})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.text(f"Type: {co['type']}")
                        st.text(f"Reason: {co['reason']}")
                        st.text(f"Date Issued: {co['date_issued']}")
                        st.text_area("Description", value=co['description'], disabled=True, key=f"desc_{co['oco_number']}")
                    
                    with col2:
                        st.text(f"Amount: ${co['amount']:,.2f}")
                        st.text(f"Contractor: {co['contractor_acceptance']}")
                        st.text(f"Affected SOV: {', '.join(co['affected_sov_items'])}")
                        st.text_area("Justification", value=co['justification'], disabled=True, key=f"just_{co['oco_number']}")
                    
                    # Approval actions
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"✅ Approve {co['oco_number']}", type="primary", key=f"approve_{co['oco_number']}"):
                            # Update status
                            for change_order in data["change_orders"]:
                                if change_order["oco_number"] == co["oco_number"]:
                                    change_order["status"] = "Approved"
                                    change_order["date_approved"] = datetime.now().strftime("%Y-%m-%d")
                                    break
                            
                            self._save_oco_data(data)
                            self._update_sov_from_oco(data)
                            st.success(f"OCO {co['oco_number']} approved and SOV updated!")
                            st.rerun()
                    
                    with col2:
                        if st.button(f"❌ Reject {co['oco_number']}", key=f"reject_{co['oco_number']}"):
                            # Update status
                            for change_order in data["change_orders"]:
                                if change_order["oco_number"] == co["oco_number"]:
                                    change_order["status"] = "Rejected"
                                    break
                            
                            self._save_oco_data(data)
                            st.warning(f"OCO {co['oco_number']} rejected")
                            st.rerun()
                    
                    with col3:
                        if st.button(f"📝 Request Info {co['oco_number']}", key=f"info_{co['oco_number']}"):
                            st.info("Information request sent to contractor")
        else:
            st.info("No pending change orders for approval")
    
    def render(self):
        """Main render function for Owner Change Orders"""
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["OCO Dashboard", "Create New OCO", "Approval Workflow"])
        
        with tab1:
            self.render_oco_dashboard()
        
        with tab2:
            self.render_new_oco_form()
        
        with tab3:
            self.render_oco_approval_workflow()
        
        # SOV Update notification
        st.markdown("---")
        st.info("💡 **Note**: Approved Owner Change Orders automatically update the Schedule of Values in Cost Management → AIA G702/G703 Billing")

def render_owner_change_orders():
    """Main render function for OCO module"""
    oco_module = OwnerChangeOrdersModule()
    oco_module.render()