"""
Unit tests for Kiro directory structure and artifacts.
"""
import pytest
import os
from pathlib import Path


class TestKiroDirectoryStructure:
    """Test Kiro directory structure and required files."""
    
    def test_kiro_directory_exists(self):
        """
        Test that .kiro directory exists at repository root.
        Validates: Requirements 8.1
        """
        kiro_dir = Path(".kiro")
        assert kiro_dir.exists(), ".kiro directory should exist at repository root"
        assert kiro_dir.is_dir(), ".kiro should be a directory"
    
    def test_prompts_directory_exists(self):
        """Test that .kiro/prompts directory exists."""
        prompts_dir = Path(".kiro/prompts")
        assert prompts_dir.exists(), ".kiro/prompts directory should exist"
        assert prompts_dir.is_dir(), ".kiro/prompts should be a directory"
    
    def test_notes_directory_exists(self):
        """Test that .kiro/notes directory exists."""
        notes_dir = Path(".kiro/notes")
        assert notes_dir.exists(), ".kiro/notes directory should exist"
        assert notes_dir.is_dir(), ".kiro/notes should be a directory"
    
    def test_prompt_specification_files_exist(self):
        """
        Test that all required prompt files exist.
        Validates: Requirements 8.2
        """
        required_prompt_files = [
            ".kiro/prompts/specification.md",
            ".kiro/prompts/scoring_rules.md",
            ".kiro/prompts/tradeoff_templates.md"
        ]
        
        for file_path in required_prompt_files:
            file_obj = Path(file_path)
            assert file_obj.exists(), f"Required prompt file {file_path} should exist"
            assert file_obj.is_file(), f"{file_path} should be a file"
            
            # Verify file is not empty
            assert file_obj.stat().st_size > 0, f"{file_path} should not be empty"
    
    def test_explanation_templates_exist(self):
        """
        Test that explanation template files exist.
        Validates: Requirements 8.3
        """
        template_file = Path(".kiro/prompts/tradeoff_templates.md")
        assert template_file.exists(), "Trade-off templates file should exist"
        assert template_file.is_file(), "Trade-off templates should be a file"
        
        # Verify content contains required phrases
        content = template_file.read_text(encoding='utf-8')
        required_phrases = [
            "This is a good choice when",
            "This may be a limitation if",
            "The trade-off here is"
        ]
        
        for phrase in required_phrases:
            assert phrase in content, f"Template file should contain required phrase: {phrase}"
    
    def test_kiro_reasoning_artifacts_exist(self):
        """
        Test that Kiro-generated reasoning artifacts exist.
        Validates: Requirements 8.4
        """
        reasoning_file = Path(".kiro/notes/kiro_iterations.md")
        assert reasoning_file.exists(), "Kiro reasoning artifacts file should exist"
        assert reasoning_file.is_file(), "Kiro reasoning artifacts should be a file"
        
        # Verify file is not empty
        assert reasoning_file.stat().st_size > 0, "Reasoning artifacts file should not be empty"
    
    def test_specification_file_content(self):
        """Test that specification file contains required content."""
        spec_file = Path(".kiro/prompts/specification.md")
        content = spec_file.read_text(encoding='utf-8')
        
        # Should contain project objective
        assert "Project Objective" in content
        
        # Should contain all three services
        assert "EC2" in content
        assert "Lambda" in content
        assert "Fargate" in content
        
        # Should contain core principles
        assert "Neutral" in content or "neutral" in content
        assert "Educational" in content or "educational" in content
        
        # Should contain constraint dimensions
        assert "Budget sensitivity" in content or "budget" in content.lower()
        assert "Traffic" in content or "traffic" in content.lower()
        assert "Scalability" in content or "scalability" in content.lower()
        assert "Latency" in content or "latency" in content.lower()
        assert "Operational" in content or "operational" in content.lower()
        assert "Time" in content or "time" in content.lower()
    
    def test_scoring_rules_file_content(self):
        """Test that scoring rules file contains required content."""
        scoring_file = Path(".kiro/prompts/scoring_rules.md")
        content = scoring_file.read_text(encoding='utf-8')
        
        # Should contain scoring scale
        assert "1-5" in content or "1:" in content
        
        # Should contain all services
        assert "EC2" in content
        assert "Lambda" in content
        assert "Fargate" in content
        
        # Should contain all constraint types
        constraints = [
            "Budget Sensitivity", "Expected Traffic", "Scalability Requirement",
            "Latency Sensitivity", "Operational Overhead", "Time-to-Market"
        ]
        
        for constraint in constraints:
            # Check for constraint or similar wording
            assert (constraint in content or 
                   constraint.lower() in content.lower() or
                   constraint.replace(" ", "").lower() in content.lower()), \
                   f"Scoring rules should contain {constraint}"
        
        # Should contain scoring rationale
        assert "rationale" in content.lower() or "based on" in content.lower()
    
    def test_kiro_iterations_file_content(self):
        """Test that Kiro iterations file contains development reasoning."""
        iterations_file = Path(".kiro/notes/kiro_iterations.md")
        content = iterations_file.read_text(encoding='utf-8')
        
        # Should contain development insights
        assert len(content) > 100, "Iterations file should contain substantial content"
        
        # Should mention key design decisions
        assert ("design" in content.lower() or 
               "decision" in content.lower() or
               "approach" in content.lower()), "Should contain design reasoning"
        
        # Should mention AWS services
        assert ("AWS" in content or "EC2" in content or 
               "Lambda" in content or "Fargate" in content), "Should mention AWS services"
    
    def test_repository_structure_maintainability(self):
        """
        Test that repository structure supports maintainability and documentation.
        Validates: Requirements 8.5
        """
        # Check that we have a clear structure
        required_dirs = [".kiro", ".kiro/prompts", ".kiro/notes"]
        
        for dir_path in required_dirs:
            dir_obj = Path(dir_path)
            assert dir_obj.exists(), f"Required directory {dir_path} should exist"
            assert dir_obj.is_dir(), f"{dir_path} should be a directory"
        
        # Check that we have documentation files
        doc_files = [
            ".kiro/prompts/specification.md",
            ".kiro/prompts/scoring_rules.md", 
            ".kiro/prompts/tradeoff_templates.md",
            ".kiro/notes/kiro_iterations.md"
        ]
        
        for file_path in doc_files:
            file_obj = Path(file_path)
            assert file_obj.exists(), f"Documentation file {file_path} should exist"
            
            # Files should be readable
            try:
                content = file_obj.read_text(encoding='utf-8')
                assert len(content) > 0, f"{file_path} should not be empty"
            except Exception as e:
                pytest.fail(f"Could not read {file_path}: {e}")
    
    def test_file_permissions_and_accessibility(self):
        """Test that all Kiro files are accessible and readable."""
        kiro_files = [
            ".kiro/prompts/specification.md",
            ".kiro/prompts/scoring_rules.md",
            ".kiro/prompts/tradeoff_templates.md", 
            ".kiro/notes/kiro_iterations.md"
        ]
        
        for file_path in kiro_files:
            file_obj = Path(file_path)
            
            # File should be readable
            assert os.access(file_obj, os.R_OK), f"{file_path} should be readable"
            
            # File should have content
            assert file_obj.stat().st_size > 0, f"{file_path} should not be empty"
            
            # Should be able to read as text
            try:
                content = file_obj.read_text(encoding='utf-8')
                assert isinstance(content, str), f"{file_path} should contain valid text"
            except UnicodeDecodeError:
                pytest.fail(f"{file_path} contains invalid UTF-8 encoding")