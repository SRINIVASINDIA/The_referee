"""
Comparison engine that coordinates service evaluation and analysis.
"""
from typing import Dict, List
from .models import UserConstraints, ServiceEvaluation, ComparisonResult, TradeOffAnalysis
from .interfaces import (
    ConstraintEvaluatorInterface, 
    TradeOffAnalyzerInterface, 
    ExplanationGeneratorInterface
)


class ComparisonEngine:
    """Coordinates the complete service comparison process."""
    
    def __init__(
        self,
        constraint_evaluator: ConstraintEvaluatorInterface,
        trade_off_analyzer: TradeOffAnalyzerInterface,
        explanation_generator: ExplanationGeneratorInterface
    ):
        """Initialize the comparison engine with its dependencies."""
        self.constraint_evaluator = constraint_evaluator
        self.trade_off_analyzer = trade_off_analyzer
        self.explanation_generator = explanation_generator
    
    def compare_services(self, constraints: UserConstraints) -> ComparisonResult:
        """Perform complete service comparison and analysis."""
        try:
            # Step 1: Evaluate all services independently
            evaluations = self.constraint_evaluator.evaluate_services(constraints)
            
            # Step 2: Analyze trade-offs between services
            trade_off_analysis = self.trade_off_analyzer.analyze_trade_offs(evaluations, constraints)
            
            # Step 3: Generate contextual recommendations
            contextual_recommendations = self.explanation_generator.generate_contextual_recommendations(
                evaluations, constraints
            )
            
            # Step 4: Identify edge case warnings
            edge_case_warnings = self._identify_edge_case_warnings(constraints, evaluations)
            
            # Step 5: Create complete comparison result
            result = ComparisonResult(
                evaluations=evaluations,
                trade_off_analysis=trade_off_analysis,
                contextual_recommendations=contextual_recommendations,
                edge_case_warnings=edge_case_warnings
            )
            
            # Step 6: Validate neutrality is maintained
            self._validate_neutrality(result)
            
            return result
            
        except Exception as e:
            # Handle any errors gracefully
            raise RuntimeError(f"Comparison engine failed: {str(e)}") from e
    
    def _identify_edge_case_warnings(
        self, 
        constraints: UserConstraints, 
        evaluations: Dict[str, ServiceEvaluation]
    ) -> List[str]:
        """Identify edge cases and conflicting constraints."""
        warnings = []
        
        # Check for low budget + high scalability tension
        if (constraints.budget_sensitivity.value == "High" and 
            constraints.scalability_requirement.value == "High"):
            warnings.append(
                "Edge case detected: High budget sensitivity with high scalability requirements "
                "creates inherent tension. The trade-off here is between cost control and "
                "scaling capabilities."
            )
        
        # Check for high latency sensitivity + high traffic tension
        if (constraints.latency_sensitivity.value == "High" and 
            constraints.expected_traffic.value == "High"):
            warnings.append(
                "Performance consideration: High latency sensitivity with high traffic "
                "requires careful service selection. This may be a limitation if cold starts "
                "or provisioning delays are not acceptable."
            )
        
        # Check for fast time-to-market + low operational tolerance contradiction
        if (constraints.time_to_market_urgency.value == "High" and 
            constraints.operational_overhead_tolerance.value == "Low"):
            warnings.append(
                "Constraint alignment: Fast time-to-market with low operational tolerance "
                "suggests serverless solutions. This is a good choice when rapid deployment "
                "is prioritized over infrastructure control."
            )
        
        # Check for conflicting budget and performance requirements
        if (constraints.budget_sensitivity.value == "High" and 
            constraints.latency_sensitivity.value == "High"):
            warnings.append(
                "Trade-off consideration: High budget sensitivity with high latency sensitivity "
                "may require careful optimization. The trade-off here is between cost efficiency "
                "and performance guarantees."
            )
        
        return warnings
    
    def _validate_neutrality(self, result: ComparisonResult) -> None:
        """Validate that the comparison result maintains neutrality."""
        # Check that no service is declared as the winner
        if not self.constraint_evaluator.validate_no_winner_declaration(result.evaluations):
            raise ValueError("Neutrality violation: A service was declared as winner")
        
        # Check that all services are represented
        expected_services = 3  # EC2, Lambda, ECS Fargate
        if len(result.evaluations) != expected_services:
            raise ValueError(f"Expected {expected_services} services, got {len(result.evaluations)}")
        
        # Check that all services have recommendations
        if len(result.contextual_recommendations) != expected_services:
            raise ValueError("Not all services have contextual recommendations")
        
        # Validate that recommendations don't contain winner language
        winner_phrases = ['best choice', 'optimal', 'winner', 'perfect solution']
        for service, recommendation in result.contextual_recommendations.items():
            recommendation_lower = recommendation.lower()
            for phrase in winner_phrases:
                if phrase in recommendation_lower:
                    raise ValueError(f"Winner language detected in {service} recommendation: {phrase}")
    
    def get_comparison_summary(self, result: ComparisonResult) -> Dict[str, any]:
        """Get a neutral summary of the comparison without declaring winners."""
        summary = {
            'services_evaluated': len(result.evaluations),
            'edge_cases_identified': len(result.edge_case_warnings),
            'trade_offs_analyzed': bool(result.trade_off_analysis),
            'recommendations_provided': len(result.contextual_recommendations),
            'service_scores': {}
        }
        
        # Add score summaries for each service (without ranking)
        for service, evaluation in result.evaluations.items():
            scores = evaluation.constraint_scores
            summary['service_scores'][service] = {
                'constraint_count': len(scores),
                'average_score': round(sum(scores.values()) / len(scores), 2),
                'score_range': f"{min(scores.values())}-{max(scores.values())}"
            }
        
        return summary
    
    def validate_constraint_handling(self, constraints: UserConstraints) -> bool:
        """Validate that all constraint combinations can be handled."""
        try:
            # Attempt to process the constraints
            result = self.compare_services(constraints)
            
            # Verify result completeness
            return (
                len(result.evaluations) == 3 and
                result.trade_off_analysis is not None and
                len(result.contextual_recommendations) == 3
            )
        except Exception:
            return False