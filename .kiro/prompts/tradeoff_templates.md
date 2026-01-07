# Trade-off Explanation Templates

## Required Language Patterns

All explanations must include these neutral, analytical phrases:
- "This is a good choice when..."
- "This may be a limitation if..."
- "The trade-off here is..."

## Service Recommendation Templates

### AWS EC2 Templates

**High Control Scenarios:**
"EC2 is a good choice when you need full infrastructure control, specialized hardware, or want to optimize costs through reserved instances. This may be a limitation if your team lacks infrastructure expertise or prefers hands-off management. The trade-off here is between maximum flexibility and operational complexity."

**Cost Optimization Scenarios:**
"EC2 is a good choice when budget optimization is critical and you can commit to reserved instances or spot instances. This may be a limitation if you need rapid scaling or lack the expertise to manage infrastructure efficiently. The trade-off here is between cost control and operational overhead."

**Performance Scenarios:**
"EC2 is a good choice when consistent, predictable performance is required without cold starts. This may be a limitation if you want zero infrastructure management or rapid deployment capabilities. The trade-off here is between performance guarantees and operational simplicity."

### AWS Lambda Templates

**Rapid Development Scenarios:**
"Lambda is a good choice when you need rapid prototyping, have event-driven workloads, or want zero infrastructure management. This may be a limitation if you require predictable costs at scale or have latency-sensitive applications. The trade-off here is between development speed and performance predictability."

**Low Traffic Scenarios:**
"Lambda is a good choice when traffic is low or highly variable, as you pay only for actual usage. This may be a limitation if you have sustained high traffic, as costs can become significant. The trade-off here is between pay-per-use efficiency and cost predictability at scale."

**Serverless Architecture Scenarios:**
"Lambda is a good choice when you want to focus purely on business logic without infrastructure concerns. This may be a limitation if you need fine-grained control over the runtime environment or have strict latency requirements. The trade-off here is between operational simplicity and environmental control."

### AWS ECS Fargate Templates

**Container Scenarios:**
"ECS Fargate is a good choice when you want container benefits without managing Kubernetes or EC2 instances. This may be a limitation if cost optimization is critical, as Fargate has higher per-unit costs than EC2. The trade-off here is between container convenience and cost efficiency."

**Balanced Control Scenarios:**
"ECS Fargate is a good choice when you need more control than Lambda but less operational overhead than EC2. This may be a limitation if you need the absolute lowest costs or maximum infrastructure control. The trade-off here is between balanced functionality and specialized optimization."

**Microservices Scenarios:**
"ECS Fargate is a good choice when building containerized microservices without Kubernetes complexity. This may be a limitation if you need spot instance pricing or custom OS configurations. The trade-off here is between container orchestration simplicity and infrastructure flexibility."

## Constraint-Specific Templates

### Budget Sensitivity Templates

**High Budget Sensitivity:**
"With high budget sensitivity, the trade-off here is between cost optimization and other capabilities. EC2 offers the best cost control through reserved instances, but requires operational investment. Lambda can become expensive at scale. Fargate has the highest per-unit costs but predictable pricing."

**Low Budget Sensitivity:**
"With low budget sensitivity, the trade-off here shifts toward operational efficiency and development speed. This is a good choice when you can prioritize convenience over cost optimization, allowing focus on features rather than infrastructure management."

### Latency Sensitivity Templates

**High Latency Sensitivity:**
"With high latency sensitivity, the trade-off here is between performance consistency and operational complexity. EC2 provides the most predictable performance but requires significant management. Lambda's cold starts may be a limitation if consistent low latency is critical."

**Low Latency Sensitivity:**
"With low latency sensitivity, the trade-off here favors operational simplicity over performance optimization. This is a good choice when occasional latency spikes are acceptable in exchange for reduced infrastructure management."

### Scalability Templates

**High Scalability Requirements:**
"With high scalability requirements, the trade-off here is between automatic scaling capabilities and cost control. Lambda excels at instant scaling but costs can become unpredictable. EC2 requires more configuration but offers better cost optimization at scale."

**Low Scalability Requirements:**
"With low scalability requirements, the trade-off here is between simplicity and potential over-provisioning. This is a good choice when consistent, predictable capacity is more important than dynamic scaling capabilities."

## Edge Case Templates

### Budget vs Performance Conflict
"This constraint combination creates tension between cost optimization and performance requirements. The trade-off here is between accepting higher costs for better performance or accepting performance limitations for cost control. This may be a limitation if both constraints are equally critical."

### Speed vs Control Conflict
"This constraint combination aligns toward serverless solutions that prioritize rapid deployment over infrastructure control. This is a good choice when time-to-market is the primary concern, though it may limit long-term optimization opportunities."

### Scale vs Budget Conflict
"This constraint combination creates inherent tension between scaling capabilities and cost control. The trade-off here is between accepting higher costs for better scaling or implementing more complex cost optimization strategies. This may be a limitation if both requirements are non-negotiable."