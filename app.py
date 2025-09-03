#!/usr/bin/env python3
"""
Streamlit Client Application for Insurance Database Queries
Connects to FastAPI server to query user and policy information
"""

import streamlit as st
import httpx
import pandas as pd
from typing import Dict, List, Optional
import json

# Page configuration
st.set_page_config(
    page_title="Insurance Database Query Tool",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client()
    
    def get(self, endpoint: str) -> Optional[Dict]:
        """Make GET request to API"""
        try:
            response = self.client.get(f"{self.base_url}{endpoint}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"error": "No data found"}
            else:
                return {"error": f"API Error: {response.status_code}"}
        except Exception as e:
            return {"error": f"Connection error: {str(e)}"}
    
    def close(self):
        self.client.close()

# Initialize API client
@st.cache_resource
def get_api_client():
    return APIClient(API_BASE_URL)

def display_user_data(data: List[Dict]):
    """Display user data in a formatted way"""
    if not data:
        st.warning("No user data found.")
        return
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(data)
    
    # Display each user
    for idx, user in enumerate(data):
        with st.expander(f"👤 {user.get('first_name', '')} {user.get('last_name', '')} (ID: {user.get('user_id', 'N/A')})", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Personal Information**")
                st.write(f"📧 **Email:** {user.get('email', 'N/A')}")
                st.write(f"📞 **Phone:** {user.get('phone', 'N/A')}")
                st.write(f"🎂 **Date of Birth:** {user.get('date_of_birth', 'N/A')}")
                st.write(f"🏠 **Address:** {user.get('address', 'N/A')}")
                st.write(f"🏙️ **City, State:** {user.get('city', 'N/A')}, {user.get('state', 'N/A')} {user.get('zip_code', 'N/A')}")
            
            with col2:
                st.write("**Policy Information**")
                st.write(f"📋 **Policy Number:** {user.get('policy_number', 'N/A')}")
                st.write(f"🏷️ **Policy Type:** {user.get('policy_type', 'N/A')}")
                st.write(f"💰 **Premium Amount:** ${user.get('premium_amount', 'N/A')}")
                st.write(f"📅 **Start Date:** {user.get('policy_start_date', 'N/A')}")
                st.write(f"📅 **End Date:** {user.get('policy_end_date', 'N/A')}")
    
    # Show data table
    if st.checkbox("Show raw data table", key=f"user_table_{len(data)}"):
        st.dataframe(df, use_container_width=True)

def display_policy_data(data: List[Dict]):
    """Display policy data in a formatted way"""
    if not data:
        st.warning("No policy data found.")
        return
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(data)
    
    # Display each policy
    for idx, policy in enumerate(data):
        status_emoji = {"Active": "✅", "Expired": "⏰", "Cancelled": "❌", "Pending": "⏳"}
        emoji = status_emoji.get(policy.get('policy_status', ''), "📋")
        
        with st.expander(f"{emoji} Policy: {policy.get('policy_number', 'N/A')} - {policy.get('policy_type', 'N/A')}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Policy Details**")
                st.write(f"🆔 **Policy ID:** {policy.get('policy_id', 'N/A')}")
                st.write(f"👤 **User ID:** {policy.get('user_id', 'N/A')}")
                st.write(f"📊 **Status:** {policy.get('policy_status', 'N/A')}")
                st.write(f"💰 **Premium:** ${policy.get('premium_amount', 'N/A'):,}" if policy.get('premium_amount') else "💰 **Premium:** N/A")
                st.write(f"🏦 **Coverage:** ${policy.get('coverage_amount', 'N/A'):,}" if policy.get('coverage_amount') else "🏦 **Coverage:** N/A")
                st.write(f"💳 **Deductible:** ${policy.get('deductible_amount', 'N/A'):,}" if policy.get('deductible_amount') else "💳 **Deductible:** N/A")
            
            with col2:
                st.write("**Dates & Agent Info**")
                st.write(f"📅 **Start Date:** {policy.get('policy_start_date', 'N/A')}")
                st.write(f"📅 **End Date:** {policy.get('policy_end_date', 'N/A')}")
                st.write(f"💱 **Payment Frequency:** {policy.get('payment_frequency', 'N/A')}")
                st.write(f"👨‍💼 **Agent:** {policy.get('agent_name', 'N/A')}")
                st.write(f"📞 **Agent Phone:** {policy.get('agent_phone', 'N/A')}")
                
                if policy.get('policy_description'):
                    st.write(f"📝 **Description:** {policy.get('policy_description')}")
    
    # Show data table
    if st.checkbox("Show raw data table", key=f"policy_table_{len(data)}"):
        st.dataframe(df, use_container_width=True)

def check_api_connection(client: APIClient) -> bool:
    """Check if API server is running"""
    try:
        response = client.get("/")
        return response and "error" not in response
    except:
        return False

def main():
    st.title("🏥 Insurance Database Query Tool")
    st.markdown("Query user and policy information using FastAPI backend")
    
    # Initialize API client
    client = get_api_client()
    
    # Check API connection
    if not check_api_connection(client):
        st.error("❌ Cannot connect to API server. Please ensure the FastAPI server is running on http://127.0.0.1:8000")
        st.info("Run: `python mcp_server.py` to start the API server")
        return
    
    st.success("✅ Connected to API server")
    
    # Sidebar for query selection
    st.sidebar.header("🔍 Query Options")
    query_type = st.sidebar.selectbox(
        "Select Query Type:",
        [
            "Get User by ID",
            "Get User by Email", 
            "Search Users by Name",
            "Get Policy by Number",
            "Get Policies by User ID",
            "Get Policies by Status",
            "Get Policies by Type"
        ]
    )
    
    # Main content area
    if query_type == "Get User by ID":
        st.header("👤 Get User by ID")
        user_id = st.number_input("Enter User ID:", min_value=1, step=1)
        
        if st.button("🔍 Search User", type="primary"):
            with st.spinner("Querying database..."):
                result = client.get(f"/users/{user_id}")
                if result and "error" in result:
                    st.error(result["error"])
                elif result:
                    display_user_data(result)
    
    elif query_type == "Get User by Email":
        st.header("📧 Get User by Email")
        email = st.text_input("Enter Email Address:")
        
        if st.button("🔍 Search User", type="primary") and email:
            with st.spinner("Querying database..."):
                result = client.get(f"/users/email/{email}")
                if result and "error" in result:
                    st.error(result["error"])
                elif result:
                    display_user_data(result)
    
    elif query_type == "Search Users by Name":
        st.header("🔍 Search Users by Name")
        name = st.text_input("Enter Name (first or last):")
        
        if st.button("🔍 Search Users", type="primary") and name:
            with st.spinner("Querying database..."):
                result = client.get(f"/users/search/{name}")
                if result and "error" in result:
                    st.error(result["error"])
                elif result:
                    display_user_data(result)
    
    elif query_type == "Get Policy by Number":
        st.header("📋 Get Policy by Number")
        policy_number = st.text_input("Enter Policy Number:")
        
        if st.button("🔍 Search Policy", type="primary") and policy_number:
            with st.spinner("Querying database..."):
                result = client.get(f"/policies/{policy_number}")
                if result and "error" in result:
                    st.error(result["error"])
                elif result:
                    display_policy_data(result)
    
    elif query_type == "Get Policies by User ID":
        st.header("👤 Get Policies by User ID")
        user_id = st.number_input("Enter User ID:", min_value=1, step=1, key="policies_user_id")
        
        if st.button("🔍 Get Policies", type="primary"):
            with st.spinner("Querying database..."):
                result = client.get(f"/policies/user/{user_id}")
                if result and "error" in result:
                    st.error(result["error"])
                elif result:
                    display_policy_data(result)
    
    elif query_type == "Get Policies by Status":
        st.header("📊 Get Policies by Status")
        status = st.selectbox(
            "Select Policy Status:",
            ["Active", "Expired", "Cancelled", "Pending"]
        )
        
        if st.button("🔍 Get Policies by Status", type="primary"):
            with st.spinner("Querying database..."):
                result = client.get(f"/policies/status/{status}")
                if result and "error" in result:
                    st.error(result["error"])
                elif result:
                    display_policy_data(result)
    
    elif query_type == "Get Policies by Type":
        st.header("🏷️ Get Policies by Type")
        policy_type = st.selectbox(
            "Select Policy Type:",
            ["Auto", "Home", "Life", "Health", "Business"]
        )
        
        if st.button("🔍 Get Policies by Type", type="primary"):
            with st.spinner("Querying database..."):
                result = client.get(f"/policies/type/{policy_type}")
                if result and "error" in result:
                    st.error(result["error"])
                elif result:
                    display_policy_data(result)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Insurance Database Query Tool**")
    st.sidebar.markdown("Powered by FastAPI & Streamlit")
    
    # API Info
    with st.sidebar.expander("ℹ️ API Information"):
        st.markdown(f"**API URL:** {API_BASE_URL}")
        st.markdown("**Status:** ✅ Connected" if check_api_connection(client) else "**Status:** ❌ Disconnected")

if __name__ == "__main__":
    main()