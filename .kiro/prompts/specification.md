# Cloud Service Referee - Project Specification

## Project Objective

Build a Python + Streamlit application that helps users choose between AWS compute services (EC2, Lambda, ECS Fargate) based on user-defined constraints. The tool must behave like a neutral referee, not an optimizer.

## Core Principles

- **Neutral Analysis**: No single "best" service declared
- **Educational Focus**: Transparent trade-off explanations
- **Independent Evaluation**: Each service evaluated separately
- **Constraint-Based**: Six dimensions of user requirements
- **Plain English**: Clear, analytical explanations

## Services to Compare

- AWS EC2 (Elastic Compute Cloud)
- AWS Lambda (Serverless Functions)
- AWS ECS Fargate (Serverless Containers)

## User Input Constraints

1. Budget sensitivity: Low / Medium / High
2. Expected traffic: Low / Medium / High
3. Scalability requirement: Low / Medium / High
4. Latency sensitivity: Low / Medium / High
5. Operational overhead tolerance: Low / Medium / High
6. Time-to-market urgency: Low / Medium / High

## Output Requirements

- Side-by-side comparison table
- Constraint-wise scores per service (1-5 scale)
- Clear pros and cons for each service
- Trade-off explanations in plain English
- Contextual recommendations (when to choose each service)

## Required Language Patterns

- "This is a good choice when..."
- "This may be a limitation if..."
- "The trade-off here is..."

## Edge Cases to Handle

- Low budget + high scalability
- High latency sensitivity + high traffic
- Fast time-to-market + low operational tolerance