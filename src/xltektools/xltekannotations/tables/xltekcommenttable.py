"""xltekcommenttable.py

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
from typing import Any

# Third-Party Packages #
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# Local Packages #
from .xltekannotationstable import BaseXLTEKAnnotationsTableSchema, XLTEKAnnotationsTableManifestation


# Definitions #
# Classes #
class BaseXLTEKCommentTableSchema(BaseXLTEKAnnotationsTableSchema):
    """A table schema for containing the Comment annotations in an XLTEK Study.

    Class Attributes:
        __tablename__: The name of the table.
        __mapper_args__: Mapper arguments for SQLAlchemy.
    """

    # Class Attributes #
    __tablename__ = "comments"
    __mapper_args__ = {"polymorphic_identity": "comments"}

    # Columns #
    id = mapped_column(ForeignKey("annotations.id"), primary_key=True)
    user: Mapped[str] = mapped_column(nullable=True)


class XLTEKCommentTableManifestation(XLTEKAnnotationsTableManifestation):
    """The manifestation of a XLTEKCommentTable.

    Attributes:
        _database: A weak reference to the SQAlchemy database to interface with.
        table_schema: The SQLAlchemy declarative table which this object act as the interface for.

    Args:
        table_schema: The SQLAlchemy declarative table which this object act as the interface for.
        database: The SQAlchemy database to interface with.
        init: Determines if this object will construct.
        **kwargs: Additional keyword arguments.
    """
