"""
Pure Python BIM Engine for Highland Tower Development
Advanced BIM collaboration and clash detection using standard Python

Integrated comprehensive BIM platform capabilities with Highland Tower data
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date, timedelta
import math
import json

from .bim_models import (
    BIMElement, BIMModel, Clash, WorkInPlaceItem, QualityInspection, ProgressPhoto,
    SystemType, ElementStatus, ClashType, ClashStatus, Priority,
    HIGHLAND_TOWER_BIM_ELEMENTS, HIGHLAND_TOWER_BIM_CLASHES, HIGHLAND_TOWER_WORK_IN_PLACE
)
from .data_models import HIGHLAND_TOWER_PROJECT


class BIMManager:
    """Highland Tower Development BIM operations manager"""
    
    def __init__(self):
        self.project = HIGHLAND_TOWER_PROJECT
        self.elements: List[BIMElement] = HIGHLAND_TOWER_BIM_ELEMENTS.copy()
        self.clashes: List[Clash] = HIGHLAND_TOWER_BIM_CLASHES.copy()
        self.work_in_place: List[WorkInPlaceItem] = HIGHLAND_TOWER_WORK_IN_PLACE.copy()
        self.models: List[BIMModel] = []
        self.inspections: List[QualityInspection] = []
        self.progress_photos: List[ProgressPhoto] = []
    
    # Element Management Methods
    def get_elements(self, system_type: Optional[SystemType] = None, 
                    status: Optional[ElementStatus] = None,
                    level: Optional[str] = None) -> List[BIMElement]:
        """Get BIM elements with optional filtering"""
        elements = self.elements.copy()
        
        if system_type:
            elements = [e for e in elements if e.system_type == system_type]
        
        if status:
            elements = [e for e in elements if e.status == status]
        
        if level:
            elements = [e for e in elements if e.level == level]
        
        return elements
    
    def update_element_status(self, element_id: str, new_status: ElementStatus) -> bool:
        """Update element status"""
        for element in self.elements:
            if element.id == element_id:
                element.status = new_status
                element.updated_at = datetime.now()
                return True
        return False
    
    def get_element_by_id(self, element_id: str) -> Optional[BIMElement]:
        """Get specific element by ID"""
        for element in self.elements:
            if element.id == element_id:
                return element
        return None
    
    # Work In Place Tracking
    def get_work_in_place_summary(self) -> Dict[str, Any]:
        """Get work in place progress summary"""
        total_items = len(self.work_in_place)
        completed = len([w for w in self.work_in_place if w.status == ElementStatus.COMPLETE])
        in_progress = len([w for w in self.work_in_place if w.status == ElementStatus.IN_PROGRESS])
        not_started = len([w for w in self.work_in_place if w.status == ElementStatus.NOT_STARTED])
        
        # Calculate average progress
        total_progress = sum(w.progress_percentage for w in self.work_in_place)
        avg_progress = total_progress / total_items if total_items > 0 else 0
        
        # Progress by system
        system_progress = {}
        for system_type in SystemType:
            system_elements = [e for e in self.elements if e.system_type == system_type]
            system_work = [w for w in self.work_in_place 
                          if any(e.id == w.element_id and e.system_type == system_type 
                                for e in system_elements)]
            
            if system_work:
                system_avg = sum(w.progress_percentage for w in system_work) / len(system_work)
                system_progress[system_type.value] = round(system_avg, 1)
        
        return {
            "total_work_items": total_items,
            "completed": completed,
            "in_progress": in_progress,
            "not_started": not_started,
            "overall_progress": round(avg_progress, 1),
            "system_progress": system_progress
        }
    
    def update_work_progress(self, work_id: str, progress_percentage: float, 
                           notes: Optional[str] = None) -> bool:
        """Update work in place progress"""
        for work_item in self.work_in_place:
            if work_item.id == work_id:
                work_item.progress_percentage = min(100.0, max(0.0, progress_percentage))
                
                # Auto-update status based on progress
                if work_item.progress_percentage == 0:
                    work_item.status = ElementStatus.NOT_STARTED
                elif work_item.progress_percentage == 100:
                    work_item.status = ElementStatus.COMPLETE
                    work_item.actual_completion = date.today()
                else:
                    work_item.status = ElementStatus.IN_PROGRESS
                
                if notes:
                    work_item.notes.append(f"{datetime.now().strftime('%Y-%m-%d')}: {notes}")
                
                return True
        return False
    
    # Clash Detection and Management
    def run_clash_detection(self, tolerance_hard: float = 0.0, 
                          tolerance_soft: float = 25.0) -> List[Clash]:
        """Run clash detection analysis on Highland Tower elements"""
        new_clashes = []
        clash_id_counter = len(self.clashes) + 1
        
        # Compare all element pairs
        for i, element_a in enumerate(self.elements):
            for element_b in self.elements[i+1:]:
                # Skip same system comparisons for now (can be enabled)
                if element_a.system_type == element_b.system_type:
                    continue
                
                # Calculate clash
                clash_result = self._detect_element_clash(element_a, element_b, tolerance_hard, tolerance_soft)
                
                if clash_result:
                    clash = Clash(
                        id=f"HTD-CLASH-{clash_id_counter:03d}",
                        project_id=self.project.id,
                        element_a_id=element_a.id,
                        element_b_id=element_b.id,
                        clash_type=clash_result["type"],
                        status=ClashStatus.ACTIVE,
                        priority=clash_result["priority"],
                        distance=clash_result["distance"],
                        location=clash_result["location"],
                        description=f"{element_a.display_name} conflicts with {element_b.display_name}",
                        resolution=None,
                        detected_by="Highland BIM Engine",
                        created_by="Highland BIM Team",
                        assigned_to="BIM Coordinator"
                    )
                    
                    new_clashes.append(clash)
                    clash_id_counter += 1
        
        # Add new clashes to existing list
        self.clashes.extend(new_clashes)
        return new_clashes
    
    def _detect_element_clash(self, element_a: BIMElement, element_b: BIMElement,
                            tolerance_hard: float, tolerance_soft: float) -> Optional[Dict[str, Any]]:
        """Detect clash between two elements"""
        # Simplified geometric clash detection using bounding boxes
        geom_a = element_a.geometry
        geom_b = element_b.geometry
        
        # Get bounding boxes
        bbox_a = self._get_bounding_box(geom_a)
        bbox_b = self._get_bounding_box(geom_b)
        
        # Check for overlap
        overlap = self._check_bbox_overlap(bbox_a, bbox_b)
        
        if overlap:
            # Calculate minimum distance
            distance = self._calculate_minimum_distance(bbox_a, bbox_b)
            
            # Determine clash type and priority
            if distance <= tolerance_hard:
                return {
                    "type": ClashType.HARD_CLASH,
                    "priority": Priority.CRITICAL,
                    "distance": distance,
                    "location": self._get_clash_location(bbox_a, bbox_b)
                }
            elif distance <= tolerance_soft:
                return {
                    "type": ClashType.SOFT_CLASH,
                    "priority": Priority.HIGH,
                    "distance": distance,
                    "location": self._get_clash_location(bbox_a, bbox_b)
                }
        
        return None
    
    def _get_bounding_box(self, geometry: Dict[str, Any]) -> Dict[str, Any]:
        """Get bounding box from geometry"""
        if "start_point" in geometry and "end_point" in geometry:
            # Linear element (beam, duct, conduit)
            start = geometry["start_point"]
            end = geometry["end_point"]
            width = geometry.get("width", 0)
            height = geometry.get("height", 0)
            
            return {
                "min_x": min(start["x"], end["x"]) - width/2,
                "max_x": max(start["x"], end["x"]) + width/2,
                "min_y": min(start["y"], end["y"]) - height/2,
                "max_y": max(start["y"], end["y"]) + height/2,
                "min_z": min(start["z"], end["z"]) - height/2,
                "max_z": max(start["z"], end["z"]) + height/2
            }
        
        # Default minimal bounding box
        return {
            "min_x": 0, "max_x": 100,
            "min_y": 0, "max_y": 100,
            "min_z": 0, "max_z": 100
        }
    
    def _check_bbox_overlap(self, bbox_a: Dict[str, Any], bbox_b: Dict[str, Any]) -> bool:
        """Check if two bounding boxes overlap"""
        return (bbox_a["min_x"] <= bbox_b["max_x"] and bbox_a["max_x"] >= bbox_b["min_x"] and
                bbox_a["min_y"] <= bbox_b["max_y"] and bbox_a["max_y"] >= bbox_b["min_y"] and
                bbox_a["min_z"] <= bbox_b["max_z"] and bbox_a["max_z"] >= bbox_b["min_z"])
    
    def _calculate_minimum_distance(self, bbox_a: Dict[str, Any], bbox_b: Dict[str, Any]) -> float:
        """Calculate minimum distance between bounding boxes"""
        # Calculate center points
        center_a = {
            "x": (bbox_a["min_x"] + bbox_a["max_x"]) / 2,
            "y": (bbox_a["min_y"] + bbox_a["max_y"]) / 2,
            "z": (bbox_a["min_z"] + bbox_a["max_z"]) / 2
        }
        
        center_b = {
            "x": (bbox_b["min_x"] + bbox_b["max_x"]) / 2,
            "y": (bbox_b["min_y"] + bbox_b["max_y"]) / 2,
            "z": (bbox_b["min_z"] + bbox_b["max_z"]) / 2
        }
        
        # Calculate 3D distance
        dx = center_a["x"] - center_b["x"]
        dy = center_a["y"] - center_b["y"]
        dz = center_a["z"] - center_b["z"]
        
        return math.sqrt(dx**2 + dy**2 + dz**2)
    
    def _get_clash_location(self, bbox_a: Dict[str, Any], bbox_b: Dict[str, Any]) -> Dict[str, float]:
        """Get clash location coordinates"""
        return {
            "x": (bbox_a["min_x"] + bbox_a["max_x"] + bbox_b["min_x"] + bbox_b["max_x"]) / 4,
            "y": (bbox_a["min_y"] + bbox_a["max_y"] + bbox_b["min_y"] + bbox_b["max_y"]) / 4,
            "z": (bbox_a["min_z"] + bbox_a["max_z"] + bbox_b["min_z"] + bbox_b["max_z"]) / 4
        }
    
    def get_clash_statistics(self) -> Dict[str, Any]:
        """Get clash detection statistics"""
        total_clashes = len(self.clashes)
        active_clashes = len([c for c in self.clashes if c.status == ClashStatus.ACTIVE])
        resolved_clashes = len([c for c in self.clashes if c.status == ClashStatus.RESOLVED])
        critical_clashes = len([c for c in self.clashes if c.priority == Priority.CRITICAL])
        
        # Clashes by type
        clash_types = {}
        for clash_type in ClashType:
            count = len([c for c in self.clashes if c.clash_type == clash_type])
            clash_types[clash_type.value] = count
        
        # Clashes by system interaction
        system_interactions = {}
        for clash in self.clashes:
            elem_a = self.get_element_by_id(clash.element_a_id)
            elem_b = self.get_element_by_id(clash.element_b_id)
            
            if elem_a and elem_b:
                interaction = f"{elem_a.system_type.value}-{elem_b.system_type.value}"
                system_interactions[interaction] = system_interactions.get(interaction, 0) + 1
        
        return {
            "total_clashes": total_clashes,
            "active_clashes": active_clashes,
            "resolved_clashes": resolved_clashes,
            "critical_clashes": critical_clashes,
            "resolution_rate": (resolved_clashes / total_clashes * 100) if total_clashes > 0 else 0,
            "clash_types": clash_types,
            "system_interactions": system_interactions
        }
    
    def update_clash_status(self, clash_id: str, new_status: ClashStatus, 
                          resolution: Optional[str] = None) -> bool:
        """Update clash status"""
        for clash in self.clashes:
            if clash.id == clash_id:
                clash.status = new_status
                if resolution:
                    clash.resolution = resolution
                if new_status == ClashStatus.RESOLVED:
                    clash.resolved_at = datetime.now()
                return True
        return False
    
    # Progress Analytics
    def get_system_progress_analytics(self) -> Dict[str, Any]:
        """Get detailed system progress analytics"""
        analytics = {}
        
        for system_type in SystemType:
            system_elements = self.get_elements(system_type=system_type)
            system_work = [w for w in self.work_in_place 
                          if any(e.id == w.element_id for e in system_elements)]
            
            if system_elements:
                # Status distribution
                status_counts = {}
                for status in ElementStatus:
                    count = len([e for e in system_elements if e.status == status])
                    status_counts[status.value] = count
                
                # Progress metrics
                if system_work:
                    avg_progress = sum(w.progress_percentage for w in system_work) / len(system_work)
                    on_schedule = len([w for w in system_work 
                                     if w.target_completion and (not w.actual_completion or 
                                                               w.actual_completion <= w.target_completion)])
                    delayed = len(system_work) - on_schedule
                else:
                    avg_progress = 0
                    on_schedule = 0
                    delayed = 0
                
                analytics[system_type.value] = {
                    "total_elements": len(system_elements),
                    "status_distribution": status_counts,
                    "average_progress": round(avg_progress, 1),
                    "work_items": len(system_work),
                    "on_schedule": on_schedule,
                    "delayed": delayed
                }
        
        return analytics
    
    def get_bim_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive BIM dashboard data"""
        work_summary = self.get_work_in_place_summary()
        clash_stats = self.get_clash_statistics()
        system_analytics = self.get_system_progress_analytics()
        
        return {
            "highland_tower_bim": {
                "project_name": self.project.name,
                "project_value": f"${self.project.value:,.0f}",
                "total_elements": len(self.elements),
                "systems_count": len(SystemType),
                "progress_summary": work_summary,
                "clash_summary": clash_stats,
                "system_analytics": system_analytics,
                "last_updated": datetime.now().isoformat()
            }
        }
    
    def export_bim_data(self) -> Dict[str, Any]:
        """Export comprehensive BIM data"""
        return {
            "highland_tower_bim_export": {
                "project": {
                    "id": self.project.id,
                    "name": self.project.name,
                    "value": self.project.value
                },
                "elements": [
                    {
                        "id": e.id,
                        "name": e.name,
                        "system_type": e.system_type.value,
                        "element_type": e.element_type,
                        "status": e.status.value,
                        "level": e.level,
                        "location": e.location_description,
                        "properties": e.properties
                    }
                    for e in self.elements
                ],
                "clashes": [
                    {
                        "id": c.id,
                        "type": c.clash_type.value,
                        "status": c.status.value,
                        "priority": c.priority.value,
                        "distance": c.distance,
                        "description": c.description,
                        "days_open": c.days_open
                    }
                    for c in self.clashes
                ],
                "work_in_place": [
                    {
                        "id": w.id,
                        "work_type": w.work_type,
                        "status": w.status.value,
                        "progress": w.progress_percentage,
                        "assigned_to": w.assigned_to
                    }
                    for w in self.work_in_place
                ],
                "export_timestamp": datetime.now().isoformat()
            }
        }


# Global Highland Tower BIM manager instance
highland_bim_manager = BIMManager()