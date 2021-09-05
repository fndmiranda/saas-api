import math
from collections import namedtuple

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.filters.exceptions import InvalidPage


async def apply_pagination(
    stmt, session: AsyncSession, page_number=None, page_size=None
):
    """Apply pagination to a SQLAlchemy stmt object.

    :param stmt:
        A :class:`sqlalchemy.sql.selectable.Select` instance.

    :param session:
        A :class:`sqlalchemy.ext.asyncio.AsyncSession` instance.

    :param page_number:
        Page to be returned (starts and defaults to 1).

    :param page_size:
        Maximum number of results to be returned in the page (defaults
        to the total results).

    :returns:
        A 2-tuple with the paginated SQLAlchemy stmt object and
        a pagination namedtuple.

        The pagination object contains information about the results
        and pages: ``page_size`` (defaults to ``total_results``),
        ``page_number`` (defaults to 1), ``num_pages`` and
        ``total_results``.

    Basic usage::

        stmt, pagination = apply_pagination(stmt, 1, 10)
        >>> len(stmt)
        10
        >>> pagination.page_size
        10
        >>> pagination.page_number
        1
        >>> pagination.num_pages
        3
        >>> pagination.total_results
        22
        >>> page_size, page_number, num_pages, total_results = pagination
    """

    query_count = await session.execute(stmt.with_only_columns(func.count()))

    total_results = query_count.scalar_one()
    stmt = _limit(stmt, page_size)

    # Page size defaults to total results
    if page_size is None or (page_size > total_results and total_results > 0):
        page_size = total_results

    stmt = _offset(stmt, page_number, page_size)

    # Page number defaults to 1
    if page_number is None:
        page_number = 1

    num_pages = _calculate_num_pages(page_size, total_results)

    Pagination = namedtuple(
        "Pagination",
        ["page_number", "page_size", "num_pages", "total_results"],
    )
    return stmt, Pagination(page_number, page_size, num_pages, total_results)


def _limit(query, page_size):
    if page_size is not None:
        if page_size < 0:
            raise InvalidPage(
                "Page size should not be negative: {}".format(page_size)
            )

        query = query.limit(page_size)

    return query


def _offset(query, page_number, page_size):
    if page_number is not None:
        if page_number < 1:
            raise InvalidPage(
                "Page number should be positive: {}".format(page_number)
            )

        query = query.offset((page_number - 1) * page_size)

    return query


def _calculate_num_pages(page_size, total_results):
    if page_size == 0:
        return 0

    return math.ceil(float(total_results) / float(page_size))
