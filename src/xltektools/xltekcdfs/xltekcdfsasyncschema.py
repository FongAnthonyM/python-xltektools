"""xltekcdfsschema.py

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
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

# Local Packages #
from .tables import BaseXLTEKMetaInformationTableSchema, BaseXLTEKContentsTableSchema


# Definitions #
# Classes #
class XLTEKCDFSAsyncSchema(AsyncAttrs, DeclarativeBase):
    pass


class XLTEKMetaInformationTableSchema(BaseXLTEKMetaInformationTableSchema, XLTEKCDFSAsyncSchema):
    pass


class XLTEKContentsTableSchema(BaseXLTEKContentsTableSchema, XLTEKCDFSAsyncSchema):
    pass
