""" xltekvideostable.py

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
from cdfs import BaseTimeContentsTableSchema, TimeContentsTableManifestation
from sqlalchemy import select, lambda_stmt
from sqlalchemy.orm import Session, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.types import BigInteger

# Local Packages #


# Definitions #
# Classes #
class BaseXLTEKVideosTableSchema(BaseTimeContentsTableSchema):
    __tablename__ = "xltekvideos"
    __mapper_args__ = {"polymorphic_identity": "xltekvideos"}
    start_id = mapped_column(BigInteger)
    end_id = mapped_column(BigInteger)

    # Class Methods #
    @classmethod
    def get_start_end_ids(cls, session: Session) -> tuple[tuple[int, int], ...]:
        statement = lambda_stmt(lambda: select(cls.start_id, cls.end_id).order_by(cls.start_id))
        return tuple(session.execute(statement))

    @classmethod
    async def get_start_end_ids_async(cls, session: AsyncSession) -> tuple[tuple[int, int], ...]:
        statement = lambda_stmt(lambda: select(cls.start_id, cls.end_id).order_by(cls.start_id))
        return tuple(await session.execute(statement))


class XLTEKVideosTableManifestation(TimeContentsTableManifestation):

    # Instance Methods #
    # Contents
    def get_start_end_ids(self, session: Session | None = None) -> tuple[tuple[int, int], ...]:
        if session is not None:
            return self.table_schema.get_start_end_ids(session=session)
        else:
            with self.create_session() as session:
                return self.table_schema.get_start_end_ids(session=session)

    async def get_start_end_ids_async(self, session: AsyncSession | None = None) -> tuple[tuple[int, int], ...]:
        if session is not None:
            return await self.table_schema.get_start_end_ids_async(session=session)
        else:
            async with self.create_async_session() as session:
                return await self.table_schema.get_start_end_ids_async(session=session)