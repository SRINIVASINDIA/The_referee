"""
Streamlit UI controller for the Cloud Service Referee application.
"""
import streamlit as st
from typing import Dict
from .models import UserConstraints, ConstraintLevel, ComparisonResult
from .interfaces import UIControllerInterface


class UIController(UIControllerInterface):
    """Streamlit UI controller for managing user interactions."""
    
    def __init__(self):
        """Initialize the UI controller."""
        self.constraint_options = ["Low", "Medium", "High"]
        self.constraint_descriptions = {
            "budget_sensitivity": {
                "label": "Budget Sensitivity",
                "description": "How important is cost optimization?",
                "help": "Low: Cost is not a primary concern | Medium: Balanced cost considerations | High: Cost is a major constraint"
            },
            "expected_traffic": {
                "label": "Expected Traffic",
                "description": "What level of traffic do you expect?",
                "help": "Low: Minimal or sporadic traffic | Medium: Moderate, consistent traffic | High: Heavy, sustained traffic"
            },
            "scalability_requirement": {
                "label": "Scalability Requirement",
                "description": "How important is automatic scaling?",
                "help": "Low: Predictable capacity needs | Medium: Some scaling needed | High: Rapid, automatic scaling critical"
            },
            "latency_sensitivity": {
                "label": "Latency Sensitivity",
                "description": "How critical is low latency?",
                "help": "Low: Latency not critical | Medium: Some latency acceptable | High: Consistent low latency required"
            },
            "operational_overhead_tolerance": {
                "label": "Operational Overhead Tolerance",
                "description": "How much infrastructure management can you handle?",
                "help": "Low: Want minimal operational work | Medium: Some operational work acceptable | High: Comfortable with infrastructure management"
            },
            "time_to_market_urgency": {
                "label": "Time-to-Market Urgency",
                "description": "How quickly do you need to deploy?",
                "help": "Low: Time not critical | Medium: Moderate time pressure | High: Need to ship quickly"
            }
        }
    
    def render_constraint_inputs(self) -> Dict[str, str]:
        """Render constraint input controls and return values."""
        st.header("🏛️ Cloud Service Referee")
        st.subheader("Compare AWS Compute Services")
        
        st.markdown("""
        This tool helps you make informed decisions about AWS compute services by providing 
        neutral, educational comparisons. Rather than declaring a single "best" choice, 
        it explains trade-offs and helps you understand when each service is most appropriate.
        """)
        
        st.markdown("---")
        st.subheader("📊 Define Your Requirements")
        st.markdown("Please specify your project constraints:")
        
        # Create two columns for better layout
        col1, col2 = st.columns(2)
        
        constraints = {}
        
        with col1:
            # Budget Sensitivity
            desc = self.constraint_descriptions["budget_sensitivity"]
            constraints["budget_sensitivity"] = st.selectbox(
                desc["label"],
                self.constraint_options,
                index=1,  # Default to Medium
                help=desc["help"],
                key="budget_sensitivity"
            )
            
            # Expected Traffic
            desc = self.constraint_descriptions["expected_traffic"]
            constraints["expected_traffic"] = st.selectbox(
                desc["label"],
                self.constraint_options,
                index=1,  # Default to Medium
                help=desc["help"],
                key="expected_traffic"
            )
            
            # Scalability Requirement
            desc = self.constraint_descriptions["scalability_requirement"]
            constraints["scalability_requirement"] = st.selectbox(
                desc["label"],
                self.constraint_options,
                index=1,  # Default to Medium
                help=desc["help"],
                key="scalability_requirement"
            )
        
        with col2:
            # Latency Sensitivity
            desc = self.constraint_descriptions["latency_sensitivity"]
            constraints["latency_sensitivity"] = st.selectbox(
                desc["label"],
                self.constraint_options,
                index=1,  # Default to Medium
                help=desc["help"],
                key="latency_sensitivity"
            )
            
            # Operational Overhead Tolerance
            desc = self.constraint_descriptions["operational_overhead_tolerance"]
            constraints["operational_overhead_tolerance"] = st.selectbox(
                desc["label"],
                self.constraint_options,
                index=1,  # Default to Medium
                help=desc["help"],
                key="operational_overhead_tolerance"
            )
            
            # Time-to-Market Urgency
            desc = self.constraint_descriptions["time_to_market_urgency"]
            constraints["time_to_market_urgency"] = st.selectbox(
                desc["label"],
                self.constraint_options,
                index=1,  # Default to Medium
                help=desc["help"],
                key="time_to_market_urgency"
            )
        
        return constraints
    
    def display_comparison_results(self, results: ComparisonResult) -> None:
        """Display comparison results in the UI."""
        st.markdown("---")
        st.subheader("📋 Service Comparison Results")
        
        # Display service comparison table
        self.render_service_comparison_table(
            {service: eval.constraint_scores for service, eval in results.evaluations.items()}
        )
        
        # Display contextual recommendations
        st.markdown("---")
        st.subheader("💡 Contextual Recommendations")
        
        for service, recommendation in results.contextual_recommendations.items():
            service_eval = results.evaluations[service]
            
            with st.expander(f"🔍 {service_eval.service_name}", expanded=True):
                st.markdown(recommendation)
                
                # Show strengths and limitations
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Strengths:**")
                    for strength in service_eval.strengths[:3]:  # Show top 3
                        st.markdown(f"• {strength}")
                
                with col2:
                    st.markdown("**Limitations:**")
                    for limitation in service_eval.limitations[:3]:  # Show top 3
                        st.markdown(f"• {limitation}")
        
        # Display trade-off analysis
        if results.trade_off_analysis:
            st.markdown("---")
            st.subheader("⚖️ Trade-off Analysis")
            
            # Cost vs Control
            with st.expander("💰 Cost vs Control Trade-offs", expanded=False):
                st.markdown(results.trade_off_analysis.cost_vs_control)
            
            # Latency vs Operational Complexity
            with st.expander("⚡ Latency vs Operational Complexity", expanded=False):
                st.markdown(results.trade_off_analysis.latency_vs_ops_complexity)
        
        # Display edge case warnings
        if results.edge_case_warnings:
            st.markdown("---")
            st.subheader("⚠️ Edge Case Considerations")
            
            for warning in results.edge_case_warnings:
                st.warning(warning)
    
    def render_service_comparison_table(self, scores: Dict[str, Dict[str, int]]) -> None:
        """Render the service comparison table."""
        import pandas as pd
        
        # Prepare data for the table
        table_data = []
        constraint_names = [
            "Budget Sensitivity",
            "Expected Traffic", 
            "Scalability Requirement",
            "Latency Sensitivity",
            "Operational Overhead Tolerance",
            "Time-to-Market Urgency"
        ]
        
        constraint_keys = [
            "budget_sensitivity",
            "expected_traffic",
            "scalability_requirement", 
            "latency_sensitivity",
            "operational_overhead_tolerance",
            "time_to_market_urgency"
        ]
        
        for i, constraint_name in enumerate(constraint_names):
            constraint_key = constraint_keys[i]
            row = {"Constraint": constraint_name}
            
            for service, service_scores in scores.items():
                score = service_scores.get(constraint_key, 0)
                # Add emoji indicators for scores
                if score >= 4:
                    indicator = "🟢"
                elif score >= 3:
                    indicator = "🟡"
                else:
                    indicator = "🔴"
                row[service] = f"{score}/5 {indicator}"
            
            table_data.append(row)
        
        # Create and display the table
        df = pd.DataFrame(table_data)
        st.table(df.set_index("Constraint"))
        
        # Add legend
        st.markdown("""
        **Score Legend:** 🟢 Good fit (4-5) | 🟡 Average fit (3) | 🔴 Poor fit (1-2)
        """)
    
    def validate_constraint_inputs(self, constraints: Dict[str, str]) -> bool:
        """Validate that constraint inputs are valid."""
        required_constraints = [
            "budget_sensitivity", "expected_traffic", "scalability_requirement",
            "latency_sensitivity", "operational_overhead_tolerance", "time_to_market_urgency"
        ]
        
        # Check all constraints are present
        for constraint in required_constraints:
            if constraint not in constraints:
                return False
            
            # Check constraint value is valid
            if constraints[constraint] not in self.constraint_options:
                return False
        
        return True
    
    def create_user_constraints_from_input(self, constraints: Dict[str, str]) -> UserConstraints:
        """Create UserConstraints object from input dictionary."""
        return UserConstraints(
            budget_sensitivity=ConstraintLevel(constraints["budget_sensitivity"]),
            expected_traffic=ConstraintLevel(constraints["expected_traffic"]),
            scalability_requirement=ConstraintLevel(constraints["scalability_requirement"]),
            latency_sensitivity=ConstraintLevel(constraints["latency_sensitivity"]),
            operational_overhead_tolerance=ConstraintLevel(constraints["operational_overhead_tolerance"]),
            time_to_market_urgency=ConstraintLevel(constraints["time_to_market_urgency"])
        )
    
    def display_error_message(self, message: str) -> None:
        """Display an error message to the user."""
        st.error(f"❌ {message}")
    
    def display_info_message(self, message: str) -> None:
        """Display an info message to the user."""
        st.info(f"ℹ️ {message}")
    
    def display_success_message(self, message: str) -> None:
        """Display a success message to the user."""
        st.success(f"✅ {message}")