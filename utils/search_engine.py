"""
Global Search Engine for Highland Tower Development

Advanced search and filtering across all modules with intelligent suggestions.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Any, Optional
import re
import logging

class GlobalSearchEngine:
    """Advanced search engine for the Highland Tower Development dashboard."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.search_index = {}
        self.search_history = []
        
    def index_data(self, data: List[Dict[str, Any]]):
        """Index data for faster searching."""
        self.search_index = {}
        
        for item in data:
            # Create searchable text from all fields
            searchable_text = ""
            for key, value in item.items():
                if isinstance(value, (str, int, float)):
                    searchable_text += f" {str(value).lower()}"
            
            # Store with metadata
            item_id = item.get("id", f"item_{len(self.search_index)}")
            self.search_index[item_id] = {
                "data": item,
                "searchable_text": searchable_text,
                "module": item.get("module", "Unknown")
            }
    
    def search(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Perform intelligent search with filtering."""
        if not query or not self.search_index:
            return []
        
        query_lower = query.lower()
        results = []
        
        # Search through indexed data
        for item_id, indexed_item in self.search_index.items():
            score = self._calculate_relevance_score(query_lower, indexed_item)
            
            if score > 0:
                result = indexed_item["data"].copy()
                result["_search_score"] = score
                result["_search_highlights"] = self._get_highlights(query_lower, indexed_item)
                results.append(result)
        
        # Sort by relevance score
        results.sort(key=lambda x: x["_search_score"], reverse=True)
        
        # Apply filters if provided
        if filters:
            results = self._apply_filters(results, filters)
        
        # Add to search history
        self._add_to_history(query)
        
        return results[:50]  # Return top 50 results
    
    def _calculate_relevance_score(self, query: str, indexed_item: Dict[str, Any]) -> int:
        """Calculate relevance score for search results."""
        searchable_text = indexed_item["searchable_text"]
        score = 0
        
        # Exact phrase match (highest score)
        if query in searchable_text:
            score += 100
        
        # Individual word matches
        query_words = query.split()
        for word in query_words:
            if word in searchable_text:
                score += 10
                
                # Bonus for matches in important fields
                data = indexed_item["data"]
                if word in str(data.get("title", "")).lower():
                    score += 20
                if word in str(data.get("id", "")).lower():
                    score += 15
                if word in str(data.get("status", "")).lower():
                    score += 10
        
        return score
    
    def _get_highlights(self, query: str, indexed_item: Dict[str, Any]) -> List[str]:
        """Get highlighted text snippets for search results."""
        highlights = []
        data = indexed_item["data"]
        
        # Check important fields for highlights
        important_fields = ["title", "description", "id", "status"]
        
        for field in important_fields:
            if field in data:
                field_text = str(data[field])
                if query in field_text.lower():
                    # Extract snippet around the match
                    match_start = field_text.lower().find(query)
                    start = max(0, match_start - 30)
                    end = min(len(field_text), match_start + len(query) + 30)
                    snippet = field_text[start:end]
                    
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(field_text):
                        snippet = snippet + "..."
                    
                    highlights.append(snippet)
        
        return highlights[:3]  # Return top 3 highlights
    
    def _apply_filters(self, results: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply filters to search results."""
        filtered_results = results
        
        # Module filter
        if "module" in filters and filters["module"]:
            filtered_results = [r for r in filtered_results if r.get("module") == filters["module"]]
        
        # Status filter
        if "status" in filters and filters["status"]:
            filtered_results = [r for r in filtered_results if r.get("status") == filters["status"]]
        
        # Date range filter
        if "date_from" in filters and filters["date_from"]:
            # Implementation for date filtering
            pass
        
        return filtered_results
    
    def _add_to_history(self, query: str):
        """Add search query to history."""
        if "search_history" not in st.session_state:
            st.session_state.search_history = []
        
        # Remove duplicate if exists
        if query in st.session_state.search_history:
            st.session_state.search_history.remove(query)
        
        # Add to beginning
        st.session_state.search_history.insert(0, query)
        
        # Keep only last 20 searches
        st.session_state.search_history = st.session_state.search_history[:20]
    
    def get_search_suggestions(self, partial_query: str) -> List[str]:
        """Get search suggestions based on partial query."""
        if not partial_query or len(partial_query) < 2:
            return []
        
        suggestions = []
        
        # Get suggestions from search history
        history = st.session_state.get("search_history", [])
        for query in history:
            if partial_query.lower() in query.lower():
                suggestions.append(query)
        
        # Get suggestions from indexed data
        common_terms = set()
        for indexed_item in self.search_index.values():
            data = indexed_item["data"]
            for field in ["title", "id", "status"]:
                if field in data:
                    text = str(data[field]).lower()
                    if partial_query.lower() in text:
                        common_terms.add(data[field])
        
        suggestions.extend(list(common_terms))
        
        # Remove duplicates and limit
        unique_suggestions = list(dict.fromkeys(suggestions))
        return unique_suggestions[:10]
    
    def get_popular_searches(self) -> List[str]:
        """Get popular search terms."""
        # This would be enhanced with actual usage analytics
        return [
            "RFI status",
            "submittal approval",
            "safety inspection",
            "schedule delay",
            "Highland Tower progress",
            "transmittal pending"
        ]