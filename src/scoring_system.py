"""
Rule-based scoring system for AWS compute services.
"""
from typing import Dict
from .models import UserConstraints, ConstraintLevel, ServiceType
from .interfaces import ScoringSystemInterface


class ScoringSystem(ScoringSystemInterface):
    """Rule-based scoring system that evaluates services against constraints."""
    
    def __init__(self):
        """Initialize the scoring system with predefined rules."""
        self._scoring_rules = self._initialize_scoring_rules()
    
    def _initialize_scoring_rules(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        """Initialize scoring rules for all constraint-service combinations."""
        return {
            "budget_sensitivity": {
                ConstraintLevel.LOW.value: {
                    ServiceType.EC2.value: 4,
                    ServiceType.LAMBDA.value: 3,
                    ServiceType.ECS_FARGATE.value: 2
                },
                ConstraintLevel.MEDIUM.value: {
                    ServiceType.EC2.value: 5,
                    ServiceType.LAMBDA.value: 3,
                    ServiceType.ECS_FARGATE.value: 2
                },
                ConstraintLevel.HIGH.value: {
                    ServiceType.EC2.value: 5,
                    ServiceType.LAMBDA.value: 2,
                    ServiceType.ECS_FARGATE.value: 1
                }
            },
            "expected_traffic": {
                ConstraintLevel.LOW.value: {
                    ServiceType.EC2.value: 2,
                    ServiceType.LAMBDA.value: 5,
                    ServiceType.ECS_FARGATE.value: 3
                },
                ConstraintLevel.MEDIUM.value: {
                    ServiceType.EC2.value: 4,
                    ServiceType.LAMBDA.value: 4,
                    ServiceType.ECS_FARGATE.value: 4
                },
                ConstraintLevel.HIGH.value: {
                    ServiceType.EC2.value: 5,
                    ServiceType.LAMBDA.value: 3,
                    ServiceType.ECS_FARGATE.value: 4
                }
            },
            "scalability_requirement": {
                ConstraintLevel.LOW.value: {
                    ServiceType.EC2.value: 3,
                    ServiceType.LAMBDA.value: 4,
                    ServiceType.ECS_FARGATE.value: 4
                },
                ConstraintLevel.MEDIUM.value: {
                    ServiceType.EC2.value: 4,
                    ServiceType.LAMBDA.value: 5,
                    ServiceType.ECS_FARGATE.value: 5
                },
                ConstraintLevel.HIGH.value: {
                    ServiceType.EC2.value: 3,
                    ServiceType.LAMBDA.value: 5,
                    ServiceType.ECS_FARGATE.value: 4
                }
            },
            "latency_sensitivity": {
                ConstraintLevel.LOW.value: {
                    ServiceType.EC2.value: 4,
                    ServiceType.LAMBDA.value: 3,
                    ServiceType.ECS_FARGATE.value: 4
                },
                ConstraintLevel.MEDIUM.value: {
                    ServiceType.EC2.value: 5,
                    ServiceType.LAMBDA.value: 3,
                    ServiceType.ECS_FARGATE.value: 4
                },
                ConstraintLevel.HIGH.value: {
                    ServiceType.EC2.value: 5,
                    ServiceType.LAMBDA.value: 1,
                    ServiceType.ECS_FARGATE.value: 3
                }
            },
            "operational_overhead_tolerance": {
                ConstraintLevel.LOW.value: {
                    ServiceType.EC2.value: 1,
                    ServiceType.LAMBDA.value: 5,
                    ServiceType.ECS_FARGATE.value: 4
                },
                ConstraintLevel.MEDIUM.value: {
                    ServiceType.EC2.value: 2,
                    ServiceType.LAMBDA.value: 5,
                    ServiceType.ECS_FARGATE.value: 4
                },
                ConstraintLevel.HIGH.value: {
                    ServiceType.EC2.value: 4,
                    ServiceType.LAMBDA.value: 4,
                    ServiceType.ECS_FARGATE.value: 3
                }
            },
            "time_to_market_urgency": {
                ConstraintLevel.LOW.value: {
                    ServiceType.EC2.value: 3,
                    ServiceType.LAMBDA.value: 4,
                    ServiceType.ECS_FARGATE.value: 3
                },
                ConstraintLevel.MEDIUM.value: {
                    ServiceType.EC2.value: 2,
                    ServiceType.LAMBDA.value: 5,
                    ServiceType.ECS_FARGATE.value: 4
                },
                ConstraintLevel.HIGH.value: {
                    ServiceType.EC2.value: 1,
                    ServiceType.LAMBDA.value: 5,
                    ServiceType.ECS_FARGATE.value: 3
                }
            }
        }
    
    def score_service_against_constraint(
        self, 
        service: str, 
        constraint: str, 
        value: str
    ) -> int:
        """Score a service against a specific constraint."""
        if constraint not in self._scoring_rules:
            raise ValueError(f"Unknown constraint: {constraint}")
        
        if value not in self._scoring_rules[constraint]:
            raise ValueError(f"Unknown constraint value: {value}")
        
        if service not in self._scoring_rules[constraint][value]:
            raise ValueError(f"Unknown service: {service}")
        
        score = self._scoring_rules[constraint][value][service]
        
        # Validate score is within 1-5 range
        if not (1 <= score <= 5):
            raise ValueError(f"Invalid score {score} for {service} on {constraint}={value}")
        
        return score
    
    def get_all_scores(
        self, 
        service: str, 
        constraints: UserConstraints
    ) -> Dict[str, int]:
        """Get all constraint scores for a service."""
        scores = {}
        
        constraint_mapping = {
            "budget_sensitivity": constraints.budget_sensitivity.value,
            "expected_traffic": constraints.expected_traffic.value,
            "scalability_requirement": constraints.scalability_requirement.value,
            "latency_sensitivity": constraints.latency_sensitivity.value,
            "operational_overhead_tolerance": constraints.operational_overhead_tolerance.value,
            "time_to_market_urgency": constraints.time_to_market_urgency.value
        }
        
        for constraint_name, constraint_value in constraint_mapping.items():
            scores[constraint_name] = self.score_service_against_constraint(
                service, constraint_name, constraint_value
            )
        
        return scores
    
    def get_scoring_rationale(self, service: str, constraint: str, value: str) -> str:
        """Get the rationale for a specific score."""
        # This would be expanded with detailed rationale for each score
        score = self.score_service_against_constraint(service, constraint, value)
        return f"Score {score}/5 for {service} on {constraint}={value}"
    
    def validate_all_rules(self) -> bool:
        """Validate that all scoring rules are complete and within valid range."""
        expected_constraints = [
            "budget_sensitivity", "expected_traffic", "scalability_requirement",
            "latency_sensitivity", "operational_overhead_tolerance", "time_to_market_urgency"
        ]
        expected_levels = [ConstraintLevel.LOW.value, ConstraintLevel.MEDIUM.value, ConstraintLevel.HIGH.value]
        expected_services = [ServiceType.EC2.value, ServiceType.LAMBDA.value, ServiceType.ECS_FARGATE.value]
        
        for constraint in expected_constraints:
            if constraint not in self._scoring_rules:
                return False
            
            for level in expected_levels:
                if level not in self._scoring_rules[constraint]:
                    return False
                
                for service in expected_services:
                    if service not in self._scoring_rules[constraint][level]:
                        return False
                    
                    score = self._scoring_rules[constraint][level][service]
                    if not (1 <= score <= 5):
                        return False
        
        return True