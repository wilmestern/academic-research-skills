"""Academic Research Skills - Core Package.

This package provides tools and utilities for developing and assessing
academic research skills, including literature review, citation management,
critical analysis, and research methodology guidance.

Note: Personal fork for learning purposes. Using this to practice
literature review workflows for my thesis research.
"""

__version__ = "0.1.0"
__author__ = "academic-research-skills contributors"
__license__ = "MIT"

from .core import ResearchSkillsManager
from .assessments import SkillAssessment
from .resources import ResourceLibrary

__all__ = [
    "ResearchSkillsManager",
    "SkillAssessment",
    "ResourceLibrary",
    "__version__",
]
