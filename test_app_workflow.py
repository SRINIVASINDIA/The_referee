"""
Test script to validate the complete application workflow.
"""
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.models import UserConstraints, ConstraintLevel
from src.service_repository import ServiceRepository
from src.scoring_system import ScoringSystem
from src.constraint_evaluator import ConstraintEvaluator
from src.trade_off_analyzer import TradeOffAnalyzer
from src.explanation_generator import ExplanationGenerator
from src.comparison_engine import ComparisonEngine
from src.ui_controller import UIController


def test_complete_workflow():
    """Test the complete application workflow."""
    print("🏛️ Testing Cloud Service Referee Workflow")
    print("=" * 50)
    
    # Initialize components
    print("1. Initializing components...")
    service_repo = ServiceRepository()
    scoring_system = ScoringSystem()
    constraint_evaluator = ConstraintEvaluator(scoring_system, service_repo)
    trade_off_analyzer = TradeOffAnalyzer()
    explanation_generator = ExplanationGenerator()
    
    comparison_engine = ComparisonEngine(
        constraint_evaluator=constraint_evaluator,
        trade_off_analyzer=trade_off_analyzer,
        explanation_generator=explanation_generator
    )
    
    ui_controller = UIController()
    print("✅ Components initialized successfully")
    
    # Test constraint input validation
    print("\n2. Testing constraint input validation...")
    test_constraints = {
        "budget_sensitivity": "High",
        "expected_traffic": "Low",
        "scalability_requirement": "Medium",
        "latency_sensitivity": "High",
        "operational_overhead_tolerance": "Low",
        "time_to_market_urgency": "High"
    }
    
    assert ui_controller.validate_constraint_inputs(test_constraints)
    print("✅ Constraint validation working")
    
    # Convert to UserConstraints
    print("\n3. Converting constraints...")
    user_constraints = ui_controller.create_user_constraints_from_input(test_constraints)
    print(f"✅ Constraints converted: {user_constraints}")
    
    # Perform comparison
    print("\n4. Performing service comparison...")
    comparison_result = comparison_engine.compare_services(user_constraints)
    print("✅ Comparison completed successfully")
    
    # Validate results
    print("\n5. Validating results...")
    assert len(comparison_result.evaluations) == 3, "Should have 3 service evaluations"
    assert len(comparison_result.contextual_recommendations) == 3, "Should have 3 recommendations"
    assert comparison_result.trade_off_analysis is not None, "Should have trade-off analysis"
    
    print("✅ Results validation passed")
    
    # Test specific service scores
    print("\n6. Testing service scores...")
    for service, evaluation in comparison_result.evaluations.items():
        print(f"   {service}: {len(evaluation.constraint_scores)} constraint scores")
        assert len(evaluation.constraint_scores) == 6, f"{service} should have 6 constraint scores"
        
        for constraint, score in evaluation.constraint_scores.items():
            assert 1 <= score <= 5, f"Score {score} for {service}.{constraint} outside valid range"
    
    print("✅ Service scores validation passed")
    
    # Test recommendations contain required phrases
    print("\n7. Testing recommendation phrases...")
    for service, recommendation in comparison_result.contextual_recommendations.items():
        assert explanation_generator.validate_required_phrases(recommendation), \
            f"Recommendation for {service} missing required phrases"
    
    print("✅ Required phrases validation passed")
    
    # Test edge case detection
    print("\n8. Testing edge case detection...")
    if comparison_result.edge_case_warnings:
        print(f"   Detected {len(comparison_result.edge_case_warnings)} edge case warnings")
        for warning in comparison_result.edge_case_warnings:
            print(f"   - {warning[:100]}...")
    else:
        print("   No edge cases detected for this constraint combination")
    
    print("✅ Edge case detection working")
    
    # Summary
    print("\n" + "=" * 50)
    print("🎉 Complete workflow test PASSED!")
    print("\nSummary:")
    print(f"   Services evaluated: {len(comparison_result.evaluations)}")
    print(f"   Recommendations generated: {len(comparison_result.contextual_recommendations)}")
    print(f"   Edge case warnings: {len(comparison_result.edge_case_warnings)}")
    print(f"   Trade-off analysis: {'✅' if comparison_result.trade_off_analysis else '❌'}")
    
    return True


if __name__ == "__main__":
    try:
        test_complete_workflow()
    except Exception as e:
        print(f"\n❌ Workflow test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)