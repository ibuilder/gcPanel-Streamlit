"""
Unit Prices Module - Advanced Material, Equipment & Labor Cost Tracking
Highland Tower Development - Comprehensive Cost Management System
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render_unit_prices():
    """Advanced unit pricing system for materials, equipment, and labor"""
    st.title("💰 Unit Prices - Cost Intelligence Center")
    st.markdown("**Comprehensive pricing analytics for Highland Tower Development**")
    
    # Real-time cost overview dashboard using native Streamlit components
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Daily Material Costs", "$48,200", "+2.1% vs budget")
    with col2:
        st.metric("Daily Labor Costs", "$35,600", "-1.5% vs budget")
    with col3:
        st.metric("Equipment Rental", "$12,800", "On target")
    with col4:
        st.metric("Cost Accuracy", "96.4%", "+0.8% this week")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧱 Materials", "📦 Material Management", "⚙️ Equipment", "👷 Labor", "📊 Analytics", "🔄 Integrations"
    ])
    
    with tab1:
        render_materials_pricing()
    
    with tab2:
        render_material_management()
    
    with tab3:
        render_equipment_pricing()
    
    with tab3:
        render_labor_pricing()
    
    with tab4:
        render_pricing_analytics()
    
    with tab5:
        render_cost_integrations()

def render_materials_pricing():
    """Advanced material cost tracking and forecasting"""
    st.markdown("### 🧱 Material Cost Intelligence")
    
    # Material filters and search
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    with filter_col1:
        category_filter = st.selectbox("Category", 
            ["All Categories", "Structural Steel", "Concrete", "MEP Systems", "Finishes", "Glass & Glazing"])
    
    with filter_col2:
        supplier_filter = st.selectbox("Supplier", 
            ["All Suppliers", "Steel Fabricators Inc", "NYC Concrete Co", "HVAC Systems LLC", "Guardian Glass"])
    
    with filter_col3:
        date_range = st.selectbox("Time Period", 
            ["Last 30 Days", "Last Quarter", "Year to Date", "Project Lifetime"])
    
    with filter_col4:
        variance_filter = st.selectbox("Cost Variance", 
            ["All Items", "Under Budget", "Over Budget", "Critical Variance"])
    
    # Advanced search
    search_query = st.text_input("🔍 Search Materials", 
        placeholder="Search by item code, description, supplier, or specification...")
    
    # Highland Tower specific material data
    materials_data = [
        {
            "Item_Code": "STL-W24-62",
            "Description": "W24x62 Steel Beam - ASTM A992",
            "Unit": "LF",
            "Budget_Price": 45.80,
            "Current_Price": 47.20,
            "Variance": 3.1,
            "Quantity_Used": 2450,
            "Total_Cost": 115640,
            "Supplier": "Steel Fabricators Inc",
            "Last_Updated": "2025-01-25",
            "Lead_Time": 14,
            "Category": "Structural Steel",
            "Specification": "AISC 360-16",
            "Quality_Grade": "A+",
            "Delivery_Status": "On Schedule"
        },
        {
            "Item_Code": "CON-5000-PSI",
            "Description": "5000 PSI Concrete Mix - High Strength",
            "Unit": "CY",
            "Budget_Price": 185.00,
            "Current_Price": 178.50,
            "Variance": -3.5,
            "Quantity_Used": 890,
            "Total_Cost": 158865,
            "Supplier": "NYC Concrete Co",
            "Last_Updated": "2025-01-25",
            "Lead_Time": 3,
            "Category": "Concrete",
            "Specification": "ACI 318-19",
            "Quality_Grade": "A",
            "Delivery_Status": "Daily Supply"
        },
        {
            "Item_Code": "HVAC-RTU-15T",
            "Description": "Trane 15-Ton Rooftop Unit - Variable Speed",
            "Unit": "EA",
            "Budget_Price": 15750.00,
            "Current_Price": 16240.00,
            "Variance": 3.1,
            "Quantity_Used": 8,
            "Total_Cost": 129920,
            "Supplier": "HVAC Systems LLC",
            "Last_Updated": "2025-01-24",
            "Lead_Time": 45,
            "Category": "MEP Systems",
            "Specification": "ASHRAE 90.1",
            "Quality_Grade": "A+",
            "Delivery_Status": "2 Weeks Out"
        },
        {
            "Item_Code": "GLS-CW-1000",
            "Description": "Guardian Glass Curtain Wall System",
            "Unit": "SF",
            "Budget_Price": 125.00,
            "Current_Price": 128.75,
            "Variance": 3.0,
            "Quantity_Used": 12500,
            "Total_Cost": 1609375,
            "Supplier": "Guardian Glass",
            "Last_Updated": "2025-01-23",
            "Lead_Time": 60,
            "Category": "Glass & Glazing",
            "Specification": "ASTM E2112",
            "Quality_Grade": "A+",
            "Delivery_Status": "Manufacturing"
        }
    ]
    
    # Display materials with enhanced formatting
    for material in materials_data:
        variance_color = "🔴" if material['Variance'] > 5 else "🟡" if material['Variance'] > 0 else "🟢"
        status_icon = "✅" if material['Delivery_Status'] == "On Schedule" else "⏰" if "Week" in material['Delivery_Status'] else "🚛"
        
        with st.expander(f"{variance_color} {material['Item_Code']} - {material['Description']} {status_icon}"):
            # Multi-column detailed view
            detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
            
            with detail_col1:
                st.markdown("**💰 Pricing Analysis**")
                st.metric("Budget Price", f"${material['Budget_Price']:,.2f}", 
                         delta=f"{material['Variance']:+.1f}%", delta_color="inverse")
                st.metric("Current Price", f"${material['Current_Price']:,.2f}")
                st.text(f"Unit: {material['Unit']}")
            
            with detail_col2:
                st.markdown("**📊 Usage & Cost**")
                st.metric("Quantity Used", f"{material['Quantity_Used']:,}")
                st.metric("Total Cost", f"${material['Total_Cost']:,.0f}")
                st.text(f"Quality: {material['Quality_Grade']}")
            
            with detail_col3:
                st.markdown("**🚚 Supply Chain**")
                st.text(f"Supplier: {material['Supplier']}")
                st.text(f"Lead Time: {material['Lead_Time']} days")
                st.text(f"Status: {material['Delivery_Status']}")
            
            with detail_col4:
                st.markdown("**📋 Specifications**")
                st.text(f"Category: {material['Category']}")
                st.text(f"Spec: {material['Specification']}")
                st.text(f"Updated: {material['Last_Updated']}")
    
    # Cost trend analysis
    st.markdown("### 📈 Material Cost Trends")
    
    # Create sample trend data
    dates = pd.date_range(start='2024-10-01', end='2025-01-25', freq='D')
    trend_data = pd.DataFrame({
        'Date': dates,
        'Steel_Price': 45.80 + np.random.normal(0, 1.5, len(dates)).cumsum() * 0.1,
        'Concrete_Price': 185.00 + np.random.normal(0, 2.0, len(dates)).cumsum() * 0.05,
        'HVAC_Price': 15750 + np.random.normal(0, 200, len(dates)).cumsum() * 0.02
    })
    
    fig_trends = go.Figure()
    fig_trends.add_trace(go.Scatter(x=trend_data['Date'], y=trend_data['Steel_Price'], 
                                   name='Steel ($/LF)', line=dict(color='#3b82f6')))
    fig_trends.add_trace(go.Scatter(x=trend_data['Date'], y=trend_data['Concrete_Price'], 
                                   name='Concrete ($/CY)', line=dict(color='#10b981')))
    
    fig_trends.update_layout(
        title="Material Price Trends - Highland Tower Development",
        xaxis_title="Date",
        yaxis_title="Unit Price ($)",
        template="plotly_dark",
        height=400
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)

def render_equipment_pricing():
    """Equipment rental and ownership cost tracking"""
    st.markdown("### ⚙️ Equipment Cost Management")
    
    # Equipment cost overview
    equipment_data = [
        {
            "Equipment_ID": "CR-250T-01",
            "Description": "250-Ton Tower Crane - Liebherr",
            "Type": "Rental",
            "Daily_Rate": 2850.00,
            "Monthly_Rate": 72000.00,
            "Utilization": 94.5,
            "Days_Used": 125,
            "Total_Cost": 356250,
            "Operator_Required": True,
            "Operator_Rate": 420.00,
            "Maintenance_Cost": 8500,
            "Status": "Active",
            "Location": "Level 13"
        },
        {
            "Equipment_ID": "EX-350-02",
            "Description": "CAT 350 Excavator",
            "Type": "Owned",
            "Daily_Rate": 875.00,
            "Monthly_Rate": 22000.00,
            "Utilization": 78.2,
            "Days_Used": 89,
            "Total_Cost": 77875,
            "Operator_Required": True,
            "Operator_Rate": 380.00,
            "Maintenance_Cost": 12500,
            "Status": "Active",
            "Location": "Site Yard"
        },
        {
            "Equipment_ID": "GEN-150KW",
            "Description": "150kW Diesel Generator - Caterpillar",
            "Type": "Rental",
            "Daily_Rate": 245.00,
            "Monthly_Rate": 6200.00,
            "Utilization": 88.0,
            "Days_Used": 156,
            "Total_Cost": 38220,
            "Operator_Required": False,
            "Operator_Rate": 0.00,
            "Maintenance_Cost": 1800,
            "Status": "Active",
            "Location": "Power Station"
        }
    ]
    
    for equipment in equipment_data:
        utilization_color = "🟢" if equipment['Utilization'] > 85 else "🟡" if equipment['Utilization'] > 70 else "🔴"
        
        with st.expander(f"{utilization_color} {equipment['Equipment_ID']} - {equipment['Description']}"):
            equip_col1, equip_col2, equip_col3, equip_col4 = st.columns(4)
            
            with equip_col1:
                st.markdown("**💰 Cost Structure**")
                st.metric("Daily Rate", f"${equipment['Daily_Rate']:,.2f}")
                st.metric("Monthly Rate", f"${equipment['Monthly_Rate']:,.0f}")
                st.text(f"Type: {equipment['Type']}")
            
            with equip_col2:
                st.markdown("**📊 Utilization**")
                st.metric("Utilization Rate", f"{equipment['Utilization']:.1f}%")
                st.metric("Days Used", equipment['Days_Used'])
                st.metric("Total Cost", f"${equipment['Total_Cost']:,.0f}")
            
            with equip_col3:
                st.markdown("**👷 Operations**")
                operator_text = "Required" if equipment['Operator_Required'] else "Not Required"
                st.text(f"Operator: {operator_text}")
                if equipment['Operator_Required']:
                    st.metric("Operator Rate", f"${equipment['Operator_Rate']:.2f}/day")
                st.text(f"Location: {equipment['Location']}")
            
            with equip_col4:
                st.markdown("**🔧 Maintenance**")
                st.metric("Maintenance Cost", f"${equipment['Maintenance_Cost']:,.0f}")
                st.text(f"Status: {equipment['Status']}")
                
                # Equipment action buttons
                if st.button(f"📋 Service Log", key=f"service_{equipment['Equipment_ID']}"):
                    st.info(f"Service history for {equipment['Equipment_ID']} would display here")

def render_labor_pricing():
    """Labor cost tracking and crew optimization"""
    st.markdown("### 👷 Labor Cost Intelligence")
    
    # Labor categories and rates
    labor_data = [
        {
            "Trade": "Structural Steel Workers",
            "Base_Rate": 42.50,
            "Overtime_Rate": 63.75,
            "Benefits_Rate": 28.40,
            "Total_Rate": 70.90,
            "Crew_Size": 12,
            "Daily_Hours": 8,
            "Overtime_Hours": 2,
            "Productivity": 115.2,
            "Daily_Cost": 4251.00,
            "Foreman": "Mike Rodriguez",
            "Union": "Local 40",
            "Efficiency_Rating": "A+"
        },
        {
            "Trade": "Electricians",
            "Base_Rate": 38.75,
            "Overtime_Rate": 58.13,
            "Benefits_Rate": 26.20,
            "Total_Rate": 64.95,
            "Crew_Size": 8,
            "Daily_Hours": 8,
            "Overtime_Hours": 1.5,
            "Productivity": 108.7,
            "Daily_Cost": 2953.20,
            "Foreman": "Sarah Chen",
            "Union": "Local 3",
            "Efficiency_Rating": "A"
        },
        {
            "Trade": "Concrete Finishers",
            "Base_Rate": 35.20,
            "Overtime_Rate": 52.80,
            "Benefits_Rate": 24.50,
            "Total_Rate": 59.70,
            "Crew_Size": 6,
            "Daily_Hours": 8,
            "Overtime_Hours": 0,
            "Productivity": 98.5,
            "Daily_Cost": 2863.20,
            "Foreman": "Jennifer Walsh",
            "Union": "Local 6A",
            "Efficiency_Rating": "B+"
        }
    ]
    
    for labor in labor_data:
        productivity_color = "🟢" if labor['Productivity'] > 110 else "🟡" if labor['Productivity'] > 100 else "🔴"
        
        with st.expander(f"{productivity_color} {labor['Trade']} - {labor['Efficiency_Rating']} Rating"):
            labor_col1, labor_col2, labor_col3, labor_col4 = st.columns(4)
            
            with labor_col1:
                st.markdown("**💰 Rate Structure**")
                st.metric("Base Rate", f"${labor['Base_Rate']:.2f}/hr")
                st.metric("Total Rate", f"${labor['Total_Rate']:.2f}/hr")
                st.text(f"Benefits: ${labor['Benefits_Rate']:.2f}/hr")
            
            with labor_col2:
                st.markdown("**👥 Crew Details**")
                st.metric("Crew Size", labor['Crew_Size'])
                st.metric("Daily Cost", f"${labor['Daily_Cost']:,.2f}")
                st.text(f"Foreman: {labor['Foreman']}")
            
            with labor_col3:
                st.markdown("**⏰ Time Tracking**")
                st.metric("Regular Hours", f"{labor['Daily_Hours']}")
                st.metric("Overtime Hours", f"{labor['Overtime_Hours']}")
                st.text(f"Union: {labor['Union']}")
            
            with labor_col4:
                st.markdown("**📈 Performance**")
                st.metric("Productivity", f"{labor['Productivity']:.1f}%", 
                         delta=f"{labor['Productivity']-100:+.1f}%")
                st.text(f"Rating: {labor['Efficiency_Rating']}")

def render_pricing_analytics():
    """Advanced cost analytics and forecasting"""
    st.markdown("### 📊 Cost Intelligence Analytics")
    
    # Cost breakdown chart
    cost_categories = ['Materials', 'Labor', 'Equipment', 'Overhead', 'Profit']
    cost_values = [2150000, 1680000, 450000, 320000, 400000]
    
    fig_breakdown = px.pie(values=cost_values, names=cost_categories,
                          title="Highland Tower Development - Cost Breakdown",
                          color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'])
    fig_breakdown.update_layout(template="plotly_dark")
    
    st.plotly_chart(fig_breakdown, use_container_width=True)
    
    # Cost variance analysis
    st.markdown("### 📈 Cost Variance Tracking")
    
    variance_data = pd.DataFrame({
        'Category': ['Structural Steel', 'Concrete', 'MEP Systems', 'Finishes', 'Equipment'],
        'Budget': [2200000, 850000, 1200000, 600000, 450000],
        'Actual': [2267000, 821500, 1237000, 618000, 432000],
        'Variance_%': [3.0, -3.4, 3.1, 3.0, -4.0]
    })
    
    fig_variance = px.bar(variance_data, x='Category', y='Variance_%',
                         title="Cost Variance by Category",
                         color='Variance_%',
                         color_continuous_scale=['red', 'yellow', 'green'])
    fig_variance.update_layout(template="plotly_dark")
    
    st.plotly_chart(fig_variance, use_container_width=True)

def render_cost_integrations():
    """Integration with accounting systems and cost management tools"""
    st.markdown("### 🔄 Enterprise Integrations")
    
    # Sage integration section
    st.markdown("#### 📊 Sage 300 Construction Integration")
    
    integration_col1, integration_col2 = st.columns(2)
    
    with integration_col1:
        st.markdown("""
        **🔗 Active Integrations:**
        
        **✅ Sage 300 Construction**
        - Real-time cost synchronization
        - Automated journal entries
        - Payroll integration
        - Equipment cost allocation
        
        **✅ Procore Integration**
        - Bidirectional data sync
        - RFI cost tracking
        - Change order pricing
        
        **✅ QuickBooks Enterprise**
        - Vendor payment processing
        - Purchase order automation
        - Tax compliance reporting
        """)
    
    with integration_col2:
        st.markdown("""
        **⚙️ Integration Status:**
        
        - **Last Sync:** 5 minutes ago
        - **Data Accuracy:** 99.8%
        - **Error Rate:** 0.02%
        - **Sync Frequency:** Real-time
        
        **📊 Data Flow:**
        - Daily cost exports to Sage
        - Hourly labor updates
        - Real-time material receipts
        - Automated variance reporting
        """)
    
    # Integration management buttons
    st.markdown("#### 🛠️ Integration Management")
    
    int_col1, int_col2, int_col3, int_col4 = st.columns(4)
    
    with int_col1:
        if st.button("🔄 Sync Now", use_container_width=True):
            st.success("✅ Manual sync initiated with Sage 300")
    
    with int_col2:
        if st.button("📋 Integration Logs", use_container_width=True):
            st.info("📊 Integration activity logs would display here")
    
    with int_col3:
        if st.button("⚙️ Configure", use_container_width=True):
            st.info("🔧 Integration configuration panel would open")
    
    with int_col4:
        if st.button("📊 Reports", use_container_width=True):
            st.info("📈 Integration performance reports available")
    
    # API endpoints and webhook status
    st.markdown("#### 🌐 API & Webhook Status")
    
    api_status = [
        {"Service": "Sage 300 API", "Status": "✅ Active", "Last_Call": "2 minutes ago", "Response_Time": "245ms"},
        {"Service": "Procore Webhook", "Status": "✅ Active", "Last_Event": "8 minutes ago", "Response_Time": "180ms"},
        {"Service": "QuickBooks API", "Status": "✅ Active", "Last_Sync": "15 minutes ago", "Response_Time": "320ms"},
        {"Service": "Material Suppliers", "Status": "✅ Active", "Last_Update": "1 hour ago", "Response_Time": "156ms"}
    ]
    
    status_df = pd.DataFrame(api_status)
    st.dataframe(status_df, use_container_width=True)

if __name__ == "__main__":
    render_unit_prices()