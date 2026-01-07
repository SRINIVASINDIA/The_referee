"""
Core data models for the Cloud Service Referee application.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ConstraintLevel(Enum):
    """Enumeration for constraint levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class ServiceType(Enum):
    """Enumeration for AWS service types."""
    EC2 = "EC2"
    LAMBDA = "Lambda"
    ECS_FARGATE = "ECS_Fargate"


@dataclass
class UserConstraints:
    """User-defined constraints for service evaluation."""
    budget_sensitivity: ConstraintLevel
    expected_traffic: ConstraintLevel
    scalability_requirement: ConstraintLevel
    latency_sensitivity: ConstraintLevel
    operational_overhead_tolerance: ConstraintLevel
    time_to_market_urgency: ConstraintLevel


@dataclass
class ServiceEvaluation:
    """Evaluation results for a single service."""
    service_name: str
    constraint_scores: Dict[str, int]  # constraint -> score (1-5)
    strengths: List[str]
    limitations: List[str]
    best_use_cases: List[str]


@dataclass
class TradeOffAnalysis:
    """Analysis of trade-offs between services."""
    cost_vs_control: str
    latency_vs_ops_complexity: str
    edge_case_warnings: List[str]
    conflicting_constraints: List[str]


@dataclass
class ComparisonResult:
    """Complete comparison result for all services."""
    evaluations: Dict[str, ServiceEvaluation]  # service -> evaluation
    trade_off_analysis: TradeOffAnalysis
    contextual_recommendations: Dict[str, str]  # service -> recommendation
    edge_case_warnings: List[str]


@dataclass
class ServiceCharacteristics:
    """Static characteristics of an AWS service."""
    name: str
    strengths: List[str]
    limitations: List[str]
    best_use_cases: List[str]
    cost_model: str
    scaling_characteristics: str
    operational_overhead: str