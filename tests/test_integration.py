"""
Integration tests for the Cloud Service Referee application.
"""
import pytest
from src.models import UserConstraints, ConstraintLevel
from src.service_repository import ServiceRepository
from src.scoring_system import ScoringSystem
from src.constraint_evaluator import ConstraintEvaluator
from src.trade_off_analyzer import TradeOffAnalyzer
from src.explanation_generator import ExplanationGenerator
from src.comparison_engine import ComparisonEngine
from src.ui_controller import UIController


class TestIntegration:
    """Test complete integration workflows."""
    
    def setup_method(self):
        """Set up integration test fixtures."""
        # Initialize all components
        self.service_repo = ServiceRepository()
        self.scoring_system = ScoringSystem()
        self.constraint_evaluator = ConstraintEvaluator(self.scoring_system, self.service_repo)
        self.trade_off_analyzer = TradeOffAnalyzer()
        self.explanation_generator = ExplanationGenerator()
        
        self.comparison_engine = ComparisonEngine(
            constraint_evaluator=self.constraint_evaluator,
            trade_off_analyzer=self.trade_off_analyzer,
            explanation_generator=self.explanation_generator
        )
        
        self.ui_controller = UIController()
    
    def test_complete_user_workflow(self):
        """
        Test complete user workflow from input to results.
        Validates: All requirements integrated
        """
        # Step 1: User provides constraint inputs
        constraint_inputs = {
            "budget_sensitivity": "High",
            "expected_traffic": "Low", 
            "scalability_requirement": "Medium",
            "latency_sensitivity": "High",
            "operational_overhead_tolerance": "Low",
            "time_to_market_urgency": "High"
        }
        
        # Step 2: UI validates inputs
        assert self.ui_controller.validate_constraint_inputs(constraint_inputs)
        
        # Step 3: Convert to UserConstraints
        user_constraints = self.ui_controller.create_user_constraints_from_input(constraint_inputs)
        
        # Step 4: Perform comparison
        comparison_result = self.comparison_engine.compare_services(user_constraints)
        
        # Step 5: Validate complete results
        # Should have evaluations for all services
        assert len(comparison_result.evaluations) == 3
        expected_services = {"EC2", "Lambda", "ECS_Fargate"}
        assert set(comparison_result.evaluations.keys()) == expected_services
        
        # Should have recommendations for all services
        assert len(comparison_result.contextual_recommendations) == 3
        assert set(comparison_result.contextual_recommendations.keys()) == expected_services
        
        # Should have trade-off analysis
        assert comparison_result.trade_off_analysis is not None
        assert len(comparison_result.trade_off_analysis.cost_vs_control) > 0
        assert len(comparison_result.trade_off_analysis.latency_vs_ops_complexity) > 0
        
        # Should detect edge cases for this constraint combination
        assert len(comparison_result.edge_case_warnings) > 0
        
        # Step 6: Validate service evaluations
        for service, evaluation in comparison_result.evaluations.items():
            # Each service should have complete evaluation
            assert len(evaluation.constraint_scores) == 6
            assert len(evaluation.strengths) > 0
            assert len(evaluation.limitations) > 0
            assert len(evaluation.best_use_cases) > 0
            
            # All scores should be valid
            for score in evaluation.constraint_scores.values():
                assert 1 <= score <= 5
        
        # Step 7: Validate recommendations contain required phrases
        for service, recommendation in comparison_result.contextual_recommendations.items():
            assert self.explanation_generator.validate_required_phrases(recommendation)
    
    def test_error_handling_and_recovery(self):
        """Test error handling and recovery mechanisms."""
        # Test invalid constraint inputs
        invalid_inputs = {
            "budget_sensitivity": "Invalid",
            "expected_traffic": "Low",
            "scalability_requirement": "Medium",
            "latency_sensitivity": "High",
            "operational_overhead_tolerance": "Low",
            "time_to_market_urgency": "High"
        }
        
        # Should reject invalid inputs
        assert not self.ui_controller.validate_constraint_inputs(invalid_inputs)
        
        # Test missing constraint inputs
        incomplete_inputs = {
            "budget_sensitivity": "High",
            "expected_traffic": "Low"
            # Missing other constraints
        }
        
        # Should reject incomplete inputs
        assert not self.ui_controller.validate_constraint_inputs(incomplete_inputs)
        
        # Test that valid inputs still work after errors
        valid_inputs = {
            "budget_sensitivity": "Medium",
            "expected_traffic": "Medium",
            "scalability_requirement": "Medium",
            "latency_sensitivity": "Medium",
            "operational_overhead_tolerance": "Medium",
            "time_to_market_urgency": "Medium"
        }
        
        assert self.ui_controller.validate_constraint_inputs(valid_inputs)
        user_constraints = self.ui_controller.create_user_constraints_from_input(valid_inputs)
        result = self.comparison_engine.compare_services(user_constraints)
        
        # Should still produce valid results
        assert len(result.evaluations) == 3
        assert len(result.contextual_recommendations) == 3
    
    def test_all_constraint_combinations_handled(self):
        """Test that all constraint combinations are handled correctly."""
        constraint_values = [ConstraintLevel.LOW, ConstraintLevel.MEDIUM, ConstraintLevel.HIGH]
        
        # Test a representative sample of combinations
        test_combinations = [
            # All low
            (ConstraintLevel.LOW, ConstraintLevel.LOW, ConstraintLevel.LOW, 
             ConstraintLevel.LOW, ConstraintLevel.LOW, ConstraintLevel.LOW),
            # All high
            (ConstraintLevel.HIGH, ConstraintLevel.HIGH, ConstraintLevel.HIGH,
             ConstraintLevel.HIGH, ConstraintLevel.HIGH, ConstraintLevel.HIGH),
            # Mixed combination 1
            (ConstraintLevel.HIGH, ConstraintLevel.LOW, ConstraintLevel.MEDIUM,
             ConstraintLevel.HIGH, ConstraintLevel.LOW, ConstraintLevel.HIGH),
            # Mixed combination 2
            (ConstraintLevel.LOW, ConstraintLevel.HIGH, ConstraintLevel.HIGH,
             ConstraintLevel.LOW, ConstraintLevel.HIGH, ConstraintLevel.MEDIUM),
            # All medium
            (ConstraintLevel.MEDIUM, ConstraintLevel.MEDIUM, ConstraintLevel.MEDIUM,
             ConstraintLevel.MEDIUM, ConstraintLevel.MEDIUM, ConstraintLevel.MEDIUM)
        ]
        
        for combination in test_combinations:
            user_constraints = UserConstraints(
                budget_sensitivity=combination[0],
                expected_traffic=combination[1],
                scalability_requirement=combination[2],
                latency_sensitivity=combination[3],
                operational_overhead_tolerance=combination[4],
                time_to_market_urgency=combination[5]
            )
            
            # Should handle all combinations without errors
            result = self.comparison_engine.compare_services(user_constraints)
            
            # Validate results are complete
            assert len(result.evaluations) == 3
            assert len(result.contextual_recommendations) == 3
            assert result.trade_off_analysis is not None
            
            # Validate all services have complete evaluations
            for service, evaluation in result.evaluations.items():
                assert len(evaluation.constraint_scores) == 6
                for score in evaluation.constraint_scores.values():
                    assert 1 <= score <= 5
    
    def test_component_interactions(self):
        """Test that all components work together correctly."""
        # Create test constraints
        constraints = UserConstraints(
            budget_sensitivity=ConstraintLevel.HIGH,
            expected_traffic=ConstraintLevel.MEDIUM,
            scalability_requirement=ConstraintLevel.HIGH,
            latency_sensitivity=ConstraintLevel.MEDIUM,
            operational_overhead_tolerance=ConstraintLevel.LOW,
            time_to_market_urgency=ConstraintLevel.HIGH
        )
        
        # Test individual component interactions
        
        # 1. Service Repository -> Scoring System
        services = self.service_repo.get_all_services()
        for service in services:
            scores = self.scoring_system.get_all_scores(service, constraints)
            assert len(scores) == 6
            assert all(1 <= score <= 5 for score in scores.values())
        
        # 2. Scoring System -> Constraint Evaluator
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        assert len(evaluations) == 3
        
        # 3. Constraint Evaluator -> Trade-off Analyzer
        trade_off_analysis = self.trade_off_analyzer.analyze_trade_offs(evaluations, constraints)
        assert trade_off_analysis is not None
        
        # 4. Constraint Evaluator -> Explanation Generator
        recommendations = self.explanation_generator.generate_contextual_recommendations(
            evaluations, constraints
        )
        assert len(recommendations) == 3
        
        # 5. All components -> Comparison Engine
        final_result = self.comparison_engine.compare_services(constraints)
        assert final_result.evaluations == evaluations
        assert final_result.contextual_recommendations == recommendations
        assert final_result.trade_off_analysis == trade_off_analysis
    
    def test_neutrality_maintained_throughout_workflow(self):
        """Test that neutrality is maintained throughout the entire workflow."""
        # Test multiple constraint combinations
        test_scenarios = [
            UserConstraints(
                budget_sensitivity=ConstraintLevel.HIGH,
                expected_traffic=ConstraintLevel.LOW,
                scalability_requirement=ConstraintLevel.LOW,
                latency_sensitivity=ConstraintLevel.LOW,
                operational_overhead_tolerance=ConstraintLevel.HIGH,
                time_to_market_urgency=ConstraintLevel.LOW
            ),
            UserConstraints(
                budget_sensitivity=ConstraintLevel.LOW,
                expected_traffic=ConstraintLevel.HIGH,
                scalability_requirement=ConstraintLevel.HIGH,
                latency_sensitivity=ConstraintLevel.HIGH,
                operational_overhead_tolerance=ConstraintLevel.LOW,
                time_to_market_urgency=ConstraintLevel.HIGH
            )
        ]
        
        for constraints in test_scenarios:
            result = self.comparison_engine.compare_services(constraints)
            
            # Verify no winner is declared
            assert self.constraint_evaluator.validate_no_winner_declaration(result.evaluations)
            
            # Verify recommendations don't contain winner language
            winner_words = ['best', 'winner', 'optimal', 'perfect']
            for service, recommendation in result.contextual_recommendations.items():
                recommendation_lower = recommendation.lower()
                for word in winner_words:
                    assert word not in recommendation_lower, \
                        f"Winner word '{word}' found in {service} recommendation"
            
            # Verify all services are represented equally
            assert len(result.evaluations) == 3
            assert len(result.contextual_recommendations) == 3
    
    def test_end_to_end_data_flow(self):
        """Test complete data flow from UI input to final output."""
        # Start with UI input format
        ui_input = {
            "budget_sensitivity": "High",
            "expected_traffic": "Medium",
            "scalability_requirement": "High", 
            "latency_sensitivity": "Low",
            "operational_overhead_tolerance": "Medium",
            "time_to_market_urgency": "Medium"
        }
        
        # UI processing
        assert self.ui_controller.validate_constraint_inputs(ui_input)
        user_constraints = self.ui_controller.create_user_constraints_from_input(ui_input)
        
        # Core processing
        comparison_result = self.comparison_engine.compare_services(user_constraints)
        
        # Verify data integrity throughout the flow
        
        # 1. Constraint values preserved
        assert user_constraints.budget_sensitivity == ConstraintLevel.HIGH
        assert user_constraints.expected_traffic == ConstraintLevel.MEDIUM
        assert user_constraints.scalability_requirement == ConstraintLevel.HIGH
        
        # 2. Service evaluations complete
        for service, evaluation in comparison_result.evaluations.items():
            # Scores should reflect input constraints
            budget_score = evaluation.constraint_scores["budget_sensitivity"]
            traffic_score = evaluation.constraint_scores["expected_traffic"]
            scalability_score = evaluation.constraint_scores["scalability_requirement"]
            
            # Verify scores are reasonable for the constraints
            assert 1 <= budget_score <= 5
            assert 1 <= traffic_score <= 5
            assert 1 <= scalability_score <= 5
        
        # 3. Trade-off analysis addresses the specific constraints
        trade_off_text = comparison_result.trade_off_analysis.cost_vs_control.lower()
        assert "budget" in trade_off_text or "cost" in trade_off_text
        
        # 4. Recommendations are contextual to the constraints
        for service, recommendation in comparison_result.contextual_recommendations.items():
            # Should contain required phrases
            assert self.explanation_generator.validate_required_phrases(recommendation)
            
            # Should be substantial content
            assert len(recommendation) > 100