"""
Unit tests for edge case scenarios in the Cloud Service Referee application.
"""
import pytest
from src.models import UserConstraints, ConstraintLevel
from src.service_repository import ServiceRepository
from src.scoring_system import ScoringSystem
from src.constraint_evaluator import ConstraintEvaluator
from src.trade_off_analyzer import TradeOffAnalyzer
from src.explanation_generator import ExplanationGenerator


class TestEdgeCaseScenarios:
    """Test specific edge case scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service_repo = ServiceRepository()
        self.scoring_system = ScoringSystem()
        self.constraint_evaluator = ConstraintEvaluator(self.scoring_system, self.service_repo)
        self.trade_off_analyzer = TradeOffAnalyzer()
        self.explanation_generator = ExplanationGenerator()
    
    def test_low_budget_high_scalability_edge_case(self):
        """
        Test low budget + high scalability explanation.
        Validates: Requirements 7.1
        """
        # Create constraints with low budget + high scalability tension
        constraints = UserConstraints(
            budget_sensitivity=ConstraintLevel.HIGH,  # High sensitivity = low budget tolerance
            expected_traffic=ConstraintLevel.MEDIUM,
            scalability_requirement=ConstraintLevel.HIGH,
            latency_sensitivity=ConstraintLevel.MEDIUM,
            operational_overhead_tolerance=ConstraintLevel.MEDIUM,
            time_to_market_urgency=ConstraintLevel.MEDIUM
        )
        
        # Get evaluations and analysis
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        trade_off_analysis = self.trade_off_analyzer.analyze_trade_offs(evaluations, constraints)
        
        # Verify edge case is detected
        assert len(trade_off_analysis.edge_case_warnings) > 0
        
        # Check for budget-scalability tension in warnings
        budget_scalability_warning_found = False
        for warning in trade_off_analysis.edge_case_warnings:
            if "budget" in warning.lower() and "scalability" in warning.lower():
                budget_scalability_warning_found = True
                # Verify required phrases are present
                assert "the trade-off here is" in warning.lower()
                assert ("this may be a limitation if" in warning.lower() or 
                       "this is a good choice when" in warning.lower())
                break
        
        assert budget_scalability_warning_found, "Budget-scalability tension not detected"
        
        # Verify conflict is identified
        assert "Budget sensitivity vs Scalability requirement" in trade_off_analysis.conflicting_constraints
    
    def test_high_latency_sensitivity_high_traffic_edge_case(self):
        """
        Test high latency sensitivity + high traffic explanation.
        Validates: Requirements 7.2
        """
        # Create constraints with high latency sensitivity + high traffic
        constraints = UserConstraints(
            budget_sensitivity=ConstraintLevel.MEDIUM,
            expected_traffic=ConstraintLevel.HIGH,
            scalability_requirement=ConstraintLevel.MEDIUM,
            latency_sensitivity=ConstraintLevel.HIGH,
            operational_overhead_tolerance=ConstraintLevel.MEDIUM,
            time_to_market_urgency=ConstraintLevel.MEDIUM
        )
        
        # Get evaluations and analysis
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        trade_off_analysis = self.trade_off_analyzer.analyze_trade_offs(evaluations, constraints)
        
        # Verify performance implications are identified
        assert len(trade_off_analysis.edge_case_warnings) > 0
        
        # Check for performance implications in warnings
        performance_warning_found = False
        for warning in trade_off_analysis.edge_case_warnings:
            if ("performance" in warning.lower() or "latency" in warning.lower()) and "traffic" in warning.lower():
                performance_warning_found = True
                # Verify required phrases are present
                assert ("this is a good choice when" in warning.lower() or 
                       "this may be a limitation if" in warning.lower())
                break
        
        assert performance_warning_found, "Performance implications not identified"
        
        # Verify Lambda gets low score for high latency sensitivity
        lambda_latency_score = evaluations["Lambda"].constraint_scores["latency_sensitivity"]
        assert lambda_latency_score <= 2, f"Lambda should score low on high latency sensitivity, got {lambda_latency_score}"
        
        # Verify EC2 gets high score for high latency sensitivity
        ec2_latency_score = evaluations["EC2"].constraint_scores["latency_sensitivity"]
        assert ec2_latency_score >= 4, f"EC2 should score high on high latency sensitivity, got {ec2_latency_score}"
    
    def test_fast_time_to_market_low_operational_tolerance_edge_case(self):
        """
        Test fast time-to-market + low operational tolerance explanation.
        Validates: Requirements 7.3
        """
        # Create constraints with fast time-to-market + low operational tolerance
        constraints = UserConstraints(
            budget_sensitivity=ConstraintLevel.MEDIUM,
            expected_traffic=ConstraintLevel.MEDIUM,
            scalability_requirement=ConstraintLevel.MEDIUM,
            latency_sensitivity=ConstraintLevel.MEDIUM,
            operational_overhead_tolerance=ConstraintLevel.LOW,
            time_to_market_urgency=ConstraintLevel.HIGH
        )
        
        # Get evaluations and analysis
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        trade_off_analysis = self.trade_off_analyzer.analyze_trade_offs(evaluations, constraints)
        
        # Verify speed-simplicity alignment is identified
        assert len(trade_off_analysis.edge_case_warnings) > 0
        
        # Check for speed-simplicity alignment in warnings
        alignment_warning_found = False
        for warning in trade_off_analysis.edge_case_warnings:
            if "time" in warning.lower() and "operational" in warning.lower():
                alignment_warning_found = True
                # Verify required phrases are present
                assert "this is a good choice when" in warning.lower()
                assert "serverless" in warning.lower()  # Should suggest serverless solutions
                break
        
        assert alignment_warning_found, "Speed-simplicity alignment not identified"
        
        # Verify Lambda gets high scores for both constraints
        lambda_time_score = evaluations["Lambda"].constraint_scores["time_to_market_urgency"]
        lambda_ops_score = evaluations["Lambda"].constraint_scores["operational_overhead_tolerance"]
        
        assert lambda_time_score >= 4, f"Lambda should score high on time-to-market, got {lambda_time_score}"
        assert lambda_ops_score >= 4, f"Lambda should score high on low operational tolerance, got {lambda_ops_score}"
        
        # Verify EC2 gets low score for low operational tolerance
        ec2_ops_score = evaluations["EC2"].constraint_scores["operational_overhead_tolerance"]
        assert ec2_ops_score <= 2, f"EC2 should score low on low operational tolerance, got {ec2_ops_score}"
    
    def test_multiple_conflicting_constraints(self):
        """Test scenario with multiple conflicting constraints."""
        # Create constraints with multiple conflicts
        constraints = UserConstraints(
            budget_sensitivity=ConstraintLevel.HIGH,      # Conflicts with latency and traffic
            expected_traffic=ConstraintLevel.HIGH,        # Conflicts with budget
            scalability_requirement=ConstraintLevel.HIGH, # Conflicts with budget
            latency_sensitivity=ConstraintLevel.HIGH,     # Conflicts with budget
            operational_overhead_tolerance=ConstraintLevel.LOW,  # Aligns with time-to-market
            time_to_market_urgency=ConstraintLevel.HIGH   # Conflicts with ops tolerance (but they align)
        )
        
        # Get evaluations and analysis
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        trade_off_analysis = self.trade_off_analyzer.analyze_trade_offs(evaluations, constraints)
        
        # Should identify multiple conflicts
        assert len(trade_off_analysis.conflicting_constraints) >= 2
        
        # Should identify multiple edge case warnings
        assert len(trade_off_analysis.edge_case_warnings) >= 2
        
        # Verify specific conflicts are identified
        expected_conflicts = [
            "Budget sensitivity vs Latency sensitivity",
            "Budget sensitivity vs Scalability requirement",
            "Expected traffic vs Budget sensitivity"
        ]
        
        conflicts_found = 0
        for expected_conflict in expected_conflicts:
            if expected_conflict in trade_off_analysis.conflicting_constraints:
                conflicts_found += 1
        
        assert conflicts_found >= 2, f"Expected at least 2 conflicts, found {conflicts_found}"
    
    def test_no_conflicts_scenario(self):
        """Test scenario with no conflicting constraints."""
        # Create constraints with no conflicts (all medium)
        constraints = UserConstraints(
            budget_sensitivity=ConstraintLevel.MEDIUM,
            expected_traffic=ConstraintLevel.MEDIUM,
            scalability_requirement=ConstraintLevel.MEDIUM,
            latency_sensitivity=ConstraintLevel.MEDIUM,
            operational_overhead_tolerance=ConstraintLevel.MEDIUM,
            time_to_market_urgency=ConstraintLevel.MEDIUM
        )
        
        # Get evaluations and analysis
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        trade_off_analysis = self.trade_off_analyzer.analyze_trade_offs(evaluations, constraints)
        
        # Should have minimal conflicts
        assert len(trade_off_analysis.conflicting_constraints) == 0
        
        # Should still have trade-off analysis
        assert len(trade_off_analysis.cost_vs_control) > 0
        assert len(trade_off_analysis.latency_vs_ops_complexity) > 0
        
        # All services should have reasonable scores
        for service, evaluation in evaluations.items():
            scores = evaluation.constraint_scores.values()
            avg_score = sum(scores) / len(scores)
            assert 1.5 <= avg_score <= 4.5, f"{service} average score {avg_score} outside reasonable range"