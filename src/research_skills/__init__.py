"""Academic Research Skills - Core Package.

This package provides tools and utilities for developing and assessing
academic research skills, including literature review, citation management,
critical analysis, and research methodology guidance.

Note: Personal fork for learning purposes. Using this to practice
literature review workflows for my thesis research.

Personal customizations:
- Added __email__ field for contact info
- Exposed __version__ more prominently for debugging
- Added __email__ to __all__ for consistency
- Fixed: __email__ was missing from __all__ despite being a public attribute
"""

__version__ = "0.1.0"
__author__ = "academic-research-skills contributors"
__license__ = "MIT"
__email__ = ""  # personal contact placeholder

from .core import ResearchSkillsManager
from .assessments import SkillAssessment
from .resources import ResourceLibrary

__all__ = [
    "ResearchSkillsManager",
    "SkillAssessment",
    "ResourceLibrary",
    "__version__",
    "__author__",
    "__email__",
]
