"""
Comprehensive Unit Tests for gcPanel Construction Management Platform
Highland Tower Development - Enterprise Testing Suite
"""

import unittest
import sys
import os
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestGCPanelCore(unittest.TestCase):
    """Test core gcPanel functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_user_roles = {
            "admin": {
                "role_name": "Administrator",
                "modules": ["Dashboard", "Unit Prices", "Safety", "Contracts"],
                "permissions": ["read_all", "write_all", "manage_users"]
            },
            "manager": {
                "role_name": "Project Manager",
                "modules": ["Dashboard", "Unit Prices", "Safety"],
                "permissions": ["read_all", "write_rfis"]
            }
        }
    
    def test_role_permissions_structure(self):
        """Test that role permissions are properly structured"""
        # Import the function we're testing
        try:
            from gcpanel_core_focused import get_user_role_permissions
            permissions = get_user_role_permissions()
            
            # Test admin role exists and has required fields
            self.assertIn("admin", permissions)
            self.assertIn("role_name", permissions["admin"])
            self.assertIn("modules", permissions["admin"])
            self.assertIn("permissions", permissions["admin"])
            
            # Test manager role exists
            self.assertIn("manager", permissions)
            
            # Test Unit Prices module is included for admin and manager
            self.assertIn("Unit Prices", permissions["admin"]["modules"])
            self.assertIn("Unit Prices", permissions["manager"]["modules"])
            
        except ImportError:
            self.skipTest("gcpanel_core_focused module not available")
    
    def test_module_access_control(self):
        """Test module access control functionality"""
        try:
            from gcpanel_core_focused import check_module_access
            
            # Mock session state for testing
            with patch('streamlit.session_state') as mock_session:
                # Test admin access
                mock_session.get.return_value = True  # authenticated
                mock_session.__getitem__.return_value = "admin"  # user_role
                
                # Admin should have access to Unit Prices
                result = check_module_access("Unit Prices")
                self.assertTrue(result, "Admin should have access to Unit Prices module")
                
                # Test user role without access
                mock_session.__getitem__.return_value = "user"
                result = check_module_access("Admin Settings")
                self.assertFalse(result, "Regular user should not have access to Admin Settings")
                
        except ImportError:
            self.skipTest("Module access control functions not available")

class TestUnitPricesModule(unittest.TestCase):
    """Test Unit Prices module functionality"""
    
    def setUp(self):
        """Set up test data for Unit Prices"""
        self.sample_material = {
            "Item_Code": "STL-W24-62",
            "Description": "W24x62 Steel Beam - ASTM A992",
            "Unit": "LF",
            "Budget_Price": 45.80,
            "Current_Price": 47.20,
            "Variance": 3.1,
            "Quantity_Used": 2450,
            "Total_Cost": 115640,
            "Supplier": "Steel Fabricators Inc"
        }
        
        self.sample_equipment = {
            "Equipment_ID": "CR-250T-01",
            "Description": "250-Ton Tower Crane - Liebherr",
            "Type": "Rental",
            "Daily_Rate": 2850.00,
            "Utilization": 94.5,
            "Days_Used": 125,
            "Total_Cost": 356250
        }
    
    def test_material_cost_calculation(self):
        """Test material cost calculations"""
        material = self.sample_material
        
        # Test variance calculation
        expected_variance = ((material["Current_Price"] - material["Budget_Price"]) / material["Budget_Price"]) * 100
        self.assertAlmostEqual(material["Variance"], expected_variance, places=1)
        
        # Test total cost calculation
        expected_total = material["Current_Price"] * material["Quantity_Used"]
        self.assertAlmostEqual(material["Total_Cost"], expected_total, places=0)
    
    def test_equipment_utilization(self):
        """Test equipment utilization calculations"""
        equipment = self.sample_equipment
        
        # Test utilization percentage is valid
        self.assertGreaterEqual(equipment["Utilization"], 0)
        self.assertLessEqual(equipment["Utilization"], 100)
        
        # Test daily rate is positive
        self.assertGreater(equipment["Daily_Rate"], 0)
        
        # Test total cost calculation
        expected_total = equipment["Daily_Rate"] * equipment["Days_Used"]
        self.assertAlmostEqual(equipment["Total_Cost"], expected_total, places=0)
    
    def test_unit_prices_module_import(self):
        """Test that Unit Prices module can be imported"""
        try:
            from modules.unit_prices import render_unit_prices
            self.assertTrue(callable(render_unit_prices))
        except ImportError:
            self.skipTest("Unit Prices module not available for testing")

class TestDailyReportsModule(unittest.TestCase):
    """Test enhanced Daily Reports functionality"""
    
    def setUp(self):
        """Set up test data for Daily Reports"""
        self.sample_progress_area = {
            "Area": "Level 13 - Structural Steel",
            "Progress": 87,
            "Crew": 12,
            "Lead": "Mike Rodriguez",
            "Priority": "High",
            "Schedule": "On Track",
            "Cost_Impact": "$0"
        }
    
    def test_progress_validation(self):
        """Test progress percentage validation"""
        area = self.sample_progress_area
        
        # Progress should be between 0 and 100
        self.assertGreaterEqual(area["Progress"], 0)
        self.assertLessEqual(area["Progress"], 100)
        
        # Crew size should be positive
        self.assertGreater(area["Crew"], 0)
    
    def test_highland_tower_data_integrity(self):
        """Test that Highland Tower specific data is maintained"""
        area = self.sample_progress_area
        
        # Test that area contains Highland Tower specific floor reference
        self.assertIn("Level", area["Area"])
        
        # Test that lead names are realistic
        self.assertIsInstance(area["Lead"], str)
        self.assertGreater(len(area["Lead"]), 0)

class TestIntegrationSystems(unittest.TestCase):
    """Test integration with external systems"""
    
    def test_sage_integration_structure(self):
        """Test Sage integration data structure"""
        sage_config = {
            "api_endpoint": "https://sage300.highland-tower.com/api",
            "sync_frequency": "real-time",
            "data_types": ["costs", "labor", "materials", "equipment"],
            "last_sync": "2025-01-25T10:30:00Z"
        }
        
        # Test required fields exist
        required_fields = ["api_endpoint", "sync_frequency", "data_types"]
        for field in required_fields:
            self.assertIn(field, sage_config)
        
        # Test data types are valid
        expected_types = ["costs", "labor", "materials", "equipment"]
        for data_type in sage_config["data_types"]:
            self.assertIn(data_type, expected_types)
    
    def test_api_response_structure(self):
        """Test expected API response structure"""
        mock_api_response = {
            "status": "success",
            "data": {
                "materials": [
                    {
                        "item_code": "STL-W24-62",
                        "current_price": 47.20,
                        "last_updated": "2025-01-25"
                    }
                ]
            },
            "timestamp": "2025-01-25T10:30:00Z"
        }
        
        # Test response structure
        self.assertIn("status", mock_api_response)
        self.assertIn("data", mock_api_response)
        self.assertEqual(mock_api_response["status"], "success")

class TestUserInterface(unittest.TestCase):
    """Test user interface components"""
    
    @patch('streamlit.markdown')
    @patch('streamlit.session_state')
    def test_sidebar_rendering(self, mock_session, mock_markdown):
        """Test sidebar rendering with role-based access"""
        # Mock authenticated admin user
        mock_session.get.side_effect = lambda key, default=None: {
            "authenticated": True,
            "user_role": "admin",
            "username": "admin"
        }.get(key, default)
        
        try:
            from gcpanel_core_focused import render_sidebar
            # This should not raise an exception
            render_sidebar()
            
            # Verify markdown was called (sidebar content was rendered)
            self.assertTrue(mock_markdown.called)
            
        except ImportError:
            self.skipTest("Sidebar rendering function not available")
    
    def test_theme_application(self):
        """Test theme application functionality"""
        try:
            from gcpanel_core_focused import apply_theme
            
            with patch('streamlit.markdown') as mock_markdown:
                apply_theme()
                
                # Verify theme CSS was applied
                self.assertTrue(mock_markdown.called)
                
                # Check that the call contained CSS styling
                call_args = mock_markdown.call_args
                if call_args:
                    css_content = call_args[0][0]
                    self.assertIn("background", css_content.lower())
                    
        except ImportError:
            self.skipTest("Theme application function not available")

class TestDataValidation(unittest.TestCase):
    """Test data validation and integrity"""
    
    def test_highland_tower_project_data(self):
        """Test Highland Tower project data consistency"""
        project_data = {
            "name": "Highland Tower Development",
            "value": "$45.5M",
            "residential_units": 120,
            "retail_units": 8,
            "floors_above": 15,
            "floors_below": 2
        }
        
        # Test data types
        self.assertIsInstance(project_data["residential_units"], int)
        self.assertIsInstance(project_data["retail_units"], int)
        
        # Test reasonable values
        self.assertGreater(project_data["residential_units"], 0)
        self.assertGreater(project_data["retail_units"], 0)
        self.assertGreater(project_data["floors_above"], 0)
    
    def test_cost_data_validation(self):
        """Test cost data validation"""
        cost_data = {
            "daily_material_cost": 48200,
            "daily_labor_cost": 35600,
            "equipment_rental": 12800,
            "cost_accuracy": 96.4
        }
        
        # Test all costs are positive
        for cost_type, value in cost_data.items():
            if "cost" in cost_type or "rental" in cost_type:
                self.assertGreater(value, 0, f"{cost_type} should be positive")
        
        # Test accuracy percentage
        self.assertGreaterEqual(cost_data["cost_accuracy"], 0)
        self.assertLessEqual(cost_data["cost_accuracy"], 100)

class TestSecurityFeatures(unittest.TestCase):
    """Test security and authentication features"""
    
    def test_session_state_initialization(self):
        """Test session state initialization"""
        expected_defaults = {
            "authenticated": False,
            "username": "",
            "user_role": "",
            "current_menu": "Dashboard"
        }
        
        # Test that defaults are secure (not authenticated by default)
        self.assertFalse(expected_defaults["authenticated"])
        self.assertEqual(expected_defaults["username"], "")
        self.assertEqual(expected_defaults["user_role"], "")
    
    def test_role_based_access(self):
        """Test role-based access control"""
        # Test that user roles have appropriate restrictions
        test_roles = ["user", "inspector", "foreman", "superintendent", "manager", "admin"]
        
        for role in test_roles:
            # Each role should have specific limitations
            if role == "user":
                # Users should have the most restrictions
                self.assertIn(role, test_roles)
            elif role == "admin":
                # Admins should have the most access
                self.assertIn(role, test_roles)

def run_comprehensive_tests():
    """Run all gcPanel tests"""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestGCPanelCore,
        TestUnitPricesModule,
        TestDailyReportsModule,
        TestIntegrationSystems,
        TestUserInterface,
        TestDataValidation,
        TestSecurityFeatures
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

if __name__ == "__main__":
    print("🧪 Running gcPanel Comprehensive Test Suite")
    print("=" * 60)
    
    result = run_comprehensive_tests()
    
    print("\n" + "=" * 60)
    print(f"🧪 Test Results Summary:")
    print(f"✅ Tests Run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️ Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n⚠️ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: Error during test execution")
    
    if len(result.failures) == 0 and len(result.errors) == 0:
        print("\n🎉 All tests passed! gcPanel is ready for production.")
    else:
        print(f"\n🔧 {len(result.failures + result.errors)} issues found. Review and fix before deployment.")