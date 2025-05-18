"""
Relationship picker component for selecting and managing relationships between entities.

This component allows users to create connections between different entities
such as RFIs, submittals, documents, drawings, etc.
"""

import streamlit as st
from typing import List, Dict, Any, Optional, Tuple

from core.relationships.entity_relationships import RelationshipManager, RelationshipType

def render_relationship_picker(
    entity_id: str,
    entity_type: str,
    allow_multiple: bool = True,
    suggested_types: List[str] = None,
    key_prefix: str = ""
) -> List[Dict[str, Any]]:
    """
    Render a component for selecting and managing relationships to other entities.
    
    Args:
        entity_id: ID of the current entity
        entity_type: Type of the current entity
        allow_multiple: Whether to allow selecting multiple relationships
        suggested_types: Optional list of entity types to suggest
        key_prefix: Prefix for Streamlit keys to avoid conflicts
    
    Returns:
        List of selected relationships
    """
    if not suggested_types:
        suggested_types = ["RFI", "Submittal", "Document", "Drawing", "Contract", "Change Order", "Transmittal"]
    
    # Initialize relationship manager
    manager = RelationshipManager()
    
    # Get existing relationships
    existing_relationships = manager.get_relationships_for_entity(entity_id, entity_type)
    
    # Show existing relationships if any
    if existing_relationships:
        st.write("**Related Items:**")
        for rel in existing_relationships:
            # Determine if this entity is the source or target
            is_source = rel["from_entity_id"] == entity_id and rel["from_entity_type"] == entity_type
            
            # Get the related entity details
            related_id = rel["to_entity_id"] if is_source else rel["from_entity_id"]
            related_type = rel["to_entity_type"] if is_source else rel["from_entity_type"]
            
            # Display relationship with the option to remove
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"- **{related_type}** {related_id} ({rel['relationship_type']})")
            
            with col2:
                if st.button("Remove", key=f"{key_prefix}_remove_rel_{rel['from_entity_id']}_{rel['to_entity_id']}"):
                    manager.delete_relationship(
                        rel["from_entity_id"],
                        rel["from_entity_type"],
                        rel["to_entity_id"],
                        rel["to_entity_type"]
                    )
                    st.rerun()
    
    # Add new relationship
    st.write("**Add Related Item:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        related_type = st.selectbox(
            "Item Type",
            suggested_types,
            key=f"{key_prefix}_related_type"
        )
    
    with col2:
        rel_type = st.selectbox(
            "Relationship",
            [rt.value for rt in RelationshipType],
            key=f"{key_prefix}_rel_type"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        related_id = st.text_input("Item ID", key=f"{key_prefix}_related_id")
    
    with col2:
        is_source = st.radio(
            "Direction",
            ["This references that", "That references this"],
            key=f"{key_prefix}_direction"
        ) == "This references that"
    
    if st.button("Add Relationship", key=f"{key_prefix}_add_rel_btn"):
        if related_id:
            if is_source:
                manager.create_relationship(
                    from_entity_id=entity_id,
                    from_entity_type=entity_type,
                    to_entity_id=related_id,
                    to_entity_type=related_type,
                    relationship_type=RelationshipType(rel_type)
                )
            else:
                manager.create_relationship(
                    from_entity_id=related_id,
                    from_entity_type=related_type,
                    to_entity_id=entity_id,
                    to_entity_type=entity_type,
                    relationship_type=RelationshipType(rel_type)
                )
            st.success("Relationship added!")
            st.rerun()
    
    return existing_relationships


def render_document_relationship_picker(
    entity_id: str,
    entity_type: str,
    key_prefix: str = ""
) -> List[Dict[str, Any]]:
    """
    Render a specialized picker for document relationships.
    
    Args:
        entity_id: ID of the current entity
        entity_type: Type of the current entity
        key_prefix: Prefix for Streamlit keys to avoid conflicts
    
    Returns:
        List of selected document relationships
    """
    # Initialize relationship manager
    manager = RelationshipManager()
    
    # Get existing document relationships
    existing_relationships = manager.get_relationships_for_entity(
        entity_id, 
        entity_type,
        relationship_types=[RelationshipType.ATTACHMENT]
    )
    
    # Filter for document types
    document_relationships = [
        rel for rel in existing_relationships
        if (rel["from_entity_type"] == "Document" or rel["to_entity_type"] == "Document" or
            rel["from_entity_type"] == "Drawing" or rel["to_entity_type"] == "Drawing")
    ]
    
    # Show existing document relationships if any
    if document_relationships:
        st.write("**Attached Documents:**")
        for rel in document_relationships:
            # Determine if this entity is the source or target
            is_source = rel["from_entity_id"] == entity_id and rel["from_entity_type"] == entity_type
            
            # Get the document details
            doc_id = rel["to_entity_id"] if is_source else rel["from_entity_id"]
            doc_type = rel["to_entity_type"] if is_source else rel["from_entity_type"]
            
            # Display document with the option to remove
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"- **{doc_type}:** {doc_id}")
            
            with col2:
                if st.button("Remove", key=f"{key_prefix}_remove_doc_{doc_id}"):
                    manager.delete_relationship(
                        rel["from_entity_id"],
                        rel["from_entity_type"],
                        rel["to_entity_id"],
                        rel["to_entity_type"]
                    )
                    st.rerun()
    
    # Add new document relationship
    st.write("**Attach Document:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        doc_type = st.selectbox(
            "Document Type",
            ["Document", "Drawing", "Specification", "Photo"],
            key=f"{key_prefix}_doc_type"
        )
    
    with col2:
        doc_id = st.text_input("Document ID/Name", key=f"{key_prefix}_doc_id")
    
    if st.button("Attach Document", key=f"{key_prefix}_attach_doc_btn"):
        if doc_id:
            manager.create_relationship(
                from_entity_id=entity_id,
                from_entity_type=entity_type,
                to_entity_id=doc_id,
                to_entity_type=doc_type,
                relationship_type=RelationshipType.ATTACHMENT
            )
            st.success("Document attached!")
            st.rerun()
    
    return document_relationships