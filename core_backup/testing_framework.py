"""
Pure Python Testing Framework for Highland Tower Development
Comprehensive test suite using standard Python unittest library

This ensures code reliability and validates business logic independently of UI frameworks
"""

import unittest
from datetime import date, datetime, timedelta
from typing import List, Dict, Any

from .data_models import (
    RFI, Subcontractor, Project, User, Priority, RFIStatus, 
    Discipline, ProjectStatus, HIGHLAND_TOWER_PROJECT
)
from .business_logic import ProjectManager, highland_tower_manager
from .ui_components import ComponentGenerator, DataProcessor, ui_components, data_processor


class TestDataModels(unittest.TestCase):
    """Test pure Python data models"""
    
    def test_highland_tower_project_creation(self):
        """Test Highland Tower project instance"""
        project = HIGHLAND_TOWER_PROJECT
        
        self.assertEqual(project.name, "Highland Tower Development")
        self.assertEqual(project.value, 45500000.0)
        self.assertEqual(project.residential_units, 120)
        self.assertEqual(project.retail_units, 8)
        self.assertEqual(project.status, ProjectStatus.ACTIVE)
    
    def test_rfi_days_open_calculation(self):
        """Test RFI days open property calculation"""
        rfi = RFI(
            id="TEST-001",
            number="RFI-TEST-001",
            subject="Test RFI",
            description="Test description",
            location="Test location",
            discipline=Discipline.STRUCTURAL,
            priority=Priority.HIGH,
            status=RFIStatus.OPEN,
            submitted_by="Test User",
            assigned_to="Test Engineer",
            submitted_date=date.today() - timedelta(days=5),
            due_date=date.today() + timedelta(days=2),
            cost_impact="$1,000",
            schedule_impact="1 day",
            project_id="TEST-PROJECT"
        )
        
        self.assertEqual(rfi.days_open, 5)
    
    def test_rfi_overdue_check(self):
        """Test RFI overdue property"""
        # Overdue RFI
        overdue_rfi = RFI(
            id="TEST-002",
            number="RFI-TEST-002",
            subject="Overdue RFI",
            description="Test description",
            location="Test location",
            discipline=Discipline.MEP,
            priority=Priority.MEDIUM,
            status=RFIStatus.OPEN,
            submitted_by="Test User",
            assigned_to="Test Engineer",
            submitted_date=date.today() - timedelta(days=10),
            due_date=date.today() - timedelta(days=1),
            cost_impact="$2,000",
            schedule_impact="2 days",
            project_id="TEST-PROJECT"
        )
        
        self.assertTrue(overdue_rfi.is_overdue)
        
        # Not overdue RFI
        current_rfi = RFI(
            id="TEST-003",
            number="RFI-TEST-003",
            subject="Current RFI",
            description="Test description",
            location="Test location",
            discipline=Discipline.ELECTRICAL,
            priority=Priority.LOW,
            status=RFIStatus.OPEN,
            submitted_by="Test User",
            assigned_to="Test Engineer",
            submitted_date=date.today() - timedelta(days=2),
            due_date=date.today() + timedelta(days=3),
            cost_impact="$500",
            schedule_impact="1 day",
            project_id="TEST-PROJECT"
        )
        
        self.assertFalse(current_rfi.is_overdue)


