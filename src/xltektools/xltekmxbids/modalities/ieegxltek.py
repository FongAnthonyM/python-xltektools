"""IEEGXLTEK.py
A BIDS IEEG XLTEK Modality.
"""
# Header #
__package_name__ = "xltektools"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2022, Anthony Fong"
__license__ = "MIT"

__version__ = "0.6.0"


# Imports #
# Standard Libraries #
from typing import ClassVar, Any

# Third-Party Packages #
from mxbids.cdfsbids import IEEGCDFS

# Local Packages #
from .ieegxltekcomponent import IEEGXLTEKComponent
from .ieegxltekannotationscomponent import IEEGXLTEKAnnotationsComponent


# Definitions #
# Classes #
class IEEGXLTEK(IEEGCDFS):
    """A BIDS IEEG XLTEK Modality.

    Class Attributes:
        _module_: The module name for this class.
        default_component_types: Default component types for the modality.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = "xltektools.xltekmxbids"
    default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
        "cdfs": (IEEGXLTEKComponent, {}),
        "annotations": (IEEGXLTEKAnnotationsComponent, {}),
    }
