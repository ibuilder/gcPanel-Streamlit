"""
Advanced Search Manager for gcPanel Highland Tower Development

Implements global search functionality with smart filters and suggestions
across all construction management modules.
"""

import streamlit as st
from typing import Dict, List, Any, Optional
import re
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
import logging

class SearchManager:
    """Enterprise search manager with global search capabilities"""
    
    def __init__(self):
        self.search_indexes = {}
        self.search_history = []
        self.setup_logging()
        self.initialize_search_indexes()
    
    def setup_logging(self):
        """Setup search operation logging"""
        self.logger = logging.getLogger('SearchManager')
    
    def initialize_search_indexes(self):
        """Initialize search indexes for Highland Tower Development"""
        self.search_indexes = {
            'rfis': {
                'fields': ['rfi_number', 'title', 'description', 'submitter', 'status'],
                'filters': ['status', 'priority', 'submitted_date']
            },
            'daily_reports': {
                'fields': ['report_date', 'foreman', 'weather_conditions', 'work_completed'],
                'filters': ['report_date', 'foreman', 'weather_conditions']
            },
            'quality_checks': {
                'fields': ['check_number', 'check_type', 'location', 'inspector', 'status'],
                'filters': ['status', 'priority', 'scheduled_date']
            },
            'clashes': {
                'fields': ['clash_number', 'description', 'location', 'disciplines', 'status'],
                'filters': ['status', 'priority', 'disciplines']
            },
            'personnel': {
                'fields': ['employee_id', 'name', 'trade', 'crew', 'status'],
                'filters': ['trade', 'crew', 'status']
            },
            'equipment': {
                'fields': ['equipment_id', 'name', 'type', 'status', 'location'],
                'filters': ['type', 'status', 'location']
            },
            'materials': {
                'fields': ['material_id', 'name', 'supplier', 'status', 'location'],
                'filters': ['status', 'supplier', 'delivery_date']
            }
        }
    
    def perform_global_search(self, query: str, filters: Dict = None) -> Dict[str, List[Dict]]:
        """Perform global search across all modules"""
        results = {}
        
        if not query or len(query.strip()) < 2:
            return results
        
        # Add to search history
        self.add_to_search_history(query, filters)
        
        # Search each module
        for module, config in self.search_indexes.items():
            module_results = self.search_module(module, query, filters)
            if module_results:
                results[module] = module_results
        
        return results
    
    def search_module(self, module: str, query: str, filters: Dict = None) -> List[Dict]:
        """Search within a specific module"""
        # This would integrate with actual database in production
        # For now, return sample results based on module
        
        sample_data = self.get_sample_module_data(module, query)
        return self.filter_results(sample_data, query, filters)
    
    def get_sample_module_data(self, module: str, query: str) -> List[Dict]:
        """Get sample data for demonstration (replace with real database queries)"""
        
        if module == 'rfis':
            return [
                {
                    'id': 'RFI-001',
                    'rfi_number': 'RFI-2025-001',
                    'title': 'Electrical outlet placement clarification',
                    'description': 'Need clarification on electrical outlet spacing in residential units',
                    'submitter': 'John Smith',
                    'status': 'Open',
                    'priority': 'Medium',
                    'module': 'RFIs'
                }
            ] if 'electrical' in query.lower() or 'outlet' in query.lower() else []
        
        elif module == 'daily_reports':
            return [
                {
                    'id': 'DR-001',
                    'report_date': '2025-05-24',
                    'foreman': 'Mike Rodriguez',
                    'weather_conditions': 'Sunny, 72°F',
                    'work_completed': 'Concrete pour Floor 12, Electrical rough-in Floor 8',
                    'module': 'Daily Reports'
                }
            ] if 'concrete' in query.lower() or 'floor' in query.lower() else []
        
        elif module == 'quality_checks':
            return [
                {
                    'id': 'QC-001',
                    'check_number': 'QC-2025-001',
                    'check_type': 'Concrete Pour Inspection',
                    'location': 'Floor 12 - East Wing',
                    'inspector': 'Sarah Chen',
                    'status': 'Completed',
                    'module': 'Quality Control'
                }
            ] if 'concrete' in query.lower() or 'inspection' in query.lower() else []
        
        return []
    
    def filter_results(self, data: List[Dict], query: str, filters: Dict = None) -> List[Dict]:
        """Filter and rank search results"""
        if not data:
            return []
        
        # Text matching with fuzzy search
        scored_results = []
        for item in data:
            score = self.calculate_relevance_score(item, query)
            if score > 30:  # Minimum relevance threshold
                item['relevance_score'] = score
                scored_results.append(item)
        
        # Apply additional filters
        if filters:
            scored_results = self.apply_filters(scored_results, filters)
        
        # Sort by relevance score
        scored_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return scored_results
    
    def calculate_relevance_score(self, item: Dict, query: str) -> int:
        """Calculate relevance score for search result"""
        max_score = 0
        query_lower = query.lower()
        
        # Check each field in the item
        for key, value in item.items():
            if isinstance(value, str):
                # Exact match gets highest score
                if query_lower in value.lower():
                    return 100
                
                # Fuzzy match for partial matches
                fuzzy_score = fuzz.partial_ratio(query_lower, value.lower())
                max_score = max(max_score, fuzzy_score)
        
        return max_score
    
    def apply_filters(self, results: List[Dict], filters: Dict) -> List[Dict]:
        """Apply additional filters to search results"""
        filtered_results = []
        
        for result in results:
            include_result = True
            
            for filter_key, filter_value in filters.items():
                if filter_key in result:
                    if isinstance(filter_value, list):
                        if result[filter_key] not in filter_value:
                            include_result = False
                            break
                    else:
                        if result[filter_key] != filter_value:
                            include_result = False
                            break
            
            if include_result:
                filtered_results.append(result)
        
        return filtered_results
    
    def add_to_search_history(self, query: str, filters: Dict = None):
        """Add search to history for analytics"""
        search_entry = {
            'query': query,
            'filters': filters or {},
            'timestamp': datetime.now().isoformat(),
            'user': st.session_state.get('username', 'unknown')
        }
        
        if 'search_history' not in st.session_state:
            st.session_state.search_history = []
        
        st.session_state.search_history.insert(0, search_entry)
        
        # Keep only last 50 searches
        st.session_state.search_history = st.session_state.search_history[:50]
    
    def get_search_suggestions(self, partial_query: str) -> List[str]:
        """Get search suggestions based on partial query"""
        suggestions = []
        
        # Common search terms for Highland Tower Development
        common_terms = [
            'electrical outlets', 'concrete pour', 'floor 12', 'rfi status',
            'daily reports', 'quality check', 'safety inspection', 'clash detection',
            'material delivery', 'equipment status', 'personnel schedule'
        ]
        
        for term in common_terms:
            if partial_query.lower() in term.lower():
                suggestions.append(term)
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def render_global_search_interface(self):
        """Render the global search interface"""
        st.markdown("### 🔍 Global Search - Highland Tower Development")
        
        # Search input with autocomplete
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "Search across all modules",
                placeholder="Search RFIs, reports, quality checks, personnel...",
                key="global_search_query"
            )
        
        with col2:
            search_button = st.button("🔍 Search", type="primary")
        
        # Search suggestions
        if search_query and len(search_query) > 1:
            suggestions = self.get_search_suggestions(search_query)
            if suggestions:
                st.markdown("**Suggestions:**")
                cols = st.columns(len(suggestions))
                for i, suggestion in enumerate(suggestions):
                    with cols[i]:
                        if st.button(suggestion, key=f"suggestion_{i}"):
                            st.session_state.global_search_query = suggestion
                            st.rerun()
        
        # Perform search
        if search_query and (search_button or len(search_query) > 2):
            self.render_search_results(search_query)
        
        # Recent searches
        self.render_recent_searches()
    
    def render_search_results(self, query: str):
        """Render search results"""
        st.markdown(f"#### Search Results for: '{query}'")
        
        # Perform search
        results = self.perform_global_search(query)
        
        if not results:
            st.info("No results found. Try different keywords or check spelling.")
            return
        
        # Display results by module
        for module, module_results in results.items():
            with st.expander(f"{module.title()} ({len(module_results)} results)", expanded=True):
                for result in module_results[:5]:  # Show top 5 per module
                    self.render_search_result_item(result)
    
    def render_search_result_item(self, result: Dict):
        """Render individual search result item"""
        module = result.get('module', 'Unknown')
        score = result.get('relevance_score', 0)
        
        # Create result card
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 5px 0; background: #f9f9f9;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{result.get('title', result.get('name', result.get('id', 'Unknown')))}</strong>
                    <span style="background: #007bff; color: white; padding: 2px 6px; border-radius: 3px; font-size: 12px; margin-left: 10px;">
                        {module}
                    </span>
                </div>
                <div style="color: #666; font-size: 12px;">
                    Relevance: {score}%
                </div>
            </div>
            <div style="margin-top: 5px; color: #666;">
                {result.get('description', result.get('work_completed', 'No description available'))[:100]}...
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action button
        if st.button(f"View Details", key=f"view_{result.get('id')}"):
            st.success(f"Opening {result.get('id')} in {module} module")
    
    def render_recent_searches(self):
        """Render recent search history"""
        if 'search_history' not in st.session_state or not st.session_state.search_history:
            return
        
        with st.expander("Recent Searches"):
            for i, search in enumerate(st.session_state.search_history[:5]):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(f"'{search['query']}'")
                with col2:
                    if st.button("🔄", key=f"repeat_search_{i}", help="Repeat search"):
                        st.session_state.global_search_query = search['query']
                        st.rerun()

@st.cache_resource
def get_search_manager():
    """Get cached search manager instance"""
    return SearchManager()