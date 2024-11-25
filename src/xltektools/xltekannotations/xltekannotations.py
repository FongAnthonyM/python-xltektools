""" xltekannotations.py.py

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
from collections.abc import Iterable
from pathlib import Path
from typing import Any

# Third-Party Packages #
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemyobjects import Database
from sqlalchemyobjects.tables import TableManifestation

# Local Packages #
from .tables import XLTEKAnnotationsInformationTableManifestation
from .tables import XLTEKAnnotationsTableManifestation
from .tables import XLTEKXLSpikeTableManifestation
from .xltekannotationsasyncschema import XLTEKAnnotationsAsyncSchema
from .xltekannotationsasyncschema import XLTEKAnnotationsInformationTableSchema
from .xltekannotationsasyncschema import XLTEKAnnotationsTableSchema
from .xltekannotationsasyncschema import XLTEKXLSpikeTableSchema


# Definitions #
# Classes #
class XLTEKAnnotations(Database):

    # Attributes #
    meta_table_name: str = "meta_information"

    schema: type[DeclarativeBase] | None = XLTEKAnnotationsAsyncSchema
    table_maps: dict[str, tuple[type[TableManifestation], type[DeclarativeBase], dict[str, Any]]] = {
        meta_table_name: (XLTEKAnnotationsInformationTableManifestation, XLTEKAnnotationsInformationTableSchema, {}),
        "annotations": (XLTEKAnnotationsTableManifestation, XLTEKAnnotationsTableSchema, {}),
        "xlspike":  (XLTEKXLSpikeTableManifestation, XLTEKXLSpikeTableSchema, {}),
    }

    type_map: dict[str, str] = {
        "annotations": "annotations",
        "xlspike": "xlspike",
    }
    annotations_types: dict[str, TableManifestation]

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: str | Path | None = None,
        schema: type[DeclarativeBase] | None = None,
        table_map: dict[str, tuple[type[TableManifestation], type[DeclarativeBase], dict[str, Any]]] | None = None,
        open_: bool = False,
        create: bool = False,
        *,
        init: bool = True,
        **kwargs,
    ) -> None:
        # New Attributes #
        self.annotations_types = {}

        # Parent Attributes #
        super().__init__()

        # Object Construction #
        if init:
            self.construct(
                path,
                schema,
                table_map,
                open_,
                create,
                **kwargs,
            )

    # Instance Methods #
    # Tables
    def manifest_tables(
        self,
        table_map: dict[str, tuple[type[TableManifestation], type[DeclarativeBase], dict[str, Any]]] | None = None,
    ) -> None:
        """Manifests the table from the table map.

        Args:
            table_map: The map of tables to manifest the table from. If None, uses the default table map.
        """
        super().manifest_tables(table_map=table_map)
        self.annotations_types.update(((a, self.tables[n]) for a, n in self.annotations_types.items()))

    # Annotations
    def insert_annotation(
        self,
        entry: dict[str, Any] | None = None,
        session: Session | None = None,
        begin: bool = False,
        **kwargs: Any,
    ) -> None:
        """Inserts an item into the table.

        Args:
            entry: A dictionary representing the entry to insert. Defaults to None.
            session: The SQLAlchemy session to apply the modification. Defaults to None.
            begin: If True, begins a transaction for the operation. Defaults to False.
            **kwargs: Additional keyword arguments for the entry.
        """
        self.annotations_types[entry["Type"]].insert(entry=entry, session=session, begin=begin, **kwargs)

    async def insert_async(
        self,
        entry: dict[str, Any] | None = None,
        session: AsyncSession | None = None,
        begin: bool = False,
        **kwargs: Any,
    ) -> None:
        """Asynchronously inserts an item into the table.

        Args:
            entry: A dictionary representing the entry to insert. Defaults to None.
            session: The SQLAlchemy session to apply the modification. Defaults to None.
            begin: If True, begins a transaction for the operation. Defaults to False.
            **kwargs: Additional keyword arguments for the entry.
        """
        await self.annotations_types[entry["Type"]].insert_async(entry=entry, session=session, begin=begin, **kwargs)

    def insert_annotations(
        self,
        entries: Iterable[dict[str, Any]] = (),
        session: Session | None = None,
        begin: bool = False,
    ) -> None:
        """Inserts multiple annotations into the table.

        Args:
            entries: The entries to insert. Defaults to an empty iterable.
            session: The SQLAlchemy session to apply the modification. Defaults to None.
            begin: If True, begins a transaction for the operation. Defaults to False.
        """
        if session is None:
            session = self.create_session()
            was_open = False
        else:
            was_open = True

        if begin:
            with session.begin():
                for entry in entries:
                    self.annotations_types[entry["Type"]].insert(entry=entry, session=session, begin=False)
        else:
            for entry in entries:
                self.annotations_types[entry["Type"]].insert(entry=entry, session=session, begin=False)

        if not was_open:
            session.close()

    async def insert_annotations_async(
        self,
        entries: Iterable[dict[str, Any]] = (),
        session: AsyncSession | None = None,
        begin: bool = False,
    ) -> None:
        """Asynchronously inserts multiple annotations into the table.

        Args:
            entries: The entries to insert. Defaults to an empty iterable.
            session: The SQLAlchemy session to apply the modification. Defaults to None.
            begin: If True, begins a transaction for the operation. Defaults to False.
        """
        if session is None:
            session = self.create_async_session()
            was_open = False
        else:
            was_open = True

        if begin:
            async with session.begin():
                for entry in entries:
                    await self.annotations_types[entry["Type"]].insert_async(entry=entry, session=session, begin=False)
        else:
            for entry in entries:
                await self.annotations_types[entry["Type"]].insert_async(entry=entry, session=session, begin=False)

        if not was_open:
            await session.close()

