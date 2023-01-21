""" xltekdatagroupcomponent.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from typing import Any

# Third-Party Packages #
from dspobjects.time import Timestamp
from hdf5objects import HDF5Map, HDF5Dataset
from hdf5objects import HDF5BaseComponent

# Local Packages #


# Definitions #
# Classes #
class XLTEKDataGroupComponent(HDF5BaseComponent):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        composite: Any = None,
        day_map_type: type | None = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.subject_id: str = ""

        self.day_map_type: type | None = None
        self.date_format: str = "%Y-%m-%d"
        self.days_dataset_name = "days"
        self._days_dataset = None

        self.time_format: str = "%Y-%m-%d_%h~%m~%s"

        # Parent Attributes #
        super().__init__(self, init=False)

        # Object Construction #
        if init:
            self.construct(
                composite=composite,
                day_map_type=day_map_type,
                **kwargs,
            )

    @property
    def days_dataset(self) -> HDF5Dataset | None:
        """Loads and returns the id axis."""
        if self._days_dataset is None:
            self._days_dataset = self.composite[self.days_dataset_name]
        return self._days_dataset

    @days_dataset.setter
    def days_dataset(self, value: HDF5Dataset | None) -> None:
        self._days_dataset = value

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        composite: Any = None,
        day_map_type: type | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            composite: The object which this object is a component of.
            **kwargs: Keyword arguments for inheritance.
        """
        if day_map_type is not None:
            self.day_map_type = day_map_type

        super().construct(composite=composite, **kwargs)

    def create_day(self, start, end=None, name=None, path=None, length=0, map_=None, id_=None):
        if name is None:
            name = start.date().strftime(self.date_format)

        if path is None:
            path = f"{self.subject_id}_{name}"

        if map_ is None:
            map_ = self.day_map_type(name=f"{self.composite.name}/{name}")
            self.composite.map.set_item(map_)

        self.days_dataset.components["node_content"].insert_entry(
            path=path,
            length=length,
            map_=map_,
            start=start,
            end=end,
            id_=id_,
        )

        return map_.get_object()

    def insert_entry(self, path, start, end=None, length=0, file_id=None, day_path=None, day_id=None):
        if self.days_dataset.size == 0:
            index = 0
            day_start = None
        else:
            index, day_start = self.days_dataset.components["start_times"].find_time_index(
                Timestamp(start.date()),
                approx=True,
                tails=True,
            )

        if day_start is not None and day_start.date() == start.date():
            day = self.days_dataset.components["object_reference"].get_object(index)
        else:
            day = self.create_day(start=start, end=end, length=length, path=day_path, id_=day_id)

        day.components["leaf_content"].insert_entry(
            path=path,
            length=length,
            start=start,
            end=end,
            id_=file_id,
        )
        day_length = day.get_field("Length").sum()
        true_day_start = day.components["start_times"].start_nanostamp
        true_day_end = day.components["end_times"].end_nanostamp
        self.days_dataset.components["node_content"].set_item(
            index=index,
            start=true_day_start,
            end=true_day_end,
            length=day_length,
        )

