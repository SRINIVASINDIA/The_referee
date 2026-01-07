"""
Interface definitions for the Cloud Service Referee application.
"""
from abc import ABC, abstractmethod
from typing import Dict, List
from .models import (
    UserConstraints, ServiceEvaluation, ComparisonResult, 
    TradeOffAnalysis, ServiceCharacteristics
)


class ScoringSystemInterface(ABC):
    """Interface for the scoring system component."""
    
    @abstractmethod
    def score_service_against_constraint(
        self, 
        service: str, 
        constraint: str, 
        value: str
    ) -> int:
        """Score a service against a specific constraint."""
        pass
    
    @abstractmethod
    def get_all_scores(
        self, 
        service: str, 
        constraints: UserConstraints
    ) -> Dict[str, int]:
        """Get all constraint scores for a service."""
        pass


class ConstraintEvaluatorInterface(ABC):
    """Interface for the constraint evaluator component."""
    
    @abstractmethod
    def evaluate_services(
        self, 
        constraints: UserConstraints
    ) -> Dict[str, ServiceEvaluation]:
        """Evaluate all services against user constraints."""
        pass
    
    @abstractmethod
    def evaluate_single_service(
        self, 
        service: str, 
        constraints: UserConstraints
    ) -> ServiceEvaluation:
        """Evaluate a single service against constraints."""
        pass


class TradeOffAnalyzerInterface(ABC):
    """Interface for the trade-off analyzer component."""
    
    @abstractmethod
    def analyze_trade_offs(
        self, 
        evaluations: Dict[str, ServiceEvaluation],
        constraints: UserConstraints
    ) -> TradeOffAnalysis:
        """Analyze trade-offs between services."""
        pass
    
    @abstractmethod
    def identify_constraint_conflicts(
        self, 
        constraints: UserConstraints
    ) -> List[str]:
        """Identify conflicting constraints."""
        pass


class ExplanationGeneratorInterface(ABC):
    """Interface for the explanation generator component."""
    
    @abstractmethod
    def generate_contextual_recommendations(
        self, 
        evaluations: Dict[str, ServiceEvaluation],
        constraints: UserConstraints
    ) -> Dict[str, str]:
        """Generate contextual recommendations for each service."""
        pass
    
    @abstractmethod
    def generate_trade_off_explanations(
        self, 
        analysis: TradeOffAnalysis
    ) -> Dict[str, str]:
        """Generate plain English trade-off explanations."""
        pass


class ServiceRepositoryInterface(ABC):
    """Interface for the service repository component."""
    
    @abstractmethod
    def get_service_characteristics(self, service: str) -> ServiceCharacteristics:
        """Get characteristics for a specific service."""
        pass
    
    @abstractmethod
    def get_all_services(self) -> List[str]:
        """Get list of all available services."""
        pass


class UIControllerInterface(ABC):
    """Interface for the UI controller component."""
    
    @abstractmethod
    def render_constraint_inputs(self) -> Dict[str, str]:
        """Render constraint input controls and return values."""
        pass
    
    @abstractmethod
    def display_comparison_results(self, results: ComparisonResult) -> None:
        """Display comparison results in the UI."""
        pass
    
    @abstractmethod
    def render_service_comparison_table(
        self, 
        scores: Dict[str, Dict[str, int]]
    ) -> None:
        """Render the service comparison table."""
        pass