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
- Added __license__ to __all__ for completeness
- Added __description__ for quick package identification in debug sessions
"""

__version__ = "0.1.0"
__author__ = "academic-research-skills contributors"
__license__ = "MIT"
__email__ = ""  # personal contact placeholder
__description__ = "Tools for developing and assessing academic research skills"

from .core import ResearchSkillsManager
from .assessments import SkillAssessment
from .resources import ResourceLibrary

__all__ = [
    "ResearchSkillsManager",
    "SkillAssessment",
    "ResourceLibrary",
    "__version__",
    "__author__",
    "__license__",  # added: useful to expose for downstream consumers
    "__email__",
    "__description__",  # added: handy for quick identification when debugging imports
]
