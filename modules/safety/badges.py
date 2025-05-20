"""
Safety Badges module for gamification of safety compliance.

This module provides functionality for awarding, tracking, and displaying
safety achievement badges to encourage positive safety behaviors on the project.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Define badge types and criteria
BADGE_DEFINITIONS = [
    {
        "id": "safety_champion",
        "name": "Safety Champion",
        "description": "Awarded for identifying and addressing 5 or more safety hazards",
        "icon": "🛡️",
        "tier": "gold",
        "points": 100
    },
    {
        "id": "quick_reporter",
        "name": "Quick Reporter",
        "description": "Awarded for reporting incidents within 24 hours of occurrence",
        "icon": "⚡",
        "tier": "silver",
        "points": 50
    },
    {
        "id": "zero_harm",
        "name": "Zero Harm Hero",
        "description": "Awarded for teams with zero incidents for 30+ consecutive days",
        "icon": "🏆",
        "tier": "gold",
        "points": 150
    },
    {
        "id": "safety_mentor",
        "name": "Safety Mentor",
        "description": "Awarded for conducting 3 or more safety training sessions",
        "icon": "🎓",
        "tier": "gold",
        "points": 100
    },
    {
        "id": "prevention_pro",
        "name": "Prevention Pro",
        "description": "Awarded for implementing preventive measures that avoid potential incidents",
        "icon": "🛠️",
        "tier": "silver",
        "points": 75
    },
    {
        "id": "ppe_perfect",
        "name": "PPE Perfect",
        "description": "Awarded for perfect PPE compliance during inspections",
        "icon": "👷",
        "tier": "bronze",
        "points": 25
    },
    {
        "id": "safety_innovator",
        "name": "Safety Innovator",
        "description": "Awarded for suggesting safety improvements that are implemented",
        "icon": "💡",
        "tier": "gold",
        "points": 100
    },
    {
        "id": "team_player",
        "name": "Safety Team Player",
        "description": "Awarded for actively participating in safety meetings and drills",
        "icon": "🤝",
        "tier": "bronze",
        "points": 25
    },
    {
        "id": "first_responder",
        "name": "First Responder",
        "description": "Awarded for properly responding to emergency situations",
        "icon": "🚑",
        "tier": "silver",
        "points": 50
    },
    {
        "id": "safety_streak",
        "name": "Safety Streak",
        "description": "Awarded for personal record of 60+ days without safety violations",
        "icon": "🔥",
        "tier": "gold",
        "points": 125
    }
]

# Generate sample user badge data
def generate_sample_badges():
    """Generate sample badge data for demonstration"""
    users = [
        {"id": "U001", "name": "Alex Johnson", "role": "Site Supervisor", "team": "Management"},
        {"id": "U002", "name": "Maria Garcia", "role": "Safety Officer", "team": "Safety"},
        {"id": "U003", "name": "David Kim", "role": "Foreman", "team": "Structural"},
        {"id": "U004", "name": "Sarah Williams", "role": "Engineer", "team": "Electrical"},
        {"id": "U005", "name": "James Smith", "role": "Worker", "team": "Concrete"},
        {"id": "U006", "name": "Emma Brown", "role": "Inspector", "team": "Quality Control"},
        {"id": "U007", "name": "Michael Davis", "role": "Worker", "team": "Plumbing"},
        {"id": "U008", "name": "Jennifer Wilson", "role": "Foreman", "team": "Finishing"}
    ]
    
    # Generate random badge assignments
    user_badges = []
    
    for user in users:
        # Randomly assign between 1-5 badges to each user
        num_badges = random.randint(1, 5)
        user_badge_ids = random.sample([badge["id"] for badge in BADGE_DEFINITIONS], k=num_badges)
        
        # Add badge details
        for badge_id in user_badge_ids:
            badge_def = next((badge for badge in BADGE_DEFINITIONS if badge["id"] == badge_id), None)
            if badge_def:
                # Generate a random date within the last 90 days
                award_date = datetime.now() - timedelta(days=random.randint(1, 90))
                
                user_badges.append({
                    "user_id": user["id"],
                    "user_name": user["name"],
                    "user_role": user["role"],
                    "user_team": user["team"],
                    "badge_id": badge_id,
                    "badge_name": badge_def["name"],
                    "badge_icon": badge_def["icon"],
                    "badge_tier": badge_def["tier"],
                    "badge_points": badge_def["points"],
                    "award_date": award_date.strftime("%Y-%m-%d"),
                    "awarded_by": random.choice(["System", "Site Manager", "Safety Director"]),
                    "notes": ""
                })
    
    return user_badges, users

def render_badges_dashboard():
    """Render the safety badges dashboard view."""
    st.subheader("Safety Badges Dashboard")
    
    # Get sample data
    user_badges, users = generate_sample_badges()
    
    # Calculate team totals
    team_stats = {}
    for badge in user_badges:
        team = badge["user_team"]
        if team not in team_stats:
            team_stats[team] = {"badges": 0, "points": 0}
        
        team_stats[team]["badges"] += 1
        team_stats[team]["points"] += badge["badge_points"]
    
    # Sort teams by points
    sorted_teams = sorted(team_stats.items(), key=lambda x: x[1]["points"], reverse=True)
    
    # Team leaderboard
    st.markdown("### 🏆 Team Leaderboard")
    
    # Create columns
    cols = st.columns(len(sorted_teams) if len(sorted_teams) <= 4 else 4)
    
    # Display top teams (up to 4)
    for i, (team, stats) in enumerate(sorted_teams[:4]):
        with cols[i]:
            # Background color based on position
            colors = ["#FFD700", "#C0C0C0", "#CD7F32", "#E8E8E8"]
            bg_color = colors[i] if i < 3 else colors[3]
            
            st.markdown(f"""
            <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; text-align: center;">
                <h3 style="margin: 0;">#{i+1} {team}</h3>
                <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{stats['points']} pts</p>
                <p>{stats['badges']} badges</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Individual badges leaderboard
    st.markdown("### 👑 Top Safety Contributors")
    
    # Calculate user totals
    user_stats = {}
    for badge in user_badges:
        user_id = badge["user_id"]
        if user_id not in user_stats:
            user_stats[user_id] = {
                "name": badge["user_name"],
                "role": badge["user_role"],
                "team": badge["user_team"],
                "badges": 0, 
                "points": 0
            }
        
        user_stats[user_id]["badges"] += 1
        user_stats[user_id]["points"] += badge["badge_points"]
    
    # Sort users by points
    sorted_users = sorted(user_stats.items(), key=lambda x: x[1]["points"], reverse=True)
    
    # Create a dataframe for top contributors
    top_users_data = []
    for user_id, stats in sorted_users:
        top_users_data.append({
            "Name": stats["name"],
            "Role": stats["role"],
            "Team": stats["team"],
            "Badges": stats["badges"],
            "Points": stats["points"]
        })
    
    # Display the table
    st.dataframe(pd.DataFrame(top_users_data), use_container_width=True)
    
    # Available badges section
    st.markdown("### 🔶 Available Safety Badges")
    
    # Create three columns for badges display
    badge_cols = st.columns(3)
    
    # Group badges by tier
    gold_badges = [b for b in BADGE_DEFINITIONS if b["tier"] == "gold"]
    silver_badges = [b for b in BADGE_DEFINITIONS if b["tier"] == "silver"]
    bronze_badges = [b for b in BADGE_DEFINITIONS if b["tier"] == "bronze"]
    
    # Display badges by tier
    with badge_cols[0]:
        st.markdown("#### Gold Tier")
        for badge in gold_badges:
            st.markdown(f"""
            <div style="border: 2px solid #FFD700; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                <div style="font-size: 24px; margin-bottom: 5px;">{badge['icon']} {badge['name']}</div>
                <div style="font-size: 14px; margin-bottom: 5px;">{badge['description']}</div>
                <div style="font-size: 14px; font-weight: bold;">🎖️ {badge['points']} points</div>
            </div>
            """, unsafe_allow_html=True)
    
    with badge_cols[1]:
        st.markdown("#### Silver Tier")
        for badge in silver_badges:
            st.markdown(f"""
            <div style="border: 2px solid #C0C0C0; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                <div style="font-size: 24px; margin-bottom: 5px;">{badge['icon']} {badge['name']}</div>
                <div style="font-size: 14px; margin-bottom: 5px;">{badge['description']}</div>
                <div style="font-size: 14px; font-weight: bold;">🎖️ {badge['points']} points</div>
            </div>
            """, unsafe_allow_html=True)
    
    with badge_cols[2]:
        st.markdown("#### Bronze Tier")
        for badge in bronze_badges:
            st.markdown(f"""
            <div style="border: 2px solid #CD7F32; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                <div style="font-size: 24px; margin-bottom: 5px;">{badge['icon']} {badge['name']}</div>
                <div style="font-size: 14px; margin-bottom: 5px;">{badge['description']}</div>
                <div style="font-size: 14px; font-weight: bold;">🎖️ {badge['points']} points</div>
            </div>
            """, unsafe_allow_html=True)

