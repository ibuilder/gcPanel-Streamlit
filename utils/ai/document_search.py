"""
AI-powered document search utilities for gcPanel.

This module provides document search capabilities using natural language
processing to find and extract relevant information from project documents.
"""

import streamlit as st
from utils.ai.anthropic_client import analyze_document

def search_project_documents(query, document_sources=None):
    """
    Search through project documents using natural language queries.
    
    Args:
        query (str): The natural language search query
        document_sources (list): List of document categories to search
        
    Returns:
        list: List of document matches with relevant excerpts
    """
    # In a production environment, this would connect to a document database
    # and retrieve actual documents matching the query
    
    # For demonstration, we'll return mock results
    if "electrical" in query.lower():
        results = [
            {
                "title": "RFI #103: Electrical Panel Location",
                "type": "RFI",
                "date": "April 12, 2025",
                "status": "Closed",
                "excerpt": "The electrical subcontractor has requested clarification on the location of the main electrical panels on level 2. The current drawings show potential conflict with HVAC ductwork.",
                "url": "#"
            },
            {
                "title": "Submittal #87: Electrical Fixtures",
                "type": "Submittal",
                "date": "March 28, 2025",
                "status": "Approved with Comments",
                "excerpt": "The proposed LED fixtures for the common areas meet the energy efficiency requirements but architect has requested sample installations before final approval.",
                "url": "#"
            }
        ]
    elif "foundation" in query.lower():
        results = [
            {
                "title": "RFI #42: Foundation Waterproofing",
                "type": "RFI",
                "date": "January 15, 2025",
                "status": "Closed",
                "excerpt": "Subcontractor requesting clarification on waterproofing details at elevator pit and foundation wall intersections. Current details show potential water intrusion points.",
                "url": "#"
            }
        ]
    else:
        results = []
    
    return results

def analyze_search_results(query, results):
    """
    Generate an AI analysis of search results.
    
    Args:
        query (str): The search query
        results (list): List of document results
        
    Returns:
        str: AI-generated summary and analysis
    """
    if not results:
        return "No relevant documents found matching your query."
    
    # In production, this would use the Anthropic API to analyze actual results
    # For now, we'll return a pre-written summary based on the query
    
    # Combine all document excerpts for analysis
    all_text = "\n\n".join([f"{r['title']}\n{r['excerpt']}" for r in results])
    
    # Check if we have an Anthropic API key available
    if 'ANTHROPIC_API_KEY' in st.secrets or 'ANTHROPIC_API_KEY' in st.session_state:
        # Use the Anthropic API to analyze the documents
        return analyze_document(all_text, query)
    else:
        # Return a message about needing the API key
        return """
        To enable AI-powered document analysis, please add your Anthropic API key.
        This will allow the AI to provide detailed insights about your documents.
        """

def render_document_search_results(results, query):
    """
    Render search results in a user-friendly format.
    
    Args:
        results (list): List of document results
        query (str): The search query
    """
    if not results:
        st.info("No documents found matching your query. Try different search terms or document sources.")
        return
    
    st.subheader(f"Search Results ({len(results)} documents)")
    
    for result in results:
        with st.container():
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
                <h4 style="margin-top: 0;">{result['title']}</h4>
                <p style="color: #666; font-size: 0.9em;">Submitted: {result['date']} | Status: {result['status']}</p>
                <p><strong>Relevant excerpt:</strong> {result['excerpt']}</p>
                <p><a href="{result['url']}" style="text-decoration: none;">View Full Document →</a></p>
            </div>
            """, unsafe_allow_html=True)
    
    # AI analysis of the results
    st.subheader("AI Summary")
    analysis = analyze_search_results(query, results)
    st.success(analysis)