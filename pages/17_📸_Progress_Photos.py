"""
Progress Photos Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Progress Photos - gcPanel", page_icon="📸", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("📸 Progress Photos")
st.markdown("Highland Tower Development - Construction Progress Documentation")
st.markdown("---")

if 'progress_photos' not in st.session_state:
    st.session_state.progress_photos = []

tab1, tab2, tab3 = st.tabs(["🖼️ Photo Gallery", "📸 Upload Photos", "📊 Photo Log"])

with tab1:
    st.subheader("🖼️ Progress Photo Gallery")
    
    if st.session_state.progress_photos:
        df = pd.DataFrame(st.session_state.progress_photos)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search photos...", key="progress_photos_search_1")
        with col2:
            location_filter = st.selectbox("Location", ["All", "Lobby", "Floor 2", "Floor 3", "Roof"])
        with col3:
            date_filter = st.date_input("Filter by Date")
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if location_filter != "All":
            filtered_df = filtered_df[filtered_df['location'] == location_filter]
        
        st.write(f"**Total Photos:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No progress photos uploaded. Upload your first photo in the Upload tab!")

with tab2:
    st.subheader("📸 Upload Progress Photos")
    
    with st.form("photo_upload_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            photo_date = st.date_input("Photo Date", value=date.today())
            location = st.text_input("Location", placeholder="Building area, floor, grid reference")
            photographer = st.text_input("Photographer", value=st.session_state.get('user_name', ''))
            weather = st.selectbox("Weather", ["Sunny", "Cloudy", "Rainy", "Snowy", "Overcast"])
        
        with col2:
            category = st.selectbox("Category", 
                ["General Progress", "Foundation", "Structure", "MEP", "Finishes", "Safety", "Quality Issues"])
            work_activity = st.text_input("Work Activity", placeholder="Current construction activity")
            equipment_visible = st.text_input("Equipment Visible", placeholder="Cranes, equipment in photo")
            crew_count = st.number_input("Crew Count", min_value=0, max_value=100, value=0)
        
        description = st.text_area("Photo Description", placeholder="Describe what is shown in the photos...")
        
        # File upload placeholder
        uploaded_files = st.file_uploader("Choose photo files", accept_multiple_files=True, 
                                        type=['jpg', 'jpeg', 'png', 'bmp'])
        
        submitted = st.form_submit_button("📸 Upload Photos", type="primary", use_container_width=True)
        
        if submitted and location:
            photo_count = len(uploaded_files) if uploaded_files else 1
            new_photo_entry = {
                "id": f"PH-{len(st.session_state.progress_photos) + 1:03d}",
                "date": str(photo_date),
                "location": location,
                "photographer": photographer,
                "weather": weather,
                "category": category,
                "work_activity": work_activity,
                "equipment_visible": equipment_visible,
                "crew_count": crew_count,
                "description": description,
                "photo_count": photo_count,
                "upload_time": str(datetime.now().strftime("%H:%M"))
            }
            st.session_state.progress_photos.insert(0, new_photo_entry)
            st.success(f"Progress photos {new_photo_entry['id']} uploaded successfully!")
            st.rerun()

with tab2:
    st.subheader("🖼️ Photo Gallery")
    
    if st.session_state.progress_photos:
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("Search photos...")
        with col2:
            category_filter = st.selectbox("Filter by Category", ["All", "General Progress", "Foundation", "Structure"])
        
        # Display photo entries in grid layout
        photos_per_row = 3
        filtered_photos = st.session_state.progress_photos.copy()
        
        if search_term:
            filtered_photos = [p for p in filtered_photos if search_term.lower() in str(p).lower()]
        
        if category_filter != "All":
            filtered_photos = [p for p in filtered_photos if p['category'] == category_filter]
        
        if filtered_photos:
            for i in range(0, len(filtered_photos), photos_per_row):
                cols = st.columns(photos_per_row)
                for j, photo in enumerate(filtered_photos[i:i+photos_per_row]):
                    with cols[j]:
                        st.markdown(f"**{photo['id']}**")
                        st.write(f"📅 {photo['date']}")
                        st.write(f"📍 {photo['location']}")
                        st.write(f"📸 {photo['photo_count']} photos")
                        
                        # Placeholder for actual photo display
                        st.markdown("""
                        <div style="height: 200px; background-color: #f0f0f0; border: 2px dashed #ccc; 
                                    display: flex; align-items: center; justify-content: center; border-radius: 5px;">
                            <div style="text-align: center; color: #666;">
                                <p>📸</p>
                                <p>Photo Preview</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("Details"):
                            st.write(f"Category: {photo['category']}")
                            st.write(f"Activity: {photo['work_activity']}")
                            st.write(f"Description: {photo['description']}")
        else:
            st.info("No photos match your search criteria.")
    else:
        st.info("No progress photos uploaded yet. Upload your first photos above!")

with tab3:
    st.subheader("📊 Photo Documentation Log")
    
    if st.session_state.progress_photos:
        df = pd.DataFrame(st.session_state.progress_photos)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search log entries...")
        with col2:
            category_filter = st.selectbox("Category Filter", ["All", "General Progress", "Foundation", "Structure"])
        with col3:
            date_filter = st.date_input("Filter by Date")
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
        
        st.write(f"**Total Photo Entries:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
            
            # Summary statistics
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_entries = len(filtered_df)
                st.metric("Photo Sessions", total_entries)
            
            with col2:
                total_photos = filtered_df['photo_count'].sum()
                st.metric("Total Photos", total_photos)
            
            with col3:
                avg_photos = filtered_df['photo_count'].mean()
                st.metric("Avg Photos/Session", f"{avg_photos:.1f}")
            
            with col4:
                most_common_category = filtered_df['category'].mode().iloc[0] if len(filtered_df) > 0 else "N/A"
                st.metric("Most Common Category", most_common_category)
    else:
        st.info("No photo documentation available. Upload your first photos above!")