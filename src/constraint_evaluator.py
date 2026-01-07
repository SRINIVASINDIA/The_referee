"""
Constraint evaluator component for the Cloud Service Referee application.
"""
from typing import Dict
from .models import UserConstraints, ServiceEvaluation
from .interfaces import ConstraintEvaluatorInterface, ScoringSystemInterface, ServiceRepositoryInterface


class ConstraintEvaluator(ConstraintEvaluatorInterface):
    """Evaluates services against user constraints independently."""
    
    def __init__(
        self, 
        scoring_system: ScoringSystemInterface,
        service_repository: ServiceRepositoryInterface
    ):
        """Initialize the constraint evaluator with dependencies."""
        self.scoring_system = scoring_system
        self.service_repository = service_repository
    
    def evaluate_services(
        self, 
        constraints: UserConstraints
    ) -> Dict[str, ServiceEvaluation]:
        """Evaluate all services against user constraints."""
        evaluations = {}
        services = self.service_repository.get_all_services()
        
        for service in services:
            evaluations[service] = self.evaluate_single_service(service, constraints)
        
        return evaluations
    
    def evaluate_single_service(
        self, 
        service: str, 
        constraints: UserConstraints
    ) -> ServiceEvaluation:
        """Evaluate a single service against constraints."""
        # Get service characteristics
        characteristics = self.service_repository.get_service_characteristics(service)
        
        # Get constraint scores
        constraint_scores = self.scoring_system.get_all_scores(service, constraints)
        
        # Create service evaluation
        evaluation = ServiceEvaluation(
            service_name=characteristics.name,
            constraint_scores=constraint_scores,
            strengths=characteristics.strengths.copy(),  # Copy to ensure independence
            limitations=characteristics.limitations.copy(),  # Copy to ensure independence
            best_use_cases=characteristics.best_use_cases.copy()  # Copy to ensure independence
        )
        
        return evaluation
    
    def _ensure_evaluation_independence(self, evaluations: Dict[str, ServiceEvaluation]) -> None:
        """Ensure that service evaluations are independent of each other."""
        # This method validates that no cross-service influence occurred
        # It's called internally to maintain the independence principle
        
        services = list(evaluations.keys())
        
        # Verify that each service has its own distinct evaluation
        for i, service1 in enumerate(services):
            for service2 in services[i+1:]:
                eval1 = evaluations[service1]
                eval2 = evaluations[service2]
                
                # Services should have different names
                assert eval1.service_name != eval2.service_name, \
                    f"Services {service1} and {service2} have identical names"
                
                # Services should have different characteristics
                # (This ensures no cross-contamination of service data)
                assert eval1.strengths != eval2.strengths, \
                    f"Services {service1} and {service2} have identical strengths"
                
                assert eval1.limitations != eval2.limitations, \
                    f"Services {service1} and {service2} have identical limitations"
    
    def get_evaluation_summary(self, evaluations: Dict[str, ServiceEvaluation]) -> Dict[str, Dict[str, float]]:
        """Get a summary of evaluations without declaring winners."""
        summary = {}
        
        for service, evaluation in evaluations.items():
            scores = evaluation.constraint_scores
            summary[service] = {
                'average_score': sum(scores.values()) / len(scores),
                'score_count': len(scores),
                'min_score': min(scores.values()),
                'max_score': max(scores.values())
            }
        
        return summary
    
    def validate_no_winner_declaration(self, evaluations: Dict[str, ServiceEvaluation]) -> bool:
        """Validate that no single service is declared as the winner."""
        # This method ensures we maintain neutrality
        # It checks that we don't have any "best" or "winner" declarations
        
        for service, evaluation in evaluations.items():
            # Check that no evaluation contains winner language
            all_text = ' '.join([
                evaluation.service_name,
                ' '.join(evaluation.strengths),
                ' '.join(evaluation.limitations),
                ' '.join(evaluation.best_use_cases)
            ]).lower()
            
            # Forbidden winner words
            winner_words = ['best', 'winner', 'optimal', 'perfect', 'ideal choice']
            for word in winner_words:
                if word in all_text:
                    return False
        
        return True