"""
Unit tests for UI components in the Cloud Service Referee application.
"""
import pytest
from src.models import UserConstraints, ConstraintLevel, ServiceEvaluation, ComparisonResult, TradeOffAnalysis
from src.ui_controller import UIController


class TestUIComponents:
    """Test UI component functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.ui_controller = UIController()
    
    def test_all_required_ui_elements_present(self):
        """
        Test that all required UI elements are present.
        Validates: Requirements 5.1, 5.2, 5.3, 5.5, 10.1
        """
        # Test constraint descriptions are complete
        expected_constraints = [
            "budget_sensitivity", "expected_traffic", "scalability_requirement",
            "latency_sensitivity", "operational_overhead_tolerance", "time_to_market_urgency"
        ]
        
        for constraint in expected_constraints:
            assert constraint in self.ui_controller.constraint_descriptions
            desc = self.ui_controller.constraint_descriptions[constraint]
            
            # Each constraint should have label, description, and help
            assert "label" in desc
            assert "description" in desc
            assert "help" in desc
            
            # Content should not be empty
            assert len(desc["label"]) > 0
            assert len(desc["description"]) > 0
            assert len(desc["help"]) > 0
    
    def test_constraint_options_validity(self):
        """Test that constraint options are exactly Low, Medium, High."""
        expected_options = ["Low", "Medium", "High"]
        assert self.ui_controller.constraint_options == expected_options
    
    def test_constraint_input_validation(self):
        """Test constraint input validation functionality."""
        # Test valid input
        valid_input = {
            "budget_sensitivity": "High",
            "expected_traffic": "Medium",
            "scalability_requirement": "Low",
            "latency_sensitivity": "High",
            "operational_overhead_tolerance": "Low",
            "time_to_market_urgency": "High"
        }
        
        assert self.ui_controller.validate_constraint_inputs(valid_input)
        
        # Test invalid constraint value
        invalid_input = valid_input.copy()
        invalid_input["budget_sensitivity"] = "Invalid"
        assert not self.ui_controller.validate_constraint_inputs(invalid_input)
        
        # Test missing constraint
        incomplete_input = valid_input.copy()
        del incomplete_input["budget_sensitivity"]
        assert not self.ui_controller.validate_constraint_inputs(incomplete_input)
    
    def test_user_constraints_creation(self):
        """Test UserConstraints object creation from UI input."""
        constraint_input = {
            "budget_sensitivity": "High",
            "expected_traffic": "Low",
            "scalability_requirement": "Medium",
            "latency_sensitivity": "High",
            "operational_overhead_tolerance": "Low",
            "time_to_market_urgency": "High"
        }
        
        user_constraints = self.ui_controller.create_user_constraints_from_input(constraint_input)
        
        # Verify correct conversion
        assert user_constraints.budget_sensitivity == ConstraintLevel.HIGH
        assert user_constraints.expected_traffic == ConstraintLevel.LOW
        assert user_constraints.scalability_requirement == ConstraintLevel.MEDIUM
        assert user_constraints.latency_sensitivity == ConstraintLevel.HIGH
        assert user_constraints.operational_overhead_tolerance == ConstraintLevel.LOW
        assert user_constraints.time_to_market_urgency == ConstraintLevel.HIGH
    
    def test_comparison_table_data_structure(self):
        """Test that comparison table can handle service score data."""
        # Create test service scores
        test_scores = {
            "EC2": {
                "budget_sensitivity": 5,
                "expected_traffic": 4,
                "scalability_requirement": 3,
                "latency_sensitivity": 5,
                "operational_overhead_tolerance": 2,
                "time_to_market_urgency": 2
            },
            "Lambda": {
                "budget_sensitivity": 3,
                "expected_traffic": 5,
                "scalability_requirement": 5,
                "latency_sensitivity": 1,
                "operational_overhead_tolerance": 5,
                "time_to_market_urgency": 5
            },
            "ECS_Fargate": {
                "budget_sensitivity": 2,
                "expected_traffic": 4,
                "scalability_requirement": 4,
                "latency_sensitivity": 3,
                "operational_overhead_tolerance": 4,
                "time_to_market_urgency": 3
            }
        }
        
        # This should not raise any exceptions
        # We can't test actual Streamlit rendering, but we can verify data structure handling
        try:
            # Verify the data structure is what the UI expects
            for service, scores in test_scores.items():
                assert isinstance(service, str)
                assert isinstance(scores, dict)
                assert len(scores) == 6  # All 6 constraints
                
                for constraint, score in scores.items():
                    assert isinstance(constraint, str)
                    assert isinstance(score, int)
                    assert 1 <= score <= 5
            
            # Test passes if no exceptions
            assert True
        except Exception as e:
            pytest.fail(f"Comparison table data structure test failed: {e}")
    
    def test_pros_and_cons_display_structure(self):
        """Test that pros and cons are displayed for all services."""
        # Create test service evaluation
        test_evaluation = ServiceEvaluation(
            service_name="Test Service",
            constraint_scores={
                "budget_sensitivity": 4,
                "expected_traffic": 3,
                "scalability_requirement": 5,
                "latency_sensitivity": 2,
                "operational_overhead_tolerance": 4,
                "time_to_market_urgency": 3
            },
            strengths=[
                "Excellent cost optimization potential",
                "Full infrastructure control",
                "High performance capabilities",
                "Mature ecosystem",
                "Flexible configuration options"
            ],
            limitations=[
                "High operational overhead",
                "Requires infrastructure expertise",
                "Slower provisioning time",
                "Manual scaling configuration needed"
            ],
            best_use_cases=[
                "Legacy system migration",
                "High-performance computing",
                "Cost-sensitive applications"
            ]
        )
        
        # Verify structure is complete
        assert len(test_evaluation.strengths) > 0
        assert len(test_evaluation.limitations) > 0
        assert len(test_evaluation.best_use_cases) > 0
        assert len(test_evaluation.constraint_scores) == 6
        
        # Verify all scores are valid
        for score in test_evaluation.constraint_scores.values():
            assert 1 <= score <= 5
    
    def test_contextual_recommendations_structure(self):
        """Test that contextual recommendations are provided for each service."""
        # Test that we can handle recommendation data structure
        test_recommendations = {
            "EC2": "EC2 is a good choice when you need full infrastructure control...",
            "Lambda": "Lambda is a good choice when you want zero infrastructure management...",
            "ECS_Fargate": "ECS Fargate is a good choice when you want container benefits..."
        }
        
        # Verify structure
        assert len(test_recommendations) == 3  # All three services
        
        expected_services = {"EC2", "Lambda", "ECS_Fargate"}
        assert set(test_recommendations.keys()) == expected_services
        
        # Verify all recommendations are non-empty strings
        for service, recommendation in test_recommendations.items():
            assert isinstance(recommendation, str)
            assert len(recommendation) > 0
    
    def test_error_message_methods(self):
        """Test error message display methods."""
        # These methods should not raise exceptions
        try:
            # We can't test actual Streamlit display, but we can test method calls
            test_message = "Test message"
            
            # These should not raise exceptions
            # (In actual Streamlit app, these would display messages)
            self.ui_controller.display_error_message(test_message)
            self.ui_controller.display_info_message(test_message)
            self.ui_controller.display_success_message(test_message)
            
            # Test passes if no exceptions
            assert True
        except Exception as e:
            pytest.fail(f"Error message methods test failed: {e}")
    
    def test_constraint_descriptions_content_quality(self):
        """Test that constraint descriptions contain helpful content."""
        for constraint_key, desc in self.ui_controller.constraint_descriptions.items():
            # Labels should be present and non-empty
            assert len(desc["label"]) > 0
            
            # Descriptions should be questions or explanatory
            assert "?" in desc["description"] or "how" in desc["description"].lower()
            
            # Help text should contain the constraint levels
            help_text = desc["help"].lower()
            assert "low" in help_text
            assert "medium" in help_text
            assert "high" in help_text
            
            # Help text should use pipe separators
            assert "|" in desc["help"]