# Cloud Service Referee 🏛️

A neutral, educational tool for comparing AWS compute services (EC2, Lambda, ECS Fargate) based on user-defined constraints. Acts as an impartial referee rather than an optimizer.

## Overview

The Cloud Service Referee helps you make informed decisions about AWS compute services by providing transparent trade-off explanations rather than declaring a single "best" choice. It evaluates each service independently against your specific constraints and explains when each service is most appropriate.

## Key Features

- 🎯 **Neutral Analysis**: No service is favored over others
- 📚 **Educational Focus**: Learn about trade-offs and implications  
- ⚖️ **Independent Evaluation**: Each service evaluated separately
- 🔍 **Constraint-Based**: Six dimensions of requirements analysis
- 💬 **Plain English**: Clear, analytical explanations

## Services Compared

- **AWS EC2**: Full infrastructure control with operational complexity
- **AWS Lambda**: Serverless simplicity with performance trade-offs
- **AWS ECS Fargate**: Container convenience with cost implications

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cloud-service-referee
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

### Test the Complete Workflow

```bash
python test_app_workflow.py
```

### Run Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_properties.py -v    # Property-based tests
pytest tests/test_edge_cases.py -v    # Edge case scenarios
pytest tests/test_ui_components.py -v # UI component tests
pytest tests/test_kiro_structure.py -v # Project structure tests
```

## How It Works

### 1. Define Your Constraints

Specify your requirements across six key dimensions:
- **Budget Sensitivity**: How important is cost optimization?
- **Expected Traffic**: What level of traffic do you expect?
- **Scalability Requirement**: How important is automatic scaling?
- **Latency Sensitivity**: How critical is low latency?
- **Operational Overhead Tolerance**: How much infrastructure management can you handle?
- **Time-to-Market Urgency**: How quickly do you need to deploy?

### 2. Get Independent Evaluations

Each service receives independent scores (1-5) for each constraint based on:
- Technical characteristics of the service
- Operational requirements for the constraint level
- Real-world trade-offs observed in practice
- Cost implications for different usage patterns
- Team capability requirements for successful implementation

### 3. Understand Trade-offs

The tool explains:
- **Cost vs Control**: Balance between cost optimization and infrastructure control
- **Latency vs Operational Complexity**: Performance consistency vs management overhead
- **Edge Cases**: Conflicting constraints and their implications
- **Contextual Recommendations**: When each service is most appropriate

## Example Output

For high budget sensitivity + high latency sensitivity + low operational tolerance:

**EC2**: "EC2 is a good choice when consistent, predictable performance is required without cold starts. This may be a limitation if your team prefers hands-off infrastructure management. The trade-off here is between maximum infrastructure control and operational complexity."

**Lambda**: "This may be a limitation if consistent low latency is critical, as Lambda cold starts can introduce 100-800ms delays. Lambda is a good choice when you want zero infrastructure management. The trade-off here is between operational simplicity and performance predictability."

**ECS Fargate**: "ECS Fargate is a good choice when you want container benefits without managing Kubernetes clusters. This may be a limitation if cost optimization is critical. The trade-off here is between container convenience and cost efficiency."

## Architecture

The application follows a modular architecture:

```
├── src/
│   ├── models.py              # Data models and enums
│   ├── interfaces.py          # Component interfaces
│   ├── service_repository.py  # AWS service characteristics
│   ├── scoring_system.py      # Rule-based scoring (1-5 scale)
│   ├── constraint_evaluator.py # Independent service evaluation
│   ├── trade_off_analyzer.py  # Trade-off identification
│   ├── explanation_generator.py # Plain English explanations
│   ├── comparison_engine.py   # Orchestrates comparison process
│   └── ui_controller.py       # Streamlit UI management
├── tests/                     # Comprehensive test suite
├── .kiro/                     # Project artifacts
│   ├── prompts/              # Specifications and templates
│   └── notes/                # Development reasoning
└── app.py                    # Main Streamlit application
```

## Testing

The project includes comprehensive testing:

- **Property-Based Tests**: 10 properties validating universal behaviors using Hypothesis
- **Unit Tests**: Specific scenarios, edge cases, and component validation
- **Integration Tests**: End-to-end workflow validation
- **Structure Tests**: Project organization and artifact validation

### Key Properties Tested

1. **Service Independence**: Each service evaluated independently
2. **Score Range Consistency**: All scores within 1-5 range
3. **No Winner Declaration**: No service declared as "best"
4. **Constraint Input Validation**: Only valid inputs accepted
5. **Required Phrase Inclusion**: Neutral language patterns maintained
6. **Trade-Off Identification**: Conflicting constraints detected
7. **Contextual Recommendation Variation**: Recommendations change with constraints
8. **Complete Scoring Coverage**: All constraint-service combinations covered
9. **System Robustness**: Handles all valid inputs without failure
10. **UI Responsiveness**: Interface updates when constraints change

## Project Structure

```
cloud-service-referee/
├── .kiro/
│   ├── prompts/
│   │   ├── specification.md      # Project specification
│   │   ├── scoring_rules.md      # Detailed scoring rules
│   │   └── tradeoff_templates.md # Explanation templates
│   └── notes/
│       └── kiro_iterations.md    # Development reasoning
├── src/                          # Source code
├── tests/                        # Test suite
├── app.py                        # Main application
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## Contributing

This project maintains strict neutrality principles:

1. **No Winner Declarations**: Never declare any service as "best" or "optimal"
2. **Independent Evaluation**: Each service must be evaluated separately
3. **Required Language Patterns**: Use "This is a good choice when...", "This may be a limitation if...", "The trade-off here is..."
4. **Comprehensive Testing**: All changes must pass property-based and unit tests
5. **Documentation**: Update reasoning artifacts for significant changes

## License

[Add your license information here]

## Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) for the web interface
- [Hypothesis](https://hypothesis.readthedocs.io/) for property-based testing
- [Pytest](https://pytest.org/) for the test framework