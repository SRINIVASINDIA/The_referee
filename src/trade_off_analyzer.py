"""
Trade-off analyzer component for identifying and explaining service trade-offs.
"""
from typing import Dict, List
from .models import UserConstraints, ServiceEvaluation, TradeOffAnalysis, ConstraintLevel
from .interfaces import TradeOffAnalyzerInterface


class TradeOffAnalyzer(TradeOffAnalyzerInterface):
    """Analyzes trade-offs between AWS compute services."""
    
    def analyze_trade_offs(
        self, 
        evaluations: Dict[str, ServiceEvaluation],
        constraints: UserConstraints
    ) -> TradeOffAnalysis:
        """Analyze trade-offs between services based on evaluations and constraints."""
        
        # Analyze cost vs control trade-offs
        cost_vs_control = self._analyze_cost_vs_control_trade_offs(evaluations, constraints)
        
        # Analyze latency vs operational complexity trade-offs
        latency_vs_ops = self._analyze_latency_vs_ops_trade_offs(evaluations, constraints)
        
        # Identify edge case warnings
        edge_case_warnings = self._generate_edge_case_warnings(constraints)
        
        # Identify conflicting constraints
        conflicting_constraints = self.identify_constraint_conflicts(constraints)
        
        return TradeOffAnalysis(
            cost_vs_control=cost_vs_control,
            latency_vs_ops_complexity=latency_vs_ops,
            edge_case_warnings=edge_case_warnings,
            conflicting_constraints=conflicting_constraints
        )
    
    def _analyze_cost_vs_control_trade_offs(
        self, 
        evaluations: Dict[str, ServiceEvaluation],
        constraints: UserConstraints
    ) -> str:
        """Analyze cost vs control trade-offs between services."""
        
        analysis_parts = []
        
        # EC2 cost vs control analysis
        analysis_parts.append(
            "EC2 offers the highest level of infrastructure control but requires significant "
            "operational investment. This is a good choice when you need specialized hardware, "
            "custom OS configurations, or want to optimize costs through reserved instances. "
            "The trade-off here is between maximum flexibility and operational complexity."
        )
        
        # Lambda cost vs control analysis
        if constraints.budget_sensitivity == ConstraintLevel.HIGH:
            analysis_parts.append(
                "Lambda eliminates infrastructure control in exchange for zero operational overhead. "
                "This may be a limitation if you need predictable costs at high scale, as Lambda "
                "pricing can become expensive with sustained high usage. This is a good choice when "
                "operational simplicity outweighs cost predictability."
            )
        else:
            analysis_parts.append(
                "Lambda trades infrastructure control for operational simplicity. The trade-off here "
                "is between hands-off management and cost predictability at scale."
            )
        
        # ECS Fargate cost vs control analysis
        analysis_parts.append(
            "ECS Fargate provides a middle ground, offering container-level control without server "
            "management. This may be a limitation if cost optimization is critical, as Fargate has "
            "higher per-unit costs than EC2. This is a good choice when you want container benefits "
            "without Kubernetes complexity."
        )
        
        return " ".join(analysis_parts)
    
    def _analyze_latency_vs_ops_trade_offs(
        self, 
        evaluations: Dict[str, ServiceEvaluation],
        constraints: UserConstraints
    ) -> str:
        """Analyze latency vs operational complexity trade-offs."""
        
        analysis_parts = []
        
        if constraints.latency_sensitivity == ConstraintLevel.HIGH:
            analysis_parts.append(
                "High latency sensitivity creates clear trade-offs between performance and operational complexity. "
                "EC2 provides the most consistent, low-latency performance but requires extensive operational "
                "management including monitoring, patching, and scaling configuration."
            )
            
            analysis_parts.append(
                "Lambda's cold start latency (100-800ms) may be a limitation if consistent low latency "
                "is required. The trade-off here is between zero operational overhead and performance "
                "predictability."
            )
            
            analysis_parts.append(
                "ECS Fargate offers better latency than Lambda but with some operational complexity. "
                "This is a good choice when you need better performance than Lambda but less operational "
                "overhead than EC2."
            )
        else:
            analysis_parts.append(
                "With moderate latency requirements, the trade-off shifts toward operational efficiency. "
                "Lambda's occasional cold starts become acceptable in exchange for zero infrastructure "
                "management. The trade-off here is between perfect performance and operational simplicity."
            )
        
        return " ".join(analysis_parts)
    
    def _generate_edge_case_warnings(self, constraints: UserConstraints) -> List[str]:
        """Generate warnings for edge cases and conflicting constraints."""
        warnings = []
        
        # Low budget + high scalability tension
        if (constraints.budget_sensitivity == ConstraintLevel.HIGH and 
            constraints.scalability_requirement == ConstraintLevel.HIGH):
            warnings.append(
                "Budget-scalability tension: High budget sensitivity with high scalability creates "
                "inherent conflict. The trade-off here is between cost control and scaling capabilities. "
                "This may be a limitation if both constraints are equally important."
            )
        
        # High latency sensitivity + high traffic
        if (constraints.latency_sensitivity == ConstraintLevel.HIGH and 
            constraints.expected_traffic == ConstraintLevel.HIGH):
            warnings.append(
                "Performance-scale challenge: High latency sensitivity with high traffic requires "
                "careful architecture. This is a good choice when consistent performance is critical, "
                "but may require significant infrastructure investment."
            )
        
        # Fast time-to-market + low operational tolerance
        if (constraints.time_to_market_urgency == ConstraintLevel.HIGH and 
            constraints.operational_overhead_tolerance == ConstraintLevel.LOW):
            warnings.append(
                "Speed-simplicity alignment: Fast time-to-market with low operational tolerance "
                "strongly favors serverless solutions. This is a good choice when rapid deployment "
                "is the priority, though it may limit long-term optimization options."
            )
        
        return warnings
    
    def identify_constraint_conflicts(self, constraints: UserConstraints) -> List[str]:
        """Identify conflicting constraints that create decision tensions."""
        conflicts = []
        
        # Budget vs Performance conflicts
        if (constraints.budget_sensitivity == ConstraintLevel.HIGH and 
            constraints.latency_sensitivity == ConstraintLevel.HIGH):
            conflicts.append("Budget sensitivity vs Latency sensitivity")
        
        # Budget vs Scalability conflicts
        if (constraints.budget_sensitivity == ConstraintLevel.HIGH and 
            constraints.scalability_requirement == ConstraintLevel.HIGH):
            conflicts.append("Budget sensitivity vs Scalability requirement")
        
        # Time-to-market vs Control conflicts
        if (constraints.time_to_market_urgency == ConstraintLevel.HIGH and 
            constraints.operational_overhead_tolerance == ConstraintLevel.HIGH):
            conflicts.append("Time-to-market urgency vs Operational overhead tolerance")
        
        # Traffic vs Budget conflicts (high traffic usually means higher costs)
        if (constraints.expected_traffic == ConstraintLevel.HIGH and 
            constraints.budget_sensitivity == ConstraintLevel.HIGH):
            conflicts.append("Expected traffic vs Budget sensitivity")
        
        return conflicts
    
    def get_trade_off_summary(self, analysis: TradeOffAnalysis) -> Dict[str, any]:
        """Get a summary of the trade-off analysis."""
        return {
            'cost_control_analysis_length': len(analysis.cost_vs_control),
            'latency_ops_analysis_length': len(analysis.latency_vs_ops_complexity),
            'edge_cases_identified': len(analysis.edge_case_warnings),
            'conflicts_identified': len(analysis.conflicting_constraints),
            'has_cost_analysis': bool(analysis.cost_vs_control),
            'has_latency_analysis': bool(analysis.latency_vs_ops_complexity)
        }