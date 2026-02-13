"""xltekhdf5.py
A HDF5 file which contains data for XLTEK EEG data.
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

# Third-Party Packages #
from classversioning import TriNumberVersion
from classversioning import Version
from dspobjects.time import Timestamp, nanostamp

# Local Packages #
from .xltekhdf5 import XLTEKHDF5


# Definitions #
# Classes #
class XLTEKHDF5_1(XLTEKHDF5):
    """A HDF5 file which contains data for XLTEK EEG data.

    Class Attributes:
        _registration: Determines if this class will be included in class registry.
        _VERSION_TYPE: The type of versioning to use.
        FILE_TYPE: The file type name of this class.
        VERSION: The version of this class.
        default_map: The HDF5 map of this object.
    """

    VERSION: Version = TriNumberVersion(1, 0, 0)

    @property
    def end_datetime(self) -> Timestamp | None:
        """The end datetime of this file."""
        return self["data"].components["timeseries"].get_datetime(-1)

    @property
    def end_nanostamp(self) -> int | None:
        """The end timestamp of this file."""
        return self["data"].components["timeseries"].get_nanostamp(-1)

    @property
    def end_timestamp(self) -> float | None:
        """The end timestamp of this file."""
        return self["data"].components["timeseries"].get_timestamp(-1)

    @property
    def start_id(self) -> int:
        """The start ID of this file."""
        return int(self.attributes.get("start_id", None))

    @property
    def end_id(self) -> int:
        """The end ID of this file."""
        data = self["data"]
        if data.components["timeseries"].sample_rate is None:
            end_id = self.attributes.get("end_id", None)
        else:
            start_id = self.start_id
            if start_id is None:
                return None
            end_id = start_id + nanostamp((data.shape[0] - 1) / data.components["timeseries"].sample_rate)
        return int(end_id)