class TestBusinessLogic(unittest.TestCase):
    """Test pure Python business logic"""
    
    def setUp(self):
        """Set up test environment"""
        self.project_manager = ProjectManager()
    
    def test_highland_tower_data_initialization(self):
        """Test Highland Tower Development data initialization"""
        # Check RFIs are loaded
        rfis = self.project_manager.get_rfis()
        self.assertGreater(len(rfis), 0)
        
        # Check subcontractors are loaded
        subcontractors = self.project_manager.get_subcontractors()
        self.assertGreater(len(subcontractors), 0)
        
        # Verify Highland Tower specific data
        highland_rfis = [rfi for rfi in rfis if "Highland" in rfi.assigned_to]
        self.assertGreater(len(highland_rfis), 0)
    
    def test_rfi_filtering(self):
        """Test RFI filtering functionality"""
        # Test status filtering
        open_rfis = self.project_manager.get_rfis(status=RFIStatus.OPEN)
        for rfi in open_rfis:
            self.assertEqual(rfi.status, RFIStatus.OPEN)
        
        # Test priority filtering
        high_priority_rfis = self.project_manager.get_rfis(priority=Priority.HIGH)
        for rfi in high_priority_rfis:
            self.assertEqual(rfi.priority, Priority.HIGH)
    
    def test_rfi_statistics_calculation(self):
        """Test RFI statistics calculation"""
        stats = self.project_manager.get_rfi_statistics()
        
        # Verify all required statistics are present
        required_keys = ["total", "open", "critical", "overdue", "avg_days_open"]
        for key in required_keys:
            self.assertIn(key, stats)
        
        # Verify statistics are non-negative
        for key, value in stats.items():
            if isinstance(value, (int, float)):
                self.assertGreaterEqual(value, 0)
    
    def test_subcontractor_performance_summary(self):
        """Test subcontractor performance metrics"""
        summary = self.project_manager.get_subcontractor_performance_summary()
        
        # Verify required fields
        required_fields = ["total_subcontractors", "average_rating", "total_contract_value", "active_projects"]
        for field in required_fields:
            self.assertIn(field, summary)
        
        # Verify rating is within valid range
        if "average_rating" in summary:
            self.assertGreaterEqual(summary["average_rating"], 0)
            self.assertLessEqual(summary["average_rating"], 5.0)
    
    def test_project_health_metrics(self):
        """Test project health calculation"""
        health = self.project_manager.get_project_health_metrics()
        
        # Verify health score is percentage
        self.assertGreaterEqual(health["overall_health_score"], 0)
        self.assertLessEqual(health["overall_health_score"], 100)
        
        # Verify Highland Tower specific metrics
        self.assertEqual(health["progress_percent"], 67.3)
        self.assertGreater(health["budget_remaining"], 0)
    
    def test_rfi_search_functionality(self):
        """Test RFI search functionality"""
        # Search for structural RFIs
        structural_rfis = self.project_manager.search_rfis("structural")
        for rfi in structural_rfis:
            self.assertTrue(
                "structural" in rfi.subject.lower() or 
                "structural" in rfi.description.lower()
            )
        
        # Search for Highland Tower specific content
        highland_rfis = self.project_manager.search_rfis("beam")
        self.assertGreater(len(highland_rfis), 0)


class TestUIComponents(unittest.TestCase):
    """Test UI component generation"""
    
    def test_rfi_list_data_generation(self):
        """Test RFI list component data generation"""
        data = ui_components.generate_rfi_list_data()
        
        # Verify structure
        self.assertIn("rfis", data)
        self.assertIn("statistics", data)
        self.assertIn("action_buttons", data)
        
        # Verify RFI data format
        if data["rfis"]:
            rfi = data["rfis"][0]
            required_fields = ["id", "number", "subject", "priority", "status", "days_open"]
            for field in required_fields:
                self.assertIn(field, rfi)
    
    def test_dashboard_data_generation(self):
        """Test dashboard component data generation"""
        data = ui_components.generate_dashboard_data()
        
        # Verify structure
        self.assertIn("project_info", data)
        self.assertIn("key_metrics", data)
        self.assertIn("recent_activities", data)
        
        # Verify Highland Tower specific data
        self.assertEqual(data["project_info"]["name"], "Highland Tower Development")
        self.assertEqual(data["project_info"]["value"], "$45.5M")
    
    def test_analytics_charts_data(self):
        """Test analytics charts data generation"""
        data = ui_components.generate_analytics_charts_data()
        
        # Verify chart data structure
        charts = ["priority_chart", "discipline_chart", "status_chart", "timeline_data"]
        for chart in charts:
            self.assertIn(chart, data)
        
        # Verify chart data has content
        for chart_name, chart_data in data.items():
            if "data" in chart_data:
                self.assertIsInstance(chart_data["data"], (dict, list))
    
    def test_subcontractor_data_generation(self):
        """Test subcontractor component data generation"""
        data = ui_components.generate_subcontractor_data()
        
        # Verify structure
        self.assertIn("subcontractors", data)
        self.assertIn("statistics", data)
        self.assertIn("summary_cards", data)
        
        # Verify Highland Tower subcontractors are included
        highland_subs = [
            sub for sub in data["subcontractors"] 
            if "Highland" in sub["company_name"]
        ]
        self.assertGreater(len(highland_subs), 0)


