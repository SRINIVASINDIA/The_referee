"""
Cloud Service Referee - Main Streamlit Application

A neutral, educational tool for comparing AWS compute services (EC2, Lambda, ECS Fargate)
based on user-defined constraints. Acts as an impartial referee rather than an optimizer.
"""
import streamlit as st
import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.service_repository import ServiceRepository
from src.scoring_system import ScoringSystem
from src.constraint_evaluator import ConstraintEvaluator
from src.trade_off_analyzer import TradeOffAnalyzer
from src.explanation_generator import ExplanationGenerator
from src.comparison_engine import ComparisonEngine
from src.ui_controller import UIController


def initialize_components():
    """Initialize all application components."""
    # Initialize core components
    service_repo = ServiceRepository()
    scoring_system = ScoringSystem()
    constraint_evaluator = ConstraintEvaluator(scoring_system, service_repo)
    trade_off_analyzer = TradeOffAnalyzer()
    explanation_generator = ExplanationGenerator()
    
    # Initialize comparison engine
    comparison_engine = ComparisonEngine(
        constraint_evaluator=constraint_evaluator,
        trade_off_analyzer=trade_off_analyzer,
        explanation_generator=explanation_generator
    )
    
    # Initialize UI controller
    ui_controller = UIController()
    
    return comparison_engine, ui_controller


def main():
    """Main application entry point."""
    # Configure Streamlit page
    st.set_page_config(
        page_title="Cloud Service Referee",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize components
    try:
        comparison_engine, ui_controller = initialize_components()
    except Exception as e:
        st.error(f"Failed to initialize application components: {str(e)}")
        st.stop()
    
    # Render constraint inputs
    try:
        constraint_inputs = ui_controller.render_constraint_inputs()
    except Exception as e:
        st.error(f"Failed to render constraint inputs: {str(e)}")
        st.stop()
    
    # Add comparison button
    if st.button("🔍 Compare Services", type="primary", use_container_width=True):
        try:
            # Validate inputs
            if not ui_controller.validate_constraint_inputs(constraint_inputs):
                ui_controller.display_error_message("Invalid constraint inputs. Please check your selections.")
                st.stop()
            
            # Convert inputs to UserConstraints object
            user_constraints = ui_controller.create_user_constraints_from_input(constraint_inputs)
            
            # Show processing message
            with st.spinner("Analyzing services and generating recommendations..."):
                # Perform comparison
                comparison_result = comparison_engine.compare_services(user_constraints)
            
            # Display results
            ui_controller.display_comparison_results(comparison_result)
            
            # Show success message
            ui_controller.display_success_message("Service comparison completed successfully!")
            
        except Exception as e:
            ui_controller.display_error_message(f"Comparison failed: {str(e)}")
            
            # Show debug information in development
            if st.secrets.get("debug_mode", False):
                st.exception(e)
    
    # Add footer with information
    st.markdown("---")
    st.markdown("""
    ### About Cloud Service Referee
    
    This tool provides **neutral, educational comparisons** of AWS compute services. Rather than 
    declaring a single "best" choice, it explains trade-offs and helps you understand when each 
    service is most appropriate for your specific constraints.
    
    **Key Features:**
    - 🎯 **Neutral Analysis**: No service is favored over others
    - 📚 **Educational Focus**: Learn about trade-offs and implications
    - ⚖️ **Independent Evaluation**: Each service evaluated separately
    - 🔍 **Constraint-Based**: Six dimensions of requirements analysis
    - 💬 **Plain English**: Clear, analytical explanations
    
    **Services Compared:**
    - **AWS EC2**: Full infrastructure control with operational complexity
    - **AWS Lambda**: Serverless simplicity with performance trade-offs  
    - **AWS ECS Fargate**: Container convenience with cost implications
    """)


if __name__ == "__main__":
    main()