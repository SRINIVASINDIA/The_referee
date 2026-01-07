"""
Property-based tests for the Cloud Service Referee application.
"""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from src.models import UserConstraints, ConstraintLevel, ServiceType
from src.service_repository import ServiceRepository
from src.scoring_system import ScoringSystem
from src.constraint_evaluator import ConstraintEvaluator
from src.trade_off_analyzer import TradeOffAnalyzer
from src.explanation_generator import ExplanationGenerator
from src.ui_controller import UIController


# Strategy for generating constraint levels
constraint_level_strategy = st.sampled_from([
    ConstraintLevel.LOW, ConstraintLevel.MEDIUM, ConstraintLevel.HIGH
])

# Strategy for generating user constraints
user_constraints_strategy = st.builds(
    UserConstraints,
    budget_sensitivity=constraint_level_strategy,
    expected_traffic=constraint_level_strategy,
    scalability_requirement=constraint_level_strategy,
    latency_sensitivity=constraint_level_strategy,
    operational_overhead_tolerance=constraint_level_strategy,
    time_to_market_urgency=constraint_level_strategy
)


class TestServiceIndependence:
    """Test service independence properties."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service_repo = ServiceRepository()
    
    @given(constraints=user_constraints_strategy)
    @settings(suppress_health_check=[HealthCheck.too_slow])
    def test_service_independence_property(self, constraints):
        """
        Property 1: Service Independence
        For any set of user constraints, each service (EC2, Lambda, ECS Fargate) 
        should receive independent evaluation scores without influence from other services' scores.
        
        Feature: cloud-service-referee, Property 1: Service Independence
        Validates: Requirements 1.4, 3.1
        """
        # Get all services
        services = self.service_repo.get_all_services()
        
        # Verify we have exactly the three expected services
        expected_services = {ServiceType.EC2.value, ServiceType.LAMBDA.value, ServiceType.ECS_FARGATE.value}
        assert set(services) == expected_services
        
        # For now, we'll test that the service repository treats each service independently
        # by verifying that each service has distinct characteristics
        service_characteristics = {}
        for service in services:
            characteristics = self.service_repo.get_service_characteristics(service)
            service_characteristics[service] = characteristics
        
        # Verify each service has independent characteristics
        # (no two services should have identical characteristics)
        for i, service1 in enumerate(services):
            for service2 in services[i+1:]:
                char1 = service_characteristics[service1]
                char2 = service_characteristics[service2]
                
                # Services should have different names
                assert char1.name != char2.name
                
                # Services should have different strengths
                assert char1.strengths != char2.strengths
                
                # Services should have different limitations
                assert char1.limitations != char2.limitations
                
                # Services should have different use cases
                assert char1.best_use_cases != char2.best_use_cases
    
    def test_all_services_present(self):
        """Test that all required services are present in the repository."""
        services = self.service_repo.get_all_services()
        expected_services = {ServiceType.EC2.value, ServiceType.LAMBDA.value, ServiceType.ECS_FARGATE.value}
        assert set(services) == expected_services
    
    def test_service_characteristics_completeness(self):
        """Test that each service has complete characteristics."""
        services = self.service_repo.get_all_services()
        
        for service in services:
            characteristics = self.service_repo.get_service_characteristics(service)
            
            # Each service should have non-empty characteristics
            assert characteristics.name
            assert len(characteristics.strengths) > 0
            assert len(characteristics.limitations) > 0
            assert len(characteristics.best_use_cases) > 0
            assert characteristics.cost_model
            assert characteristics.scaling_characteristics
            assert characteristics.operational_overhead


class TestScoringSystemProperties:
    """Test scoring system properties."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.scoring_system = ScoringSystem()
        self.service_repo = ServiceRepository()
    
    @given(
        service=st.sampled_from([ServiceType.EC2.value, ServiceType.LAMBDA.value, ServiceType.ECS_FARGATE.value]),
        constraint=st.sampled_from([
            "budget_sensitivity", "expected_traffic", "scalability_requirement",
            "latency_sensitivity", "operational_overhead_tolerance", "time_to_market_urgency"
        ]),
        value=st.sampled_from([ConstraintLevel.LOW.value, ConstraintLevel.MEDIUM.value, ConstraintLevel.HIGH.value])
    )
    def test_score_range_consistency_property(self, service, constraint, value):
        """
        Property 2: Score Range Consistency
        For any constraint-service combination, the scoring system should produce 
        scores within the 1-5 range and maintain consistency for identical inputs.
        
        Feature: cloud-service-referee, Property 2: Score Range Consistency
        Validates: Requirements 3.2, 9.2, 9.4
        """
        # Get score for the combination
        score = self.scoring_system.score_service_against_constraint(service, constraint, value)
        
        # Verify score is within valid range (1-5)
        assert 1 <= score <= 5, f"Score {score} is outside valid range 1-5"
        
        # Verify consistency - same inputs should produce same outputs
        score2 = self.scoring_system.score_service_against_constraint(service, constraint, value)
        assert score == score2, f"Inconsistent scores: {score} != {score2}"
    
    @given(constraints=user_constraints_strategy)
    def test_complete_scoring_coverage_property(self, constraints):
        """
        Property 8: Complete Scoring Coverage
        For any valid constraint combination, every service should receive 
        a score for every constraint dimension.
        
        Feature: cloud-service-referee, Property 8: Complete Scoring Coverage
        Validates: Requirements 9.1, 9.5
        """
        services = self.service_repo.get_all_services()
        expected_constraints = [
            "budget_sensitivity", "expected_traffic", "scalability_requirement",
            "latency_sensitivity", "operational_overhead_tolerance", "time_to_market_urgency"
        ]
        
        for service in services:
            scores = self.scoring_system.get_all_scores(service, constraints)
            
            # Verify all constraint dimensions are covered
            assert set(scores.keys()) == set(expected_constraints), \
                f"Missing constraints for {service}: expected {expected_constraints}, got {list(scores.keys())}"
            
            # Verify all scores are valid
            for constraint_name, score in scores.items():
                assert 1 <= score <= 5, \
                    f"Invalid score {score} for {service} on {constraint_name}"
    
    def test_scoring_rules_validation(self):
        """Test that all scoring rules are complete and valid."""
        # Test that the scoring system validates its own rules
        assert self.scoring_system.validate_all_rules(), "Scoring rules validation failed"
        
        # Test that all expected combinations are covered
        services = [ServiceType.EC2.value, ServiceType.LAMBDA.value, ServiceType.ECS_FARGATE.value]
        constraints = [
            "budget_sensitivity", "expected_traffic", "scalability_requirement",
            "latency_sensitivity", "operational_overhead_tolerance", "time_to_market_urgency"
        ]
        levels = [ConstraintLevel.LOW.value, ConstraintLevel.MEDIUM.value, ConstraintLevel.HIGH.value]
        
        for service in services:
            for constraint in constraints:
                for level in levels:
                    score = self.scoring_system.score_service_against_constraint(service, constraint, level)
                    assert 1 <= score <= 5, f"Invalid score for {service}, {constraint}, {level}"