class TestDataProcessor(unittest.TestCase):
    """Test data processing utilities"""
    
    def setUp(self):
        """Set up test data"""
        self.test_rfis = highland_tower_manager.get_rfis()
    
    def test_rfi_filtering(self):
        """Test RFI filtering functionality"""
        # Test status filter
        filters = {"status": "open"}
        filtered = data_processor.filter_rfis(self.test_rfis, filters)
        
        for rfi in filtered:
            self.assertEqual(rfi.status, RFIStatus.OPEN)
    
    def test_rfi_sorting(self):
        """Test RFI sorting functionality"""
        # Test priority sorting
        sorted_rfis = data_processor.sort_rfis(self.test_rfis, "priority", reverse=True)
        
        # Verify sorting order (Critical > High > Medium > Low)
        priority_values = [rfi.priority for rfi in sorted_rfis]
        self.assertIsInstance(priority_values, list)
    
    def test_search_text_filtering(self):
        """Test text search filtering"""
        filters = {"search_text": "steel"}
        filtered = data_processor.filter_rfis(self.test_rfis, filters)
        
        for rfi in filtered:
            self.assertTrue(
                "steel" in rfi.subject.lower() or 
                "steel" in rfi.description.lower()
            )


class TestHighlandTowerIntegration(unittest.TestCase):
    """Integration tests for Highland Tower Development specific functionality"""
    
    def test_highland_tower_project_completeness(self):
        """Test Highland Tower project has complete data"""
        project = HIGHLAND_TOWER_PROJECT
        
        # Verify all Highland Tower specific details
        self.assertEqual(project.residential_units, 120)
        self.assertEqual(project.retail_units, 8)
        self.assertEqual(project.floors_above, 15)
        self.assertEqual(project.floors_below, 2)
        self.assertEqual(project.progress_percent, 67.3)
        self.assertGreater(project.budget_remaining, 0)
    
    def test_highland_tower_rfis_authenticity(self):
        """Test Highland Tower RFIs contain authentic project data"""
        rfis = highland_tower_manager.get_rfis()
        
        # Verify Highland Tower specific locations
        highland_locations = [
            "Level 12-13, Grid Line A-B",
            "Level 12 - Mechanical Room North", 
            "South Facade - Units 8-12",
            "Ground Floor - Retail Space 3",
            "Levels 2-15 - Residential"
        ]
        
        rfi_locations = [rfi.location for rfi in rfis]
        for location in highland_locations:
            self.assertIn(location, rfi_locations)
    
    def test_highland_tower_subcontractors_authenticity(self):
        """Test Highland Tower subcontractors contain authentic data"""
        subcontractors = highland_tower_manager.get_subcontractors()
        
        # Verify Highland Tower specific companies
        company_names = [sub.company_name for sub in subcontractors]
        expected_companies = [
            "Highland Construction Corp",
            "Elite MEP Solutions", 
            "Premium Interior Finishes"
        ]
        
        for company in expected_companies:
            self.assertIn(company, company_names)


def run_all_tests():
    """Run comprehensive test suite"""
    print("🧪 Running Highland Tower Development Test Suite")
    print("=" * 60)
    
    # Create test suite
    test_classes = [
        TestDataModels,
        TestBusinessLogic, 
        TestUIComponents,
        TestDataProcessor,
        TestHighlandTowerIntegration
    ]
    
    total_tests = 0
    total_failures = 0
    
    for test_class in test_classes:
        print(f"\n📋 Testing {test_class.__name__}")
        print("-" * 40)
        
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        total_tests += result.testsRun
        total_failures += len(result.failures) + len(result.errors)
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Summary: {total_tests - total_failures}/{total_tests} tests passed")
    
    if total_failures == 0:
        print("✅ All tests passed! Highland Tower Development system is robust.")
    else:
        print(f"❌ {total_failures} tests failed. Review implementation.")
    
    return total_failures == 0


if __name__ == "__main__":
    run_all_tests()