def render_award_badge_form():
    """Render the form for awarding new badges to users."""
    st.subheader("Award Safety Badge")
    
    # Get sample data
    _, users = generate_sample_badges()
    
    # Create the form
    with st.form(key="award_badge_form"):
        # Select user
        user_options = [f"{user['name']} ({user['role']} - {user['team']})" for user in users]
        selected_user = st.selectbox("Select recipient", user_options)
        
        # Select badge
        badge_options = [f"{badge['icon']} {badge['name']} ({badge['tier'].capitalize()}, {badge['points']} pts)" for badge in BADGE_DEFINITIONS]
        selected_badge = st.selectbox("Select badge to award", badge_options)
        
        # Notes
        notes = st.text_area("Award notes", placeholder="Enter any additional notes about this achievement...")
        
        # Submit button
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button("Award Badge", use_container_width=True)
        
        with col2:
            cancel_button = st.form_submit_button("Cancel", use_container_width=True)
    
    # Handle form submission (demo only)
    if submit_button:
        st.success(f"Badge awarded to {selected_user.split(' (')[0]}!")
        
        # In a real application, this would save to the database
        
        # Show confetti animation for celebration
        st.balloons()

def render_user_badges(user_id=None):
    """Render a user's earned badges."""
    st.subheader("Employee Badge Profile")
    
    # Get sample data
    user_badges, users = generate_sample_badges()
    
    # User selector
    user_options = ["All Employees"] + [f"{user['name']} ({user['id']})" for user in users]
    selected_user_option = st.selectbox("Select employee", user_options)
    
    if selected_user_option == "All Employees":
        # Display all users with their badge counts
        user_badge_counts = {}
        for badge in user_badges:
            user_id = badge["user_id"]
            if user_id not in user_badge_counts:
                user_badge_counts[user_id] = {
                    "name": badge["user_name"],
                    "role": badge["user_role"],
                    "team": badge["user_team"],
                    "badge_count": 0,
                    "points": 0
                }
            
            user_badge_counts[user_id]["badge_count"] += 1
            user_badge_counts[user_id]["points"] += badge["badge_points"]
        
        # Convert to list for the dataframe
        user_list = []
        for user_id, data in user_badge_counts.items():
            user_list.append({
                "ID": user_id,
                "Name": data["name"],
                "Role": data["role"],
                "Team": data["team"],
                "Badges": data["badge_count"],
                "Points": data["points"]
            })
        
        # Display as a dataframe
        st.dataframe(pd.DataFrame(user_list), use_container_width=True)
    else:
        # Extract user ID from selection
        selected_user_id = selected_user_option.split("(")[1].split(")")[0]
        
        # Get user details
        selected_user = next((user for user in users if user["id"] == selected_user_id), None)
        
        if selected_user:
            # Display user profile
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Display user avatar (placeholder)
                st.markdown(f"""
                <div style="width: 100px; height: 100px; border-radius: 50%; background-color: #f0f0f0; 
                     display: flex; align-items: center; justify-content: center; font-size: 40px;">
                    {selected_user["name"][0]}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"### {selected_user['name']}")
                st.write(f"**Role:** {selected_user['role']}")
                st.write(f"**Team:** {selected_user['team']}")
                
                # Get user badges
                user_badge_list = [badge for badge in user_badges if badge["user_id"] == selected_user_id]
                
                # Calculate total points
                total_points = sum(badge["badge_points"] for badge in user_badge_list)
                
                st.write(f"**Total Badges:** {len(user_badge_list)}")
                st.write(f"**Total Points:** {total_points}")
            
            # Display user badges
            st.markdown("### Earned Badges")
            
            if not user_badge_list:
                st.info("This employee has not earned any badges yet.")
            else:
                # Group badges by tier
                gold_badges = [b for b in user_badge_list if b["badge_tier"] == "gold"]
                silver_badges = [b for b in user_badge_list if b["badge_tier"] == "silver"]
                bronze_badges = [b for b in user_badge_list if b["badge_tier"] == "bronze"]
                
                # Display badges by tier if present
                if gold_badges:
                    st.markdown("#### Gold Tier")
                    gold_cols = st.columns(len(gold_badges))
                    for i, badge in enumerate(gold_badges):
                        with gold_cols[i]:
                            st.markdown(f"""
                            <div style="border: 2px solid #FFD700; border-radius: 5px; padding: 10px; margin-bottom: 10px; text-align: center;">
                                <div style="font-size: 36px; margin-bottom: 5px;">{badge['badge_icon']}</div>
                                <div style="font-size: 16px; font-weight: bold;">{badge['badge_name']}</div>
                                <div style="font-size: 12px;">Awarded: {badge['award_date']}</div>
                                <div style="font-size: 14px;">🎖️ {badge['badge_points']} points</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                if silver_badges:
                    st.markdown("#### Silver Tier")
                    silver_cols = st.columns(len(silver_badges))
                    for i, badge in enumerate(silver_badges):
                        with silver_cols[i]:
                            st.markdown(f"""
                            <div style="border: 2px solid #C0C0C0; border-radius: 5px; padding: 10px; margin-bottom: 10px; text-align: center;">
                                <div style="font-size: 36px; margin-bottom: 5px;">{badge['badge_icon']}</div>
                                <div style="font-size: 16px; font-weight: bold;">{badge['badge_name']}</div>
                                <div style="font-size: 12px;">Awarded: {badge['award_date']}</div>
                                <div style="font-size: 14px;">🎖️ {badge['badge_points']} points</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                if bronze_badges:
                    st.markdown("#### Bronze Tier")
                    bronze_cols = st.columns(len(bronze_badges))
                    for i, badge in enumerate(bronze_badges):
                        with bronze_cols[i]:
                            st.markdown(f"""
                            <div style="border: 2px solid #CD7F32; border-radius: 5px; padding: 10px; margin-bottom: 10px; text-align: center;">
                                <div style="font-size: 36px; margin-bottom: 5px;">{badge['badge_icon']}</div>
                                <div style="font-size: 16px; font-weight: bold;">{badge['badge_name']}</div>
                                <div style="font-size: 12px;">Awarded: {badge['award_date']}</div>
                                <div style="font-size: 14px;">🎖️ {badge['badge_points']} points</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Badge history table
                st.markdown("#### Badge History")
                
                badge_history = []
                for badge in user_badge_list:
                    badge_history.append({
                        "Date": badge["award_date"],
                        "Badge": f"{badge['badge_icon']} {badge['badge_name']}",
                        "Tier": badge["badge_tier"].capitalize(),
                        "Points": badge["badge_points"],
                        "Awarded By": badge["awarded_by"]
                    })
                
                # Sort by date (newest first)
                badge_history.sort(key=lambda x: x["Date"], reverse=True)
                
                # Display as a dataframe
                st.dataframe(pd.DataFrame(badge_history), use_container_width=True)

def render_badges():
    """Main entry point for the badges module."""
    st.title("Safety Badges & Recognition")
    
    # Create tabs for different badge views
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Award Badge", "Employee Profiles"])
    
    with tab1:
        render_badges_dashboard()
    
    with tab2:
        render_award_badge_form()
    
    with tab3:
        render_user_badges()