"""xltekvideomaps.py

"""
# Package Header #
from ....header import *


# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #

# Third-Party Packages #

# Local Packages #
from cdfs.contentsfile import TimeContentGroupComponent
from cdfs.contentsfile import TimeContentGroupMap


# Local Packages #


# Definitions #
# Classes #
class XLTEKVideoDayGroupMap(TimeContentGroupMap):
    """A group map which outlines a group with basic node methods."""

    default_attributes = {"tree_type": "Leaf"}
    default_component_types = {
        "tree_node": (TimeContentGroupComponent, {"insert_method": "insert_recursive_entry_start"}),
    }


class XLTEKVideoContentGroupMap(TimeContentGroupMap):
    """A group map which outlines a group with basic node methods."""

    default_attributes = {"tree_type": "Node"}
    default_component_types = {
        "tree_node": (
            TimeContentGroupComponent,
            {"insert_method": "insert_recursive_entry_start_date", "child_map_type": XLTEKVideoDayGroupMap},
        ),
    }