"""
Service repository containing AWS service characteristics and data.
"""
from typing import Dict, List
from .models import ServiceCharacteristics, ServiceType
from .interfaces import ServiceRepositoryInterface


class ServiceRepository(ServiceRepositoryInterface):
    """Repository for AWS service characteristics and data."""
    
    def __init__(self):
        """Initialize the service repository with AWS service data."""
        self._services = self._initialize_services()
    
    def _initialize_services(self) -> Dict[str, ServiceCharacteristics]:
        """Initialize service characteristics based on research."""
        return {
            ServiceType.EC2.value: ServiceCharacteristics(
                name="AWS EC2",
                strengths=[
                    "Full control over infrastructure and OS",
                    "Cost optimization potential with reserved instances",
                    "Performance tuning capabilities",
                    "Support for specialized hardware (GPU, high-memory)",
                    "No vendor lock-in for application code",
                    "Mature ecosystem and tooling"
                ],
                limitations=[
                    "High operational overhead (patching, monitoring, scaling)",
                    "Slower provisioning and scaling compared to serverless",
                    "Requires infrastructure expertise",
                    "Manual capacity planning needed",
                    "Responsibility for security and maintenance"
                ],
                best_use_cases=[
                    "Legacy systems requiring specific OS configurations",
                    "Applications needing specialized hardware",
                    "Long-running, predictable workloads",
                    "Teams with strong infrastructure capabilities",
                    "Cost-sensitive applications with predictable usage"
                ],
                cost_model="Pay for compute time, potential savings with reserved instances",
                scaling_characteristics="Manual or auto-scaling, slower response time",
                operational_overhead="High - full infrastructure management required"
            ),
            
            ServiceType.LAMBDA.value: ServiceCharacteristics(
                name="AWS Lambda",
                strengths=[
                    "Zero infrastructure management",
                    "Automatic scaling from zero to thousands",
                    "Pay only for actual execution time",
                    "Fast prototyping and development",
                    "Built-in high availability",
                    "Event-driven architecture support"
                ],
                limitations=[
                    "Cold start latency (100-800ms for most runtimes)",
                    "15-minute maximum execution time",
                    "Vendor lock-in with AWS-specific APIs",
                    "Cost can scale unpredictably with high usage",
                    "Limited runtime environment control",
                    "Debugging complexity in distributed systems"
                ],
                best_use_cases=[
                    "Event-driven processing (S3, DynamoDB triggers)",
                    "Low-traffic web APIs and microservices",
                    "Scheduled tasks and cron jobs",
                    "Rapid prototyping and MVPs",
                    "Teams wanting zero infrastructure management"
                ],
                cost_model="Pay per request and execution time, can become expensive at scale",
                scaling_characteristics="Instant automatic scaling, handles traffic spikes well",
                operational_overhead="Very low - AWS manages all infrastructure"
            ),
            
            ServiceType.ECS_FARGATE.value: ServiceCharacteristics(
                name="AWS ECS Fargate",
                strengths=[
                    "Container benefits without cluster management",
                    "Faster provisioning than EC2",
                    "No server management required",
                    "Good for microservices architecture",
                    "Integrated with AWS ecosystem",
                    "Predictable pricing model"
                ],
                limitations=[
                    "Higher per-unit cost than EC2",
                    "Limited runtime control compared to EC2",
                    "No support for spot instances",
                    "Less flexibility than self-managed containers",
                    "Still requires container expertise",
                    "Slower cold starts than Lambda"
                ],
                best_use_cases=[
                    "Containerized web applications",
                    "Microservices without Kubernetes complexity",
                    "Teams familiar with containers but not infrastructure",
                    "Applications requiring more control than Lambda",
                    "Batch processing jobs"
                ],
                cost_model="Pay for allocated CPU and memory, higher than EC2 per unit",
                scaling_characteristics="Automatic scaling, faster than EC2 but slower than Lambda",
                operational_overhead="Medium - container management without server management"
            )
        }
    
    def get_service_characteristics(self, service: str) -> ServiceCharacteristics:
        """Get characteristics for a specific service."""
        if service not in self._services:
            raise ValueError(f"Unknown service: {service}")
        return self._services[service]
    
    def get_all_services(self) -> List[str]:
        """Get list of all available services."""
        return list(self._services.keys())
    
    def get_service_names(self) -> List[str]:
        """Get human-readable service names."""
        return [service.name for service in self._services.values()]