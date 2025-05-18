"""
Entity relationships management module for the gcPanel Construction Management Dashboard.

This module provides classes and functions for managing connections between different
entities in the system, such as documents, RFIs, submittals, etc.
"""

import streamlit as st
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional, Union, Tuple

class RelationshipType(Enum):
    """Types of relationships between entities."""
    REFERENCES = "References"  # For general references
    PARENT_CHILD = "Parent-Child"  # For hierarchical relationships
    DERIVED_FROM = "Derived From"  # For items created from others (e.g., RFI from an issue)
    RESPONSE_TO = "Response To"  # For items responding to others (e.g., submittal approval)
    ATTACHMENT = "Attachment"  # For documents attached to items
    SUPERSEDES = "Supersedes"  # For items that replace others
    DEPENDS_ON = "Depends On"  # For items that depend on others


class EntityRelationship:
    """Represents a relationship between two entities in the system."""
    
    def __init__(
        self, 
        from_entity_id: str,
        from_entity_type: str,
        to_entity_id: str,
        to_entity_type: str,
        relationship_type: RelationshipType,
        created_at: datetime = None,
        created_by: str = None,
        metadata: Dict[str, Any] = None
    ):
        """Initialize a new entity relationship.
        
        Args:
            from_entity_id: ID of the source entity
            from_entity_type: Type of the source entity
            to_entity_id: ID of the target entity
            to_entity_type: Type of the target entity
            relationship_type: Type of relationship
            created_at: When the relationship was created
            created_by: Who created the relationship
            metadata: Additional metadata about the relationship
        """
        self.from_entity_id = from_entity_id
        self.from_entity_type = from_entity_type
        self.to_entity_id = to_entity_id
        self.to_entity_type = to_entity_type
        self.relationship_type = relationship_type
        self.created_at = created_at or datetime.now()
        self.created_by = created_by
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the relationship to a dictionary."""
        return {
            "from_entity_id": self.from_entity_id,
            "from_entity_type": self.from_entity_type,
            "to_entity_id": self.to_entity_id,
            "to_entity_type": self.to_entity_type,
            "relationship_type": self.relationship_type.value,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EntityRelationship':
        """Create a relationship from a dictionary."""
        return cls(
            from_entity_id=data["from_entity_id"],
            from_entity_type=data["from_entity_type"],
            to_entity_id=data["to_entity_id"],
            to_entity_type=data["to_entity_type"],
            relationship_type=RelationshipType(data["relationship_type"]),
            created_at=data.get("created_at"),
            created_by=data.get("created_by"),
            metadata=data.get("metadata", {})
        )


class RelationshipManager:
    """Manages relationships between entities in the system."""
    
    def __init__(self):
        """Initialize the relationship manager."""
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state for relationships."""
        if "entity_relationships" not in st.session_state:
            st.session_state.entity_relationships = []
    
    def create_relationship(
        self,
        from_entity_id: str,
        from_entity_type: str,
        to_entity_id: str,
        to_entity_type: str,
        relationship_type: RelationshipType,
        created_by: str = None,
        metadata: Dict[str, Any] = None
    ) -> EntityRelationship:
        """Create a new relationship between entities.
        
        Args:
            from_entity_id: ID of the source entity
            from_entity_type: Type of the source entity
            to_entity_id: ID of the target entity
            to_entity_type: Type of the target entity
            relationship_type: Type of relationship
            created_by: Who created the relationship
            metadata: Additional metadata about the relationship
            
        Returns:
            The created relationship
        """
        relationship = EntityRelationship(
            from_entity_id=from_entity_id,
            from_entity_type=from_entity_type,
            to_entity_id=to_entity_id,
            to_entity_type=to_entity_type,
            relationship_type=relationship_type,
            created_by=created_by,
            metadata=metadata
        )
        
        st.session_state.entity_relationships.append(relationship.to_dict())
        return relationship
    
    def get_relationships_for_entity(
        self,
        entity_id: str,
        entity_type: str,
        as_source: bool = True,
        as_target: bool = True,
        relationship_types: List[RelationshipType] = None
    ) -> List[Dict[str, Any]]:
        """Get relationships involving a specific entity.
        
        Args:
            entity_id: ID of the entity to find relationships for
            entity_type: Type of the entity
            as_source: Whether to include relationships where the entity is the source
            as_target: Whether to include relationships where the entity is the target
            relationship_types: Optional filter for relationship types
            
        Returns:
            List of relationships involving the entity
        """
        relationships = []
        
        for rel_dict in st.session_state.entity_relationships:
            rel_type = RelationshipType(rel_dict["relationship_type"])
            
            # Filter by relationship type if specified
            if relationship_types and rel_type not in relationship_types:
                continue
            
            # Check if entity is source or target
            is_source = (rel_dict["from_entity_id"] == entity_id and 
                         rel_dict["from_entity_type"] == entity_type)
            is_target = (rel_dict["to_entity_id"] == entity_id and 
                         rel_dict["to_entity_type"] == entity_type)
            
            if (as_source and is_source) or (as_target and is_target):
                relationships.append(rel_dict)
        
        return relationships
    
    def get_related_entities(
        self,
        entity_id: str,
        entity_type: str,
        related_entity_type: str = None,
        relationship_types: List[RelationshipType] = None
    ) -> List[Tuple[Dict[str, Any], bool]]:
        """Get entities related to a specific entity.
        
        Args:
            entity_id: ID of the entity to find related entities for
            entity_type: Type of the entity
            related_entity_type: Optional filter for related entity type
            relationship_types: Optional filter for relationship types
            
        Returns:
            List of tuples of (entity ID, is_source) for related entities
        """
        related_entities = []
        
        for rel_dict in st.session_state.entity_relationships:
            rel_type = RelationshipType(rel_dict["relationship_type"])
            
            # Filter by relationship type if specified
            if relationship_types and rel_type not in relationship_types:
                continue
            
            # Check if entity is source
            if rel_dict["from_entity_id"] == entity_id and rel_dict["from_entity_type"] == entity_type:
                if related_entity_type is None or rel_dict["to_entity_type"] == related_entity_type:
                    related_entities.append((rel_dict["to_entity_id"], rel_dict["to_entity_type"], False))
            
            # Check if entity is target
            elif rel_dict["to_entity_id"] == entity_id and rel_dict["to_entity_type"] == entity_type:
                if related_entity_type is None or rel_dict["from_entity_type"] == related_entity_type:
                    related_entities.append((rel_dict["from_entity_id"], rel_dict["from_entity_type"], True))
        
        return related_entities
    
    def delete_relationship(
        self,
        from_entity_id: str,
        from_entity_type: str,
        to_entity_id: str,
        to_entity_type: str,
        relationship_type: RelationshipType = None
    ) -> bool:
        """Delete a relationship between entities.
        
        Args:
            from_entity_id: ID of the source entity
            from_entity_type: Type of the source entity
            to_entity_id: ID of the target entity
            to_entity_type: Type of the target entity
            relationship_type: Optional specific relationship type to delete
            
        Returns:
            Whether any relationships were deleted
        """
        initial_count = len(st.session_state.entity_relationships)
        
        st.session_state.entity_relationships = [
            rel for rel in st.session_state.entity_relationships
            if not (
                rel["from_entity_id"] == from_entity_id and
                rel["from_entity_type"] == from_entity_type and
                rel["to_entity_id"] == to_entity_id and
                rel["to_entity_type"] == to_entity_type and
                (relationship_type is None or rel["relationship_type"] == relationship_type.value)
            )
        ]
        
        return len(st.session_state.entity_relationships) < initial_count
    
    def render_entity_relationships(
        self,
        entity_id: str,
        entity_type: str,
        allow_add: bool = True,
        allow_remove: bool = True
    ):
        """Render a UI component for viewing and managing entity relationships.
        
        Args:
            entity_id: ID of the entity to show relationships for
            entity_type: Type of the entity
            allow_add: Whether to allow adding new relationships
            allow_remove: Whether to allow removing relationships
        """
        st.subheader("Related Items")
        
        # Get all relationships for this entity
        relationships = self.get_relationships_for_entity(entity_id, entity_type)
        
        if not relationships:
            st.info("No related items found.")
        else:
            # Group by relationship type
            grouped_relationships = {}
            for rel in relationships:
                rel_type = rel["relationship_type"]
                if rel_type not in grouped_relationships:
                    grouped_relationships[rel_type] = []
                grouped_relationships[rel_type].append(rel)
            
            # Display relationships by type
            for rel_type, rels in grouped_relationships.items():
                with st.expander(f"{rel_type} ({len(rels)})", expanded=True):
                    for rel in rels:
                        # Determine if this entity is the source or target
                        is_source = rel["from_entity_id"] == entity_id and rel["from_entity_type"] == entity_type
                        
                        # Get the related entity details
                        related_id = rel["to_entity_id"] if is_source else rel["from_entity_id"]
                        related_type = rel["to_entity_type"] if is_source else rel["from_entity_type"]
                        
                        # Display relationship with the option to remove
                        col1, col2 = st.columns([5, 1])
                        with col1:
                            st.write(f"**{related_type}:** {related_id}")
                        
                        with col2:
                            if allow_remove:
                                if st.button("Remove", key=f"remove_rel_{rel['from_entity_id']}_{rel['to_entity_id']}"):
                                    self.delete_relationship(
                                        rel["from_entity_id"],
                                        rel["from_entity_type"],
                                        rel["to_entity_id"],
                                        rel["to_entity_type"]
                                    )
                                    st.rerun()
        
        # Add new relationship form
        if allow_add:
            with st.expander("Add Related Item"):
                with st.form(key=f"add_relationship_{entity_id}"):
                    related_type = st.selectbox(
                        "Item Type",
                        ["RFI", "Submittal", "Document", "Drawing", "Contract", "Change Order"]
                    )
                    
                    related_id = st.text_input("Item ID")
                    
                    rel_type = st.selectbox(
                        "Relationship Type",
                        [rt.value for rt in RelationshipType]
                    )
                    
                    is_source = st.radio(
                        "Direction",
                        ["This item references the selected item", "The selected item references this item"]
                    ) == "This item references the selected item"
                    
                    submitted = st.form_submit_button("Add Relationship")
                    
                    if submitted and related_id:
                        if is_source:
                            self.create_relationship(
                                from_entity_id=entity_id,
                                from_entity_type=entity_type,
                                to_entity_id=related_id,
                                to_entity_type=related_type,
                                relationship_type=RelationshipType(rel_type)
                            )
                        else:
                            self.create_relationship(
                                from_entity_id=related_id,
                                from_entity_type=related_type,
                                to_entity_id=entity_id,
                                to_entity_type=entity_type,
                                relationship_type=RelationshipType(rel_type)
                            )
                        st.success(f"Relationship added successfully!")
                        st.rerun()