import json

from fastapi import Query


def pagination_parameters(
    page: int = 1,
    items_per_page: int = Query(5, alias="itemsPerPage"),
    filter_spec: str = Query(
        [],
        alias="filter",
        description="Dynamic filters based on JSON format.",
        example='[{"field":"foo", "op":"ilike", "value":"%bar%"}]',
    ),
    sort_spec: str = Query(
        [],
        alias="sort",
        description="Dynamic sorts based on JSON format.",
        example='[{"field":"foo", "direction":"asc"}]',
    ),
):
    if filter_spec:
        filter_spec = json.loads(filter_spec)

    if sort_spec:
        sort_spec = json.loads(sort_spec)

    return {
        "page": page,
        "items_per_page": items_per_page,
        "filter_spec": filter_spec,
        "sort_spec": sort_spec,
    }
