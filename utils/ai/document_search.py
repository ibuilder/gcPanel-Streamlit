"""
AI-Powered Document Search for gcPanel.

This module provides natural language processing capabilities for searching
and analyzing project documents, using advanced NLP techniques for improved results.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
import os
import json

class SmartDocumentSearch:
    """Smart document search implementation with NLP capabilities."""
    
    def __init__(self):
        """Initialize the smart document search."""
        # Load document index if available
        self.document_index = self.load_document_index()
    
    def load_document_index(self):
        """
        Load the document index from storage.
        
        In a real implementation, this would load pre-computed document vectors
        and metadata from a database or vector store.
        
        Returns:
            dict: Document index data
        """
        # Check if we have a cached index in session state
        if "document_index" in st.session_state:
            return st.session_state.document_index
        
        # Generate mock document index for demonstration
        documents = [
            {
                "id": "doc1",
                "title": "Highland Tower Foundation Specifications",
                "type": "Specification",
                "created_at": "2024-09-15T10:30:00",
                "updated_at": "2025-01-10T15:45:00",
                "author": "John Smith",
                "content": """
                This document details the foundation specifications for the Highland Tower project.
                The foundation consists of a reinforced concrete mat slab with a thickness of 1.2m.
                Concrete strength: 45 MPa at 28 days.
                Reinforcement: #11 bars at 25cm on center each way.
                Waterproofing: Bentonite waterproofing system with drainage layer.
                Foundation depth: 12m below street level.
                """,
                "tags": ["foundation", "structural", "specifications", "concrete"],
                "status": "Approved",
                "version": "2.1"
            },
            {
                "id": "doc2",
                "title": "Highland Tower Electrical Systems",
                "type": "Specification",
                "created_at": "2024-10-05T09:15:00",
                "updated_at": "2025-02-20T11:30:00",
                "author": "Sarah Johnson",
                "content": """
                Electrical systems specifications for Highland Tower:
                Main electrical service: 4000A, 480/277V, 3-phase, 4-wire.
                Emergency generator: 750kW diesel with 72-hour fuel storage.
                Lighting: LED throughout with daylight harvesting and occupancy sensors.
                Electric vehicle charging: 30 Level 2 charging stations in garage.
                Smart building systems: BACnet protocol for integration.
                Residential units: 200A service with smart metering.
                """,
                "tags": ["electrical", "MEP", "specifications", "power"],
                "status": "Approved",
                "version": "1.8"
            },
            {
                "id": "doc3",
                "title": "Highland Tower Structural Analysis Report",
                "type": "Report",
                "created_at": "2024-11-20T14:00:00",
                "updated_at": "2025-03-15T10:15:00",
                "author": "Mike Chen",
                "content": """
                Structural analysis report for Highland Tower:
                The building has been analyzed for wind loads up to 150 mph and seismic loads per local code.
                Lateral force resisting system: Concrete shear walls with coupling beams.
                Floor system: 8" post-tensioned concrete slabs with 5ksi concrete.
                Column layout: 30'x30' typical bay size with 24"x24" columns at lower levels.
                Drift ratio: Maximum of 1/500 under service wind loads.
                The analysis confirms that the structural system meets all code requirements with adequate safety factors.
                """,
                "tags": ["structural", "analysis", "engineering", "report"],
                "status": "Final",
                "version": "3.0"
            },
            {
                "id": "doc4",
                "title": "Highland Tower HVAC Design",
                "type": "Design Document",
                "created_at": "2024-12-10T11:20:00",
                "updated_at": "2025-03-30T16:45:00",
                "author": "Lisa Rodriguez",
                "content": """
                HVAC design document for Highland Tower:
                System type: Variable refrigerant flow (VRF) with heat recovery.
                Zoning: Each residential unit is a separate zone with individual control.
                Ventilation: Energy recovery ventilators (ERVs) for fresh air.
                Common areas: Water-source heat pumps with cooling tower and boiler.
                Retail spaces: Dedicated outdoor air system (DOAS) with VRF.
                Building automation: DDC controls with smartphone integration.
                Energy efficiency: Expected 30% better than ASHRAE 90.1 baseline.
                """,
                "tags": ["HVAC", "MEP", "mechanical", "design"],
                "status": "In Review",
                "version": "2.5"
            },
            {
                "id": "doc5",
                "title": "Highland Tower Construction Schedule",
                "type": "Schedule",
                "created_at": "2025-01-05T08:45:00",
                "updated_at": "2025-04-10T13:30:00",
                "author": "John Smith",
                "content": """
                Construction schedule for Highland Tower:
                Project start: June 1, 2024
                Excavation and foundations: June 2024 - September 2024
                Structural frame: October 2024 - July 2025
                Building envelope: April 2025 - November 2025
                MEP rough-in: June 2025 - January 2026
                Interior finishes: September 2025 - May 2026
                Commissioning: April 2026 - June 2026
                Substantial completion: July 1, 2026
                Final completion: August 15, 2026
                """,
                "tags": ["schedule", "timeline", "planning", "construction"],
                "status": "Current",
                "version": "4.2"
            }
        ]
        
        # Cache in session state
        st.session_state.document_index = documents
        
        return documents
    
    def search(self, query, filters=None, limit=10):
        """
        Search documents using natural language processing.
        
        Args:
            query (str): Search query in natural language
            filters (dict): Optional filters to apply
            limit (int): Maximum number of results to return
            
        Returns:
            list: Matching documents
        """
        # In a real implementation, this would use embeddings and vector search
        # For this demo, we'll use a simple keyword matching approach
        
        results = []
        
        # Clean the query
        query = query.lower()
        
        # For each document, calculate a relevance score
        for doc in self.document_index:
            # Basic relevance calculation
            relevance = 0
            
            # Check title
            if query in doc["title"].lower():
                relevance += 5
            
            # Check content
            if query in doc["content"].lower():
                relevance += 3
            
            # Check tags
            for tag in doc["tags"]:
                if query in tag.lower():
                    relevance += 2
            
            # Apply filters if specified
            if filters:
                # Check if document meets all filter criteria
                passes_filters = True
                
                for key, value in filters.items():
                    if key in doc and doc[key] != value:
                        passes_filters = False
                        break
                
                if not passes_filters:
                    continue
            
            # If document is relevant, add to results
            if relevance > 0:
                results.append({
                    "document": doc,
                    "relevance": relevance
                })
        
        # Sort by relevance and limit results
        results.sort(key=lambda x: x["relevance"], reverse=True)
        results = results[:limit]
        
        # Extract just the documents
        return [r["document"] for r in results]
    
    def semantic_search(self, query, filters=None, limit=10):
        """
        Perform semantic search using natural language understanding.
        
        Args:
            query (str): Search query in natural language
            filters (dict): Optional filters to apply
            limit (int): Maximum number of results to return
            
        Returns:
            list: Matching documents
        """
        # In a real implementation, this would use a language model
        # For this demo, we'll simulate it with keyword expansions
        
        # Expand query with related terms (simulating semantic search)
        expanded_terms = []
        
        # Hard-coded term expansions for demo purposes
        term_expansions = {
            "foundation": ["concrete", "footing", "slab", "reinforcement", "waterproofing"],
            "electrical": ["power", "wiring", "circuit", "lighting", "service"],
            "structural": ["beam", "column", "wall", "frame", "analysis"],
            "hvac": ["mechanical", "cooling", "heating", "ventilation", "air"],
            "schedule": ["timeline", "date", "milestone", "planning", "completion"]
        }
        
        # Check if query contains any terms that can be expanded
        for term, expansions in term_expansions.items():
            if term in query.lower():
                expanded_terms.extend(expansions)
        
        # If no expansions found, use original query
        if not expanded_terms:
            return self.search(query, filters, limit)
        
        # Search with original query
        original_results = self.search(query, filters, limit)
        
        # Search with each expanded term
        all_results = list(original_results)  # Start with original results
        
        for term in expanded_terms:
            term_results = self.search(term, filters, limit)
            
            # Add any new results
            for doc in term_results:
                if doc not in all_results:
                    all_results.append(doc)
        
        # Return top results, prioritizing original query results
        return all_results[:limit]
    
    def extract_key_information(self, document_id):
        """
        Extract key information from a document using NLP.
        
        Args:
            document_id (str): Document ID
            
        Returns:
            dict: Extracted information
        """
        # Find the document
        document = None
        for doc in self.document_index:
            if doc["id"] == document_id:
                document = doc
                break
        
        if not document:
            return None
        
        # In a real implementation, this would use NLP to extract entities, etc.
        # For this demo, we'll simulate it with pattern matching
        
        # Extract dates (simple regex for YYYY-MM-DD format)
        date_pattern = r'\b\d{4}-\d{2}-\d{2}\b'
        dates = re.findall(date_pattern, document["content"])
        
        # Extract numbers (simple regex for numbers with optional decimals)
        number_pattern = r'\b\d+(?:\.\d+)?\b'
        numbers = re.findall(number_pattern, document["content"])
        
        # Extract measurements (simple regex for numbers with units)
        measurement_pattern = r'\b\d+(?:\.\d+)?\s*(?:mm|cm|m|in|ft|mph|kW|A|V)\b'
        measurements = re.findall(measurement_pattern, document["content"], re.IGNORECASE)
        
        # Extract mentions of specifications or standards
        spec_pattern = r'\b(?:ASHRAE|ASTM|ACI|IEC|NEC|NFPA|ASCE|OSHA)\s*\d*\b'
        specifications = re.findall(spec_pattern, document["content"], re.IGNORECASE)
        
        return {
            "dates": dates,
            "numbers": numbers,
            "measurements": measurements,
            "specifications": specifications
        }


# ----- UI Components -----

def render_smart_search_interface():
    """Render the smart document search interface."""
    st.title("Smart Document Search")
    
    # Initialize search engine
    search_engine = SmartDocumentSearch()
    
    # Search input
    search_query = st.text_input("Search documents in natural language", 
                               placeholder="e.g., 'Find foundation specs for Highland Tower'")
    
    # Search method selection (basic or semantic)
    search_method = st.radio("Search method", ["Basic", "Semantic (AI-powered)"], horizontal=True)
    
    # Filters
    with st.expander("Advanced Filters"):
        col1, col2 = st.columns(2)
        
        with col1:
            filter_type = st.selectbox("Document Type", ["Any", "Specification", "Report", "Design Document", "Schedule"])
        
        with col2:
            filter_status = st.selectbox("Status", ["Any", "Approved", "In Review", "Final", "Current"])
        
        # Author filter
        filter_author = st.selectbox("Author", ["Any", "John Smith", "Sarah Johnson", "Mike Chen", "Lisa Rodriguez"])
    
    # Search button
    if st.button("Search") or search_query:
        # Build filters
        filters = {}
        
        if filter_type != "Any":
            filters["type"] = filter_type
            
        if filter_status != "Any":
            filters["status"] = filter_status
            
        if filter_author != "Any":
            filters["author"] = filter_author
        
        # Perform search
        if search_method == "Basic":
            results = search_engine.search(search_query, filters)
        else:
            results = search_engine.semantic_search(search_query, filters)
        
        # Display results
        if results:
            st.markdown(f"### {len(results)} Results Found")
            
            for doc in results:
                with st.expander(f"{doc['title']} ({doc['type']})"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Author:** {doc['author']}")
                        st.markdown(f"**Last Updated:** {doc['updated_at'].split('T')[0]}")
                        st.markdown(f"**Status:** {doc['status']} (v{doc['version']})")
                    
                    with col2:
                        st.markdown("**Tags:**")
                        tags_html = " ".join([f'<span style="background-color: #e1e1e1; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">{tag}</span>' for tag in doc['tags']])
                        st.markdown(tags_html, unsafe_allow_html=True)
                    
                    st.markdown("**Content:**")
                    st.text(doc['content'])
                    
                    # Show extracted information button
                    if st.button("Extract Key Information", key=f"extract_{doc['id']}"):
                        with st.spinner("Analyzing document..."):
                            # Simulate processing time
                            key_info = search_engine.extract_key_information(doc['id'])
                            
                            if key_info:
                                st.markdown("### Key Information Extracted")
                                
                                if key_info["measurements"]:
                                    st.markdown("**Measurements:**")
                                    st.markdown(", ".join(key_info["measurements"]))
                                
                                if key_info["specifications"]:
                                    st.markdown("**Specifications/Standards:**")
                                    st.markdown(", ".join(key_info["specifications"]))
        else:
            st.info("No documents found matching your search criteria.")
    
    # Example searches
    st.markdown("### Example Searches")
    examples = [
        "foundation specifications",
        "HVAC system details",
        "structural analysis",
        "construction timeline",
        "electrical requirements"
    ]
    
    for i, example in enumerate(examples):
        if st.button(example, key=f"example_{i}"):
            # Set search query and trigger search
            search_query = example
            st.session_state.search_query = example
            st.rerun()