"""
Search Manager for gcPanel.

This module provides global search functionality and advanced filtering
capabilities for searching across different modules in the application.

Features:
- Global search across multiple data sources
- Advanced filtering with multiple criteria
- Context-sensitive search suggestions
- Search result caching for performance
"""

import streamlit as st
import json
import os
import re
from datetime import datetime
import pandas as pd
from typing import List, Dict, Any, Callable, Optional, Union

from utils.cache_manager import CacheManager, cached

class SearchManager:
    """
    Search manager providing global and module-specific search capabilities.
    """
    
    @staticmethod
    def initialize():
        """Initialize search-related session state variables."""
        if "global_search_query" not in st.session_state:
            st.session_state.global_search_query = ""
        
        if "last_search_results" not in st.session_state:
            st.session_state.last_search_results = {}
        
        if "search_filters" not in st.session_state:
            st.session_state.search_filters = {}
            
    @staticmethod
    def render_global_search():
        """
        Render the global search bar in the application header.
        
        Returns:
            dict: Dictionary with search state and results
        """
        # Initialize search state
        SearchManager.initialize()
        
        # Create search container
        search_container = st.container()
        
        with search_container:
            # Show search bar with suggestions
            search_query = st.text_input(
                "Search across all modules",
                value=st.session_state.global_search_query,
                key="global_search_input",
                placeholder="Search documents, proposals, tickets...",
                help="Search across all modules in the application"
            )
            
            # Update session state with current query
            st.session_state.global_search_query = search_query
            
            # Process search when query is entered
            search_performed = False
            search_results = {}
            
            if search_query:
                search_performed = True
                with st.spinner("Searching..."):
                    # Perform search across modules with caching
                    search_results = SearchManager.perform_global_search(search_query)
                    
                    # Store in session state
                    st.session_state.last_search_results = search_results
            
            # Return search status and results
            return {
                "performed": search_performed,
                "query": search_query,
                "results": search_results
            }
    
    @staticmethod
    @cached(ttl_seconds=300)  # Cache search results for 5 minutes
    def perform_global_search(query: str) -> Dict[str, Any]:
        """
        Perform a global search across all modules.
        
        Args:
            query (str): The search query string
            
        Returns:
            dict: Search results organized by module
        """
        results = {}
        
        # Clean and prepare search terms
        search_terms = [term.lower() for term in query.split() if len(term) > 1]
        
        if not search_terms:
            return results
            
        # Search in proposals
        proposals_results = SearchManager._search_in_proposals(search_terms)
        if proposals_results:
            results["Proposals"] = proposals_results
            
        # Search in T&M tickets
        tm_tickets_results = SearchManager._search_in_tm_tickets(search_terms)
        if tm_tickets_results:
            results["T&M Tickets"] = tm_tickets_results
            
        # Search in change orders
        change_orders_results = SearchManager._search_in_change_orders(search_terms)
        if change_orders_results:
            results["Change Orders"] = change_orders_results
            
        # Search in documents
        document_results = SearchManager._search_in_documents(search_terms)
        if document_results:
            results["Documents"] = document_results
            
        # Add any other module searches as needed
        
        return results
    
    @staticmethod
    def _search_in_proposals(search_terms: List[str]) -> List[Dict[str, Any]]:
        """Search in proposals module data."""
        results = []
        
        # Check if proposals data exists
        file_path = "data/cost_management/proposals.json"
        if not os.path.exists(file_path):
            return results
        
        try:
            # Load proposals data
            with open(file_path, 'r') as f:
                proposals = json.load(f)
            
            # Search in each proposal
            for proposal in proposals:
                score = 0
                matches = []
                
                # Fields to search in
                searchable_fields = [
                    "proposal_id", "title", "company_name", "description", 
                    "scope_of_work", "notes", "proposal_type"
                ]
                
                # Check each search term against each field
                for field in searchable_fields:
                    if field not in proposal:
                        continue
                        
                    field_value = str(proposal[field]).lower()
                    
                    for term in search_terms:
                        if term in field_value:
                            score += 1
                            matches.append(field)
                
                # Also search in line items descriptions
                if "line_items" in proposal:
                    for item in proposal["line_items"]:
                        if "description" in item:
                            for term in search_terms:
                                if term in item["description"].lower():
                                    score += 1
                                    matches.append("line_items")
                
                # If any matches found, add to results
                if score > 0:
                    results.append({
                        "id": proposal["proposal_id"],
                        "title": proposal["title"],
                        "subtitle": f"{proposal['company_name']} - ${proposal['total_amount']:,.2f}",
                        "status": proposal.get("status", "Unknown"),
                        "date": proposal.get("submission_date", ""),
                        "score": score,
                        "matches": list(set(matches)),
                        "type": "proposal",
                        "url": f"?module=Cost Management&tab=Proposals&proposal_id={proposal['proposal_id']}"
                    })
        
        except Exception as e:
            st.error(f"Error searching proposals: {str(e)}")
        
        # Sort by score (descending)
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    @staticmethod
    def _search_in_tm_tickets(search_terms: List[str]) -> List[Dict[str, Any]]:
        """Search in T&M tickets module data."""
        results = []
        
        # Check if T&M tickets data exists
        file_path = "data/cost_management/tm_tickets.json"
        if not os.path.exists(file_path):
            return results
        
        try:
            # Load T&M tickets data
            with open(file_path, 'r') as f:
                tickets = json.load(f)
            
            # Search in each ticket
            for ticket in tickets:
                score = 0
                matches = []
                
                # Fields to search in
                searchable_fields = [
                    "ticket_id", "description", "company_name", "detailed_description", 
                    "notes", "work_type", "location", "worker_name", "supervisor_name"
                ]
                
                # Check each search term against each field
                for field in searchable_fields:
                    if field not in ticket:
                        continue
                        
                    field_value = str(ticket[field]).lower()
                    
                    for term in search_terms:
                        if term in field_value:
                            score += 1
                            matches.append(field)
                
                # Also search in line items descriptions
                if "line_items" in ticket:
                    for item in ticket["line_items"]:
                        if "description" in item:
                            for term in search_terms:
                                if term in item["description"].lower():
                                    score += 1
                                    matches.append("line_items")
                
                # If any matches found, add to results
                if score > 0:
                    results.append({
                        "id": ticket["ticket_id"],
                        "title": ticket["description"],
                        "subtitle": f"{ticket['company_name']} - ${ticket['total_amount']:,.2f}",
                        "status": ticket.get("status", "Unknown"),
                        "date": ticket.get("work_date", ""),
                        "score": score,
                        "matches": list(set(matches)),
                        "type": "tm_ticket",
                        "url": f"?module=Cost Management&tab=T&M Tickets&ticket_id={ticket['ticket_id']}"
                    })
        
        except Exception as e:
            st.error(f"Error searching T&M tickets: {str(e)}")
        
        # Sort by score (descending)
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    @staticmethod
    def _search_in_change_orders(search_terms: List[str]) -> List[Dict[str, Any]]:
        """Search in change orders module data."""
        results = []
        
        # Check if change orders data exists
        file_path = "data/cost_management/change_orders.json"
        if not os.path.exists(file_path):
            return results
        
        try:
            # Load change orders data
            with open(file_path, 'r') as f:
                change_orders = json.load(f)
            
            # Search in each change order
            for change_order in change_orders:
                score = 0
                matches = []
                
                # Fields to search in
                searchable_fields = [
                    "co_id", "title", "company_name", "description", 
                    "justification", "notes", "co_type", "approver"
                ]
                
                # Check each search term against each field
                for field in searchable_fields:
                    if field not in change_order:
                        continue
                        
                    field_value = str(change_order[field]).lower()
                    
                    for term in search_terms:
                        if term in field_value:
                            score += 1
                            matches.append(field)
                
                # Also search in linked items
                if "linked_proposals" in change_order:
                    for item in change_order["linked_proposals"]:
                        if "title" in item:
                            for term in search_terms:
                                if term in item["title"].lower():
                                    score += 1
                                    matches.append("linked_proposals")
                
                if "linked_tm_tickets" in change_order:
                    for item in change_order["linked_tm_tickets"]:
                        if "description" in item:
                            for term in search_terms:
                                if term in item["description"].lower():
                                    score += 1
                                    matches.append("linked_tm_tickets")
                
                # If any matches found, add to results
                if score > 0:
                    results.append({
                        "id": change_order["co_id"],
                        "title": change_order["title"],
                        "subtitle": f"{change_order['company_name']} - ${change_order['total_amount']:,.2f}",
                        "status": change_order.get("status", "Unknown"),
                        "date": change_order.get("submission_date", ""),
                        "score": score,
                        "matches": list(set(matches)),
                        "type": "change_order",
                        "url": f"?module=Cost Management&tab=Change Orders&co_id={change_order['co_id']}"
                    })
        
        except Exception as e:
            st.error(f"Error searching change orders: {str(e)}")
        
        # Sort by score (descending)
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    @staticmethod
    def _search_in_documents(search_terms: List[str]) -> List[Dict[str, Any]]:
        """Search in documents module data."""
        results = []
        
        # Check if documents data exists
        file_path = "data/documents/document_metadata.json"
        if not os.path.exists(file_path):
            return results
        
        try:
            # Load document metadata
            with open(file_path, 'r') as f:
                documents = json.load(f)
            
            # Search in each document's metadata
            for document in documents:
                score = 0
                matches = []
                
                # Fields to search in
                searchable_fields = [
                    "document_id", "title", "description", "filename", 
                    "author", "tags", "category", "document_type"
                ]
                
                # Check each search term against each field
                for field in searchable_fields:
                    if field not in document:
                        continue
                    
                    # Handle tags separately as they might be a list
                    if field == "tags" and isinstance(document[field], list):
                        field_value = " ".join(document[field]).lower()
                    else:
                        field_value = str(document[field]).lower()
                    
                    for term in search_terms:
                        if term in field_value:
                            score += 1
                            matches.append(field)
                
                # If any matches found, add to results
                if score > 0:
                    results.append({
                        "id": document["document_id"],
                        "title": document["title"],
                        "subtitle": f"{document.get('document_type', 'Document')} - {document.get('version', 'Unknown')}",
                        "status": document.get("status", "Unknown"),
                        "date": document.get("date_uploaded", ""),
                        "score": score,
                        "matches": list(set(matches)),
                        "type": "document",
                        "url": f"?module=Documents&document_id={document['document_id']}"
                    })
        
        except Exception as e:
            st.error(f"Error searching documents: {str(e)}")
        
        # Sort by score (descending)
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    @staticmethod
    def render_search_results(results: Dict[str, List[Dict[str, Any]]]):
        """
        Render search results in a clean, organized UI.
        
        Args:
            results (dict): Search results by module
        """
        total_results = sum(len(module_results) for module_results in results.values())
        
        if total_results == 0:
            st.info("No results found. Try different keywords or check spelling.")
            return
        
        st.markdown(f"#### Found {total_results} results")
        
        # Create tabs for each module with results
        if len(results) > 1:
            tabs = ["All Results"] + list(results.keys())
            selected_tab = st.radio("Filter results by:", tabs, horizontal=True)
        else:
            selected_tab = list(results.keys())[0]
        
        # Display results
        if selected_tab == "All Results":
            # Combine and sort all results
            all_results = []
            for module_name, module_results in results.items():
                for result in module_results:
                    result["module"] = module_name
                    all_results.append(result)
            
            all_results.sort(key=lambda x: x["score"], reverse=True)
            
            # Display combined results
            for result in all_results:
                SearchManager._render_result_card(result, show_module=True)
        else:
            # Display results for selected module
            module_results = results.get(selected_tab, [])
            for result in module_results:
                SearchManager._render_result_card(result)
    
    @staticmethod
    def _render_result_card(result: Dict[str, Any], show_module: bool = False):
        """
        Render a search result card.
        
        Args:
            result (dict): The search result data
            show_module (bool): Whether to show the module name
        """
        # Create card with border and background
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; 
                       margin-bottom: 10px; background-color: #f8f9fa;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <a href="{result['url']}" style="text-decoration: none; color: #0366d6; font-weight: bold; font-size: 16px;">{result['title']}</a>
                        <div style="color: #666; font-size: 14px; margin-top: 3px;">{result['subtitle']}</div>
                    </div>
                    <div>
                        <span style="
                            background-color: {SearchManager._get_status_color(result['status'])};
                            color: white;
                            padding: 3px 8px;
                            border-radius: 12px;
                            font-size: 12px;
                            white-space: nowrap;
                        ">{result['status']}</span>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-top: 8px;">
                    <div style="color: #555; font-size: 13px;">
                        {f"<span style='color: #777; margin-right: 10px;'>{result.get('module', '')}</span>" if show_module else ""}
                        <span style="color: #777;">ID: {result['id']}</span>
                        {f" • <span style='color: #777;'>{result['date']}</span>" if result.get('date') else ""}
                    </div>
                    <div style="color: #777; font-size: 12px;">
                        Matches: {', '.join(result['matches'][:3])}
                        {" ..." if len(result['matches']) > 3 else ""}
                    </div>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    @staticmethod
    def _get_status_color(status: str) -> str:
        """Get the appropriate color for a status."""
        status = status.lower()
        
        if "approved" in status or "complete" in status or "done" in status:
            return "#28a745"  # Green
        elif "review" in status or "pending" in status or "in progress" in status:
            return "#007bff"  # Blue
        elif "rejected" in status or "failed" in status or "error" in status:
            return "#dc3545"  # Red
        elif "draft" in status or "new" in status:
            return "#6c757d"  # Gray
        elif "submitted" in status or "waiting" in status:
            return "#17a2b8"  # Teal
        elif "invoiced" in status or "billed" in status:
            return "#6f42c1"  # Purple
        else:
            return "#6c757d"  # Default gray
    
    @staticmethod
    def render_filter_bar(items, filters, on_filter_change=None):
        """
        Render an advanced filter bar for a list of items.
        
        Args:
            items (list): List of items to filter
            filters (dict): Current filter state
            on_filter_change (callable, optional): Callback when filters change
            
        Returns:
            list: Filtered items
        """
        # Create a container for filters
        filter_container = st.container()
        
        with filter_container:
            # Create columns for different filters
            cols = st.columns([3, 2, 2, 1])
            
            with cols[0]:
                search_text = st.text_input(
                    "Search", 
                    value=filters.get("search_text", ""),
                    placeholder="Search in this view..."
                )
                
            with cols[1]:
                if "status_options" in filters:
                    status = st.multiselect(
                        "Status",
                        options=filters["status_options"],
                        default=filters.get("status", [])
                    )
                else:
                    status = []
                    
            with cols[2]:
                if "date_range" in filters:
                    start_date = st.date_input(
                        "From Date",
                        value=filters["date_range"].get("start", None)
                    )
                    end_date = st.date_input(
                        "To Date",
                        value=filters["date_range"].get("end", None)
                    )
                else:
                    start_date = None
                    end_date = None
                    
            with cols[3]:
                reset = st.button("Reset Filters")
                
            # Update filters
            new_filters = {
                "search_text": search_text,
                "status": status,
                "date_range": {
                    "start": start_date,
                    "end": end_date
                }
            }
            
            # Reset filters if button clicked
            if reset:
                new_filters = {
                    "search_text": "",
                    "status": [],
                    "date_range": {
                        "start": None,
                        "end": None
                    }
                }
                
            # Call callback if provided
            if on_filter_change and new_filters != filters:
                on_filter_change(new_filters)
            
            # Apply filters to items
            filtered_items = SearchManager._apply_filters(items, new_filters)
            
            # Show filter summary
            active_filters = []
            if search_text:
                active_filters.append(f"Search: '{search_text}'")
            if status:
                active_filters.append(f"Status: {', '.join(status)}")
            if start_date or end_date:
                date_filter = "Date: "
                if start_date:
                    date_filter += f"from {start_date.strftime('%Y-%m-%d')}"
                if start_date and end_date:
                    date_filter += " "
                if end_date:
                    date_filter += f"to {end_date.strftime('%Y-%m-%d')}"
                active_filters.append(date_filter)
                
            if active_filters:
                st.markdown(
                    f"<div style='font-size: 14px; color: #666; margin-bottom: 10px;'>"
                    f"Filters active: {' | '.join(active_filters)}</div>",
                    unsafe_allow_html=True
                )
                
            # Show filter result count
            if len(filtered_items) != len(items):
                st.markdown(
                    f"<div style='font-size: 14px; color: #666; margin-bottom: 10px;'>"
                    f"Showing {len(filtered_items)} of {len(items)} items</div>",
                    unsafe_allow_html=True
                )
            
            return filtered_items
    
    @staticmethod
    def _apply_filters(items, filters):
        """Apply filters to a list of items."""
        filtered_items = items.copy()
        
        # Apply text search filter
        if filters.get("search_text"):
            search_terms = filters["search_text"].lower().split()
            if search_terms:
                temp_items = []
                for item in filtered_items:
                    item_text = " ".join(str(v) for v in item.values() if v is not None).lower()
                    if all(term in item_text for term in search_terms):
                        temp_items.append(item)
                filtered_items = temp_items
        
        # Apply status filter
        if filters.get("status"):
            filtered_items = [item for item in filtered_items 
                              if item.get("status") in filters["status"]]
        
        # Apply date range filter
        if filters.get("date_range"):
            date_field = filters.get("date_field", "date")
            start_date = filters["date_range"].get("start")
            end_date = filters["date_range"].get("end")
            
            if start_date or end_date:
                temp_items = []
                for item in filtered_items:
                    item_date_str = item.get(date_field)
                    if not item_date_str:
                        continue
                        
                    try:
                        item_date = datetime.strptime(item_date_str, "%Y-%m-%d").date()
                        
                        if start_date and item_date < start_date:
                            continue
                            
                        if end_date and item_date > end_date:
                            continue
                            
                        temp_items.append(item)
                    except:
                        # Skip items with invalid dates
                        continue
                
                filtered_items = temp_items
        
        return filtered_items


# Initialize search manager instance
search_manager = SearchManager