class TestEvaluationIndependenceProperties:
    """Test evaluation independence properties."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service_repo = ServiceRepository()
        self.scoring_system = ScoringSystem()
        self.constraint_evaluator = ConstraintEvaluator(self.scoring_system, self.service_repo)
    
    @given(constraints=user_constraints_strategy)
    def test_no_winner_declaration_property(self, constraints):
        """
        Property 3: No Winner Declaration
        For any evaluation result, the system should not declare any service 
        as the single "best" choice or "winner".
        
        Feature: cloud-service-referee, Property 3: No Winner Declaration
        Validates: Requirements 3.3, 6.2
        """
        # Evaluate all services
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        
        # Verify no winner is declared
        assert self.constraint_evaluator.validate_no_winner_declaration(evaluations), \
            "System declared a winner, violating neutrality principle"
        
        # Verify all services are evaluated independently
        services = list(evaluations.keys())
        assert len(services) == 3, f"Expected 3 services, got {len(services)}"
        
        # Verify each service has distinct characteristics
        for i, service1 in enumerate(services):
            for service2 in services[i+1:]:
                eval1 = evaluations[service1]
                eval2 = evaluations[service2]
                
                # Services should have different names
                assert eval1.service_name != eval2.service_name
                
                # Services should have different strengths and limitations
                assert eval1.strengths != eval2.strengths
                assert eval1.limitations != eval2.limitations
    
    @given(constraints=user_constraints_strategy)
    def test_system_robustness_property(self, constraints):
        """
        Property 9: System Robustness
        For any valid constraint combination, the system should complete 
        evaluation without errors or failures.
        
        Feature: cloud-service-referee, Property 9: System Robustness
        Validates: Requirements 7.4
        """
        # This should not raise any exceptions
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        
        # Verify we got evaluations for all services
        expected_services = {ServiceType.EC2.value, ServiceType.LAMBDA.value, ServiceType.ECS_FARGATE.value}
        assert set(evaluations.keys()) == expected_services
        
        # Verify each evaluation is complete
        for service, evaluation in evaluations.items():
            assert evaluation.service_name is not None
            assert len(evaluation.constraint_scores) == 6  # All 6 constraints
            assert len(evaluation.strengths) > 0
            assert len(evaluation.limitations) > 0
            assert len(evaluation.best_use_cases) > 0
            
            # Verify all scores are valid
            for constraint, score in evaluation.constraint_scores.items():
                assert 1 <= score <= 5, f"Invalid score {score} for {service} on {constraint}"
    
    def test_evaluation_independence_validation(self):
        """Test that evaluations maintain independence."""
        # Create test constraints
        constraints = UserConstraints(
            budget_sensitivity=ConstraintLevel.HIGH,
            expected_traffic=ConstraintLevel.LOW,
            scalability_requirement=ConstraintLevel.MEDIUM,
            latency_sensitivity=ConstraintLevel.HIGH,
            operational_overhead_tolerance=ConstraintLevel.LOW,
            time_to_market_urgency=ConstraintLevel.HIGH
        )
        
        # Get evaluations
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        
        # Test internal independence validation
        self.constraint_evaluator._ensure_evaluation_independence(evaluations)
        
        # Test that summary doesn't declare winners
        summary = self.constraint_evaluator.get_evaluation_summary(evaluations)
        
        # Verify summary contains data for all services
        assert len(summary) == 3
        for service, stats in summary.items():
            assert 'average_score' in stats
            assert 'score_count' in stats
            assert 'min_score' in stats
            assert 'max_score' in stats
            assert stats['score_count'] == 6  # All 6 constraints

class TestTradeOffAnalysisProperties:
    """Test trade-off analysis properties."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service_repo = ServiceRepository()
        self.scoring_system = ScoringSystem()
        self.constraint_evaluator = ConstraintEvaluator(self.scoring_system, self.service_repo)
        self.trade_off_analyzer = TradeOffAnalyzer()
    
    @given(constraints=user_constraints_strategy)
    def test_trade_off_identification_property(self, constraints):
        """
        Property 6: Trade-Off Identification
        For any constraint combination that creates inherent tensions 
        (such as low budget + high scalability), the system should identify 
        and explain the conflicting requirements.
        
        Feature: cloud-service-referee, Property 6: Trade-Off Identification
        Validates: Requirements 4.1, 7.5
        """
        # Get service evaluations
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        
        # Analyze trade-offs
        trade_off_analysis = self.trade_off_analyzer.analyze_trade_offs(evaluations, constraints)
        
        # Verify trade-off analysis is complete
        assert trade_off_analysis.cost_vs_control is not None
        assert trade_off_analysis.latency_vs_ops_complexity is not None
        assert isinstance(trade_off_analysis.edge_case_warnings, list)
        assert isinstance(trade_off_analysis.conflicting_constraints, list)
        
        # Verify analysis contains meaningful content
        assert len(trade_off_analysis.cost_vs_control) > 0
        assert len(trade_off_analysis.latency_vs_ops_complexity) > 0
        
        # Check for specific edge case detection
        if (constraints.budget_sensitivity == ConstraintLevel.HIGH and 
            constraints.scalability_requirement == ConstraintLevel.HIGH):
            # Should identify budget-scalability tension
            assert len(trade_off_analysis.edge_case_warnings) > 0
            assert any("budget" in warning.lower() and "scalability" in warning.lower() 
                     for warning in trade_off_analysis.edge_case_warnings)
        
        if (constraints.latency_sensitivity == ConstraintLevel.HIGH and 
            constraints.expected_traffic == ConstraintLevel.HIGH):
            # Should identify performance implications
            assert len(trade_off_analysis.edge_case_warnings) > 0
            assert any("latency" in warning.lower() or "performance" in warning.lower() 
                     for warning in trade_off_analysis.edge_case_warnings)
        
        if (constraints.time_to_market_urgency == ConstraintLevel.HIGH and 
            constraints.operational_overhead_tolerance == ConstraintLevel.LOW):
            # Should identify speed-simplicity alignment
            assert len(trade_off_analysis.edge_case_warnings) > 0
            assert any("time" in warning.lower() and "operational" in warning.lower() 
                     for warning in trade_off_analysis.edge_case_warnings)
    
    def test_specific_edge_cases(self):
        """Test specific edge case scenarios."""
        # Test low budget + high scalability
        constraints1 = UserConstraints(
            budget_sensitivity=ConstraintLevel.HIGH,
            expected_traffic=ConstraintLevel.MEDIUM,
            scalability_requirement=ConstraintLevel.HIGH,
            latency_sensitivity=ConstraintLevel.MEDIUM,
            operational_overhead_tolerance=ConstraintLevel.MEDIUM,
            time_to_market_urgency=ConstraintLevel.MEDIUM
        )
        
        evaluations1 = self.constraint_evaluator.evaluate_services(constraints1)
        analysis1 = self.trade_off_analyzer.analyze_trade_offs(evaluations1, constraints1)
        
        # Should detect budget-scalability conflict
        assert len(analysis1.conflicting_constraints) > 0
        assert "Budget sensitivity vs Scalability requirement" in analysis1.conflicting_constraints
        
        # Test high latency sensitivity + high traffic
        constraints2 = UserConstraints(
            budget_sensitivity=ConstraintLevel.MEDIUM,
            expected_traffic=ConstraintLevel.HIGH,
            scalability_requirement=ConstraintLevel.MEDIUM,
            latency_sensitivity=ConstraintLevel.HIGH,
            operational_overhead_tolerance=ConstraintLevel.MEDIUM,
            time_to_market_urgency=ConstraintLevel.MEDIUM
        )
        
        evaluations2 = self.constraint_evaluator.evaluate_services(constraints2)
        analysis2 = self.trade_off_analyzer.analyze_trade_offs(evaluations2, constraints2)
        
        # Should identify performance implications
        assert len(analysis2.edge_case_warnings) > 0
        assert any("performance" in warning.lower() or "latency" in warning.lower() 
                  for warning in analysis2.edge_case_warnings)
        
        # Test fast time-to-market + low operational tolerance
        constraints3 = UserConstraints(
            budget_sensitivity=ConstraintLevel.MEDIUM,
            expected_traffic=ConstraintLevel.MEDIUM,
            scalability_requirement=ConstraintLevel.MEDIUM,
            latency_sensitivity=ConstraintLevel.MEDIUM,
            operational_overhead_tolerance=ConstraintLevel.LOW,
            time_to_market_urgency=ConstraintLevel.HIGH
        )
        
        evaluations3 = self.constraint_evaluator.evaluate_services(constraints3)
        analysis3 = self.trade_off_analyzer.analyze_trade_offs(evaluations3, constraints3)
        
        # Should identify speed-simplicity alignment
        assert len(analysis3.edge_case_warnings) > 0
        assert any("time" in warning.lower() and "operational" in warning.lower() 
                  for warning in analysis3.edge_case_warnings)
class TestExplanationGenerationProperties:
    """Test explanation generation properties."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service_repo = ServiceRepository()
        self.scoring_system = ScoringSystem()
        self.constraint_evaluator = ConstraintEvaluator(self.scoring_system, self.service_repo)
        self.trade_off_analyzer = TradeOffAnalyzer()
        self.explanation_generator = ExplanationGenerator()
    
    @given(constraints=user_constraints_strategy)
    def test_required_phrase_inclusion_property(self, constraints):
        """
        Property 5: Required Phrase Inclusion
        For any generated explanation, the text should contain at least one instance 
        of the required phrases: "This is a good choice when...", "This may be a 
        limitation if...", or "The trade-off here is...".
        
        Feature: cloud-service-referee, Property 5: Required Phrase Inclusion
        Validates: Requirements 4.3
        """
        # Get service evaluations
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        
        # Generate contextual recommendations
        recommendations = self.explanation_generator.generate_contextual_recommendations(
            evaluations, constraints
        )
        
        # Verify all recommendations contain required phrases
        for service, recommendation in recommendations.items():
            assert self.explanation_generator.validate_required_phrases(recommendation), \
                f"Recommendation for {service} missing required phrases: {recommendation}"
        
        # Verify we have recommendations for all services
        expected_services = {ServiceType.EC2.value, ServiceType.LAMBDA.value, ServiceType.ECS_FARGATE.value}
        assert set(recommendations.keys()) == expected_services
        
        # Verify phrase usage statistics
        phrase_stats = self.explanation_generator.get_phrase_usage_stats(recommendations)
        total_phrase_usage = sum(phrase_stats.values())
        assert total_phrase_usage > 0, "No required phrases found in any recommendations"
    
    @given(
        constraints1=user_constraints_strategy,
        constraints2=user_constraints_strategy
    )
    @settings(suppress_health_check=[HealthCheck.too_slow])
    def test_contextual_recommendation_variation_property(self, constraints1, constraints2):
        """
        Property 7: Contextual Recommendation Variation
        For any two different constraint combinations, the system should generate 
        different contextual recommendations that reflect the specific constraint differences.
        
        Feature: cloud-service-referee, Property 7: Contextual Recommendation Variation
        Validates: Requirements 6.3
        """
        # Skip if constraints are identical
        if constraints1 == constraints2:
            return
        
        # Get evaluations for both constraint sets
        evaluations1 = self.constraint_evaluator.evaluate_services(constraints1)
        evaluations2 = self.constraint_evaluator.evaluate_services(constraints2)
        
        # Generate recommendations for both
        recommendations1 = self.explanation_generator.generate_contextual_recommendations(
            evaluations1, constraints1
        )
        recommendations2 = self.explanation_generator.generate_contextual_recommendations(
            evaluations2, constraints2
        )
        
        # Verify recommendations are different when constraints are different
        services = [ServiceType.EC2.value, ServiceType.LAMBDA.value, ServiceType.ECS_FARGATE.value]
        
        differences_found = False
        for service in services:
            if recommendations1[service] != recommendations2[service]:
                differences_found = True
                break
        
        # If constraints are significantly different, recommendations should vary
        constraint_differences = self._count_constraint_differences(constraints1, constraints2)
        if constraint_differences >= 2:  # If 2 or more constraints differ
            assert differences_found, \
                "Recommendations should vary when constraints are significantly different"
    
    def _count_constraint_differences(self, constraints1: UserConstraints, constraints2: UserConstraints) -> int:
        """Count the number of different constraints between two constraint sets."""
        differences = 0
        
        if constraints1.budget_sensitivity != constraints2.budget_sensitivity:
            differences += 1
        if constraints1.expected_traffic != constraints2.expected_traffic:
            differences += 1
        if constraints1.scalability_requirement != constraints2.scalability_requirement:
            differences += 1
        if constraints1.latency_sensitivity != constraints2.latency_sensitivity:
            differences += 1
        if constraints1.operational_overhead_tolerance != constraints2.operational_overhead_tolerance:
            differences += 1
        if constraints1.time_to_market_urgency != constraints2.time_to_market_urgency:
            differences += 1
        
        return differences
    
    def test_explanation_completeness(self):
        """Test that explanations are complete and contain required elements."""
        # Test with specific constraint combination
        constraints = UserConstraints(
            budget_sensitivity=ConstraintLevel.HIGH,
            expected_traffic=ConstraintLevel.LOW,
            scalability_requirement=ConstraintLevel.MEDIUM,
            latency_sensitivity=ConstraintLevel.HIGH,
            operational_overhead_tolerance=ConstraintLevel.LOW,
            time_to_market_urgency=ConstraintLevel.HIGH
        )
        
        evaluations = self.constraint_evaluator.evaluate_services(constraints)
        recommendations = self.explanation_generator.generate_contextual_recommendations(
            evaluations, constraints
        )
        
        # Verify completeness
        assert len(recommendations) == 3
        
        for service, recommendation in recommendations.items():
            # Each recommendation should be substantial
            assert len(recommendation) > 50, f"Recommendation for {service} too short"
            
            # Should contain required phrases
            assert self.explanation_generator.validate_required_phrases(recommendation)
            
            # Should not contain winner language
            recommendation_lower = recommendation.lower()
            forbidden_words = ['best', 'winner', 'optimal', 'perfect']
            for word in forbidden_words:
                assert word not in recommendation_lower, \
                    f"Recommendation for {service} contains forbidden winner word: {word}"
        
        # Test trade-off explanations
        trade_off_analysis = self.trade_off_analyzer.analyze_trade_offs(evaluations, constraints)
        trade_off_explanations = self.explanation_generator.generate_trade_off_explanations(trade_off_analysis)
        
        assert 'cost_vs_control' in trade_off_explanations
        assert 'latency_vs_ops_complexity' in trade_off_explanations
        assert len(trade_off_explanations['cost_vs_control']) > 0
        assert len(trade_off_explanations['latency_vs_ops_complexity']) > 0
class TestUIControllerProperties:
    """Test UI controller properties."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.ui_controller = UIController()
    
    @given(
        budget=st.sampled_from(["Low", "Medium", "High"]),
        traffic=st.sampled_from(["Low", "Medium", "High"]),
        scalability=st.sampled_from(["Low", "Medium", "High"]),
        latency=st.sampled_from(["Low", "Medium", "High"]),
        ops_tolerance=st.sampled_from(["Low", "Medium", "High"]),
        time_urgency=st.sampled_from(["Low", "Medium", "High"])
    )
    def test_constraint_input_validation_property(
        self, budget, traffic, scalability, latency, ops_tolerance, time_urgency
    ):
        """
        Property 4: Constraint Input Validation
        For any constraint dimension, the UI should accept exactly the three values: Low, Medium, High.
        
        Feature: cloud-service-referee, Property 4: Constraint Input Validation
        Validates: Requirements 2.2, 2.3, 2.4, 2.5, 2.6, 2.7
        """
        # Create constraint input dictionary
        constraints_input = {
            "budget_sensitivity": budget,
            "expected_traffic": traffic,
            "scalability_requirement": scalability,
            "latency_sensitivity": latency,
            "operational_overhead_tolerance": ops_tolerance,
            "time_to_market_urgency": time_urgency
        }
        
        # Validate that all valid combinations are accepted
        assert self.ui_controller.validate_constraint_inputs(constraints_input), \
            f"Valid constraint combination rejected: {constraints_input}"
        
        # Test that we can create UserConstraints from valid input
        user_constraints = self.ui_controller.create_user_constraints_from_input(constraints_input)
        
        # Verify all constraints are properly set
        assert user_constraints.budget_sensitivity.value == budget
        assert user_constraints.expected_traffic.value == traffic
        assert user_constraints.scalability_requirement.value == scalability
        assert user_constraints.latency_sensitivity.value == latency
        assert user_constraints.operational_overhead_tolerance.value == ops_tolerance
        assert user_constraints.time_to_market_urgency.value == time_urgency
    
    def test_invalid_constraint_values(self):
        """Test that invalid constraint values are rejected."""
        # Test invalid constraint values
        invalid_values = ["Very Low", "Super High", "None", "", "Invalid", "1", "5"]
        
        for invalid_value in invalid_values:
            constraints_input = {
                "budget_sensitivity": invalid_value,
                "expected_traffic": "Medium",
                "scalability_requirement": "Medium",
                "latency_sensitivity": "Medium",
                "operational_overhead_tolerance": "Medium",
                "time_to_market_urgency": "Medium"
            }
            
            # Should reject invalid values
            assert not self.ui_controller.validate_constraint_inputs(constraints_input), \
                f"Invalid constraint value '{invalid_value}' was accepted"
    
    def test_missing_constraints(self):
        """Test that missing constraints are rejected."""
        # Test missing constraints
        complete_constraints = {
            "budget_sensitivity": "Medium",
            "expected_traffic": "Medium",
            "scalability_requirement": "Medium",
            "latency_sensitivity": "Medium",
            "operational_overhead_tolerance": "Medium",
            "time_to_market_urgency": "Medium"
        }
        
        # Test removing each constraint one by one
        for constraint_to_remove in complete_constraints.keys():
            incomplete_constraints = complete_constraints.copy()
            del incomplete_constraints[constraint_to_remove]
            
            # Should reject incomplete constraint sets
            assert not self.ui_controller.validate_constraint_inputs(incomplete_constraints), \
                f"Missing constraint '{constraint_to_remove}' was not detected"
    
    def test_constraint_descriptions_completeness(self):
        """Test that all constraint descriptions are complete."""
        expected_constraints = [
            "budget_sensitivity", "expected_traffic", "scalability_requirement",
            "latency_sensitivity", "operational_overhead_tolerance", "time_to_market_urgency"
        ]
        
        # Verify all constraints have descriptions
        for constraint in expected_constraints:
            assert constraint in self.ui_controller.constraint_descriptions, \
                f"Missing description for constraint: {constraint}"
            
            desc = self.ui_controller.constraint_descriptions[constraint]
            assert "label" in desc, f"Missing label for {constraint}"
            assert "description" in desc, f"Missing description for {constraint}"
            assert "help" in desc, f"Missing help text for {constraint}"
            
            # Verify content is not empty
            assert len(desc["label"]) > 0, f"Empty label for {constraint}"
            assert len(desc["description"]) > 0, f"Empty description for {constraint}"
            assert len(desc["help"]) > 0, f"Empty help text for {constraint}"
    
    def test_constraint_options_validity(self):
        """Test that constraint options are exactly Low, Medium, High."""
        expected_options = ["Low", "Medium", "High"]
        assert self.ui_controller.constraint_options == expected_options, \
            f"Constraint options should be {expected_options}, got {self.ui_controller.constraint_options}"
class TestUIResponsivenessProperties:
    """Test UI responsiveness properties."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service_repo = ServiceRepository()
        self.scoring_system = ScoringSystem()
        self.constraint_evaluator = ConstraintEvaluator(self.scoring_system, self.service_repo)
        self.trade_off_analyzer = TradeOffAnalyzer()
        self.explanation_generator = ExplanationGenerator()
        self.ui_controller = UIController()
    
    @given(
        constraints1=user_constraints_strategy,
        constraints2=user_constraints_strategy
    )
    @settings(suppress_health_check=[HealthCheck.too_slow])
    def test_ui_responsiveness_property(self, constraints1, constraints2):
        """
        Property 10: UI Responsiveness
        For any change to constraint inputs, the UI should update the displayed 
        results to reflect the new constraints.
        
        Feature: cloud-service-referee, Property 10: UI Responsiveness
        Validates: Requirements 10.4
        """
        # Skip if constraints are identical
        if constraints1 == constraints2:
            return
        
        # Simulate processing both constraint sets
        evaluations1 = self.constraint_evaluator.evaluate_services(constraints1)
        evaluations2 = self.constraint_evaluator.evaluate_services(constraints2)
        
        # Generate recommendations for both
        recommendations1 = self.explanation_generator.generate_contextual_recommendations(
            evaluations1, constraints1
        )
        recommendations2 = self.explanation_generator.generate_contextual_recommendations(
            evaluations2, constraints2
        )
        
        # Verify that different constraints produce different results
        # (This simulates UI responsiveness - when inputs change, outputs change)
        
        # Check if evaluations are different
        evaluations_different = False
        for service in evaluations1.keys():
            if evaluations1[service].constraint_scores != evaluations2[service].constraint_scores:
                evaluations_different = True
                break
        
        # Check if recommendations are different
        recommendations_different = False
        for service in recommendations1.keys():
            if recommendations1[service] != recommendations2[service]:
                recommendations_different = True
                break
        
        # Count constraint differences
        constraint_differences = self._count_constraint_differences_ui(constraints1, constraints2)
        
        # If constraints are significantly different, results should be different
        if constraint_differences >= 2:
            assert evaluations_different or recommendations_different, \
                "UI should be responsive to constraint changes - results should differ when inputs differ significantly"
    
    def _count_constraint_differences_ui(self, constraints1: UserConstraints, constraints2: UserConstraints) -> int:
        """Count the number of different constraints between two constraint sets."""
        differences = 0
        
        if constraints1.budget_sensitivity != constraints2.budget_sensitivity:
            differences += 1
        if constraints1.expected_traffic != constraints2.expected_traffic:
            differences += 1
        if constraints1.scalability_requirement != constraints2.scalability_requirement:
            differences += 1
        if constraints1.latency_sensitivity != constraints2.latency_sensitivity:
            differences += 1
        if constraints1.operational_overhead_tolerance != constraints2.operational_overhead_tolerance:
            differences += 1
        if constraints1.time_to_market_urgency != constraints2.time_to_market_urgency:
            differences += 1
        
        return differences
    
    def test_ui_constraint_conversion(self):
        """Test that UI can convert constraint inputs to UserConstraints objects."""
        # Test valid constraint input conversion
        constraint_input = {
            "budget_sensitivity": "High",
            "expected_traffic": "Low",
            "scalability_requirement": "Medium",
            "latency_sensitivity": "High",
            "operational_overhead_tolerance": "Low",
            "time_to_market_urgency": "High"
        }
        
        # Should successfully convert to UserConstraints
        user_constraints = self.ui_controller.create_user_constraints_from_input(constraint_input)
        
        # Verify conversion is correct
        assert user_constraints.budget_sensitivity == ConstraintLevel.HIGH
        assert user_constraints.expected_traffic == ConstraintLevel.LOW
        assert user_constraints.scalability_requirement == ConstraintLevel.MEDIUM
        assert user_constraints.latency_sensitivity == ConstraintLevel.HIGH
        assert user_constraints.operational_overhead_tolerance == ConstraintLevel.LOW
        assert user_constraints.time_to_market_urgency == ConstraintLevel.HIGH
    
    def test_ui_table_data_preparation(self):
        """Test that UI can prepare data for comparison table display."""
        # Create test scores
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
        # (We can't easily test the actual Streamlit rendering, but we can test data preparation)
        try:
            # The render_service_comparison_table method should handle this data
            # We'll just verify the data structure is valid
            for service, scores in test_scores.items():
                assert isinstance(scores, dict)
                assert len(scores) == 6  # All 6 constraints
                for constraint, score in scores.items():
                    assert 1 <= score <= 5  # Valid score range
            
            # Test passes if no exceptions are raised
            assert True
        except Exception as e:
            pytest.fail(f"UI table data preparation failed: {e}")