"""
Explanation generator component for creating contextual recommendations.
"""
from typing import Dict
from .models import UserConstraints, ServiceEvaluation, TradeOffAnalysis, ConstraintLevel, ServiceType
from .interfaces import ExplanationGeneratorInterface


class ExplanationGenerator(ExplanationGeneratorInterface):
    """Generates plain English explanations and contextual recommendations."""
    
    def __init__(self):
        """Initialize the explanation generator."""
        self.required_phrases = [
            "This is a good choice when",
            "This may be a limitation if", 
            "The trade-off here is"
        ]
    
    def generate_contextual_recommendations(
        self, 
        evaluations: Dict[str, ServiceEvaluation],
        constraints: UserConstraints
    ) -> Dict[str, str]:
        """Generate contextual recommendations for each service."""
        recommendations = {}
        
        for service_key, evaluation in evaluations.items():
            if service_key == ServiceType.EC2.value:
                recommendations[service_key] = self._generate_ec2_recommendation(evaluation, constraints)
            elif service_key == ServiceType.LAMBDA.value:
                recommendations[service_key] = self._generate_lambda_recommendation(evaluation, constraints)
            elif service_key == ServiceType.ECS_FARGATE.value:
                recommendations[service_key] = self._generate_fargate_recommendation(evaluation, constraints)
        
        return recommendations
    
    def _generate_ec2_recommendation(
        self, 
        evaluation: ServiceEvaluation, 
        constraints: UserConstraints
    ) -> str:
        """Generate contextual recommendation for EC2."""
        parts = []
        
        # Analyze constraint scores to determine primary use cases
        scores = evaluation.constraint_scores
        
        # Budget-focused recommendations
        if constraints.budget_sensitivity == ConstraintLevel.HIGH:
            parts.append(
                "EC2 is a good choice when budget optimization is critical and you can commit to "
                "reserved instances or spot instances for significant cost savings."
            )
        elif constraints.budget_sensitivity == ConstraintLevel.MEDIUM:
            parts.append(
                "EC2 is a good choice when you want balanced cost control with the flexibility "
                "to optimize through instance types and pricing models."
            )
        else:  # LOW budget sensitivity
            parts.append(
                "EC2 is a good choice when cost is not the primary concern and you can prioritize "
                "performance and control over cost optimization."
            )
        
        # Performance-focused recommendations
        if constraints.latency_sensitivity == ConstraintLevel.HIGH:
            parts.append(
                "This is a good choice when consistent, predictable performance is required without "
                "cold starts or provisioning delays."
            )
        elif constraints.latency_sensitivity == ConstraintLevel.MEDIUM:
            parts.append(
                "EC2 provides reliable performance for applications with moderate latency requirements."
            )
        
        # Operational overhead considerations
        if constraints.operational_overhead_tolerance == ConstraintLevel.HIGH:
            parts.append(
                "EC2 is a good choice when your team has strong infrastructure expertise and wants "
                "maximum control over the runtime environment."
            )
        elif constraints.operational_overhead_tolerance == ConstraintLevel.LOW:
            parts.append(
                "This may be a limitation if your team prefers hands-off infrastructure management "
                "or lacks expertise in server administration, monitoring, and scaling configuration."
            )
        
        # Time to market considerations
        if constraints.time_to_market_urgency == ConstraintLevel.HIGH:
            parts.append(
                "This may be a limitation if rapid deployment is critical, as EC2 requires more "
                "setup time and configuration compared to serverless options."
            )
        elif constraints.time_to_market_urgency == ConstraintLevel.MEDIUM:
            parts.append(
                "EC2 requires moderate setup time but provides long-term flexibility for evolving requirements."
            )
        
        # Traffic considerations
        if constraints.expected_traffic == ConstraintLevel.HIGH:
            parts.append(
                "EC2 is a good choice when you have high, consistent traffic that can benefit from "
                "dedicated resources and cost optimization at scale."
            )
        
        # Add trade-off analysis
        parts.append(
            "The trade-off here is between maximum infrastructure control and operational complexity. "
            "EC2 provides the most flexibility but requires the highest operational investment."
        )
        
        return " ".join(parts)
    
    def _generate_lambda_recommendation(
        self, 
        evaluation: ServiceEvaluation, 
        constraints: UserConstraints
    ) -> str:
        """Generate contextual recommendation for Lambda."""
        parts = []
        
        scores = evaluation.constraint_scores
        
        # Operational overhead considerations
        if constraints.operational_overhead_tolerance == ConstraintLevel.LOW:
            parts.append(
                "Lambda is a good choice when you want zero infrastructure management and can "
                "focus purely on business logic without server concerns."
            )
        elif constraints.operational_overhead_tolerance == ConstraintLevel.MEDIUM:
            parts.append(
                "Lambda is a good choice when you prefer minimal operational overhead while "
                "maintaining some flexibility in your architecture."
            )
        
        # Time to market considerations
        if constraints.time_to_market_urgency == ConstraintLevel.HIGH:
            parts.append(
                "This is a good choice when rapid prototyping and deployment are priorities, "
                "allowing immediate focus on application development."
            )
        elif constraints.time_to_market_urgency == ConstraintLevel.MEDIUM:
            parts.append(
                "Lambda enables faster development cycles compared to traditional infrastructure approaches."
            )
        
        # Traffic considerations
        if constraints.expected_traffic == ConstraintLevel.LOW:
            parts.append(
                "Lambda is a good choice when traffic is low or highly variable, as you pay "
                "only for actual execution time with automatic scaling from zero."
            )
        elif constraints.expected_traffic == ConstraintLevel.MEDIUM:
            parts.append(
                "Lambda handles moderate traffic well with automatic scaling, though costs should be monitored."
            )
        elif constraints.expected_traffic == ConstraintLevel.HIGH:
            parts.append(
                "Lambda can handle high traffic but cost implications should be carefully evaluated."
            )
        
        # Latency considerations
        if constraints.latency_sensitivity == ConstraintLevel.HIGH:
            parts.append(
                "This may be a limitation if consistent low latency is critical, as Lambda "
                "cold starts can introduce 100-800ms delays for new execution environments."
            )
        elif constraints.latency_sensitivity == ConstraintLevel.MEDIUM:
            parts.append(
                "Lambda's occasional cold starts may be acceptable for applications with moderate latency requirements."
            )
        
        # Budget considerations
        if constraints.budget_sensitivity == ConstraintLevel.HIGH and constraints.expected_traffic == ConstraintLevel.HIGH:
            parts.append(
                "This may be a limitation if you have sustained high traffic with tight budget "
                "constraints, as Lambda costs can become significant at scale."
            )
        elif constraints.budget_sensitivity == ConstraintLevel.HIGH:
            parts.append(
                "Lambda can be cost-effective for variable workloads but requires monitoring to avoid unexpected costs."
            )
        
        # Add trade-off analysis
        parts.append(
            "The trade-off here is between operational simplicity and performance predictability. "
            "Lambda eliminates infrastructure concerns but introduces cold start latency and "
            "potential cost scaling challenges."
        )
        
        return " ".join(parts)
    
    def _generate_fargate_recommendation(
        self, 
        evaluation: ServiceEvaluation, 
        constraints: UserConstraints
    ) -> str:
        """Generate contextual recommendation for ECS Fargate."""
        parts = []
        
        scores = evaluation.constraint_scores
        
        parts.append(
            "ECS Fargate is a good choice when you want container benefits without managing "
            "Kubernetes clusters or EC2 instances, providing a middle ground between control and convenience."
        )
        
        if constraints.scalability_requirement == ConstraintLevel.HIGH:
            parts.append(
                "This is a good choice when you need automatic container scaling without the "
                "complexity of cluster management or the limitations of Lambda's execution model."
            )
        
        if (constraints.operational_overhead_tolerance == ConstraintLevel.MEDIUM and 
            constraints.time_to_market_urgency == ConstraintLevel.MEDIUM):
            parts.append(
                "Fargate is a good choice when you want more control than Lambda but less "
                "operational overhead than EC2, especially for containerized microservices."
            )
        
        # Add limitations
        if constraints.budget_sensitivity == ConstraintLevel.HIGH:
            parts.append(
                "This may be a limitation if cost optimization is critical, as Fargate has "
                "higher per-unit costs than EC2 and doesn't support spot instance pricing."
            )
        
        if constraints.operational_overhead_tolerance == ConstraintLevel.HIGH:
            parts.append(
                "This may be a limitation if you want maximum infrastructure control or need "
                "custom OS configurations that aren't available in the managed container environment."
            )
        
        # Add trade-off analysis
        parts.append(
            "The trade-off here is between container convenience and cost efficiency. "
            "Fargate simplifies container orchestration but at a premium compared to "
            "self-managed EC2 instances."
        )
        
        return " ".join(parts)
    
    def generate_trade_off_explanations(
        self, 
        analysis: TradeOffAnalysis
    ) -> Dict[str, str]:
        """Generate plain English trade-off explanations."""
        explanations = {
            'cost_vs_control': analysis.cost_vs_control,
            'latency_vs_ops_complexity': analysis.latency_vs_ops_complexity,
            'edge_case_summary': self._summarize_edge_cases(analysis.edge_case_warnings),
            'conflict_summary': self._summarize_conflicts(analysis.conflicting_constraints)
        }
        
        return explanations
    
    def _summarize_edge_cases(self, edge_case_warnings: list) -> str:
        """Summarize edge case warnings."""
        if not edge_case_warnings:
            return "No significant edge cases detected with the current constraint combination."
        
        summary_parts = ["Edge cases identified: "]
        for warning in edge_case_warnings:
            summary_parts.append(warning)
        
        return " ".join(summary_parts)
    
    def _summarize_conflicts(self, conflicting_constraints: list) -> str:
        """Summarize conflicting constraints."""
        if not conflicting_constraints:
            return "No major constraint conflicts detected."
        
        summary = f"Conflicting constraints detected: {', '.join(conflicting_constraints)}. "
        summary += "The trade-off here is between competing priorities that may require compromise or careful architecture decisions."
        
        return summary
    
    def validate_required_phrases(self, text: str) -> bool:
        """Validate that text contains at least one required phrase."""
        text_lower = text.lower()
        return any(phrase.lower() in text_lower for phrase in self.required_phrases)
    
    def get_phrase_usage_stats(self, recommendations: Dict[str, str]) -> Dict[str, int]:
        """Get statistics on required phrase usage across recommendations."""
        stats = {phrase: 0 for phrase in self.required_phrases}
        
        for recommendation in recommendations.values():
            recommendation_lower = recommendation.lower()
            for phrase in self.required_phrases:
                if phrase.lower() in recommendation_lower:
                    stats[phrase] += 1
        
        return stats