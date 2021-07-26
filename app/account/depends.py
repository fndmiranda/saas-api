def password_reset_form_parameters(
    token: str = "tttttt",
#     page: int = 1,
#     items_per_page: int = Query(5, alias="itemsPerPage"),
#     query_str: str = Query(None, alias="q"),
#     filter_spec: str = Query(
#         [], alias="filter", description="this is the value of snap `code here`"
#     ),
#     sort_spec: str = Query(
#         [], alias="sort", description="this is the value of snap `code here`"
#     ),
#     # sort_by: List[str] = Query([], alias="sortBy[]"),
#     descending: List[bool] = Query([], alias="descending[]"),
#     # current_user: User = Depends(get_current_user),
):
#     if filter_spec:
#         filter_spec = json.loads(filter_spec)
#
#     if sort_spec:
#         sort_spec = json.loads(sort_spec)
#
#     return {
#         "page": page,
#         "items_per_page": items_per_page,
#         "query_str": query_str,
#         "filter_spec": filter_spec,
#         "sort_spec": sort_spec,
#         "descending": descending,
#         # "current_user": current_user,
#     }
    return {
        "token": token,
    }