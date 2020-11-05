from typing import Callable

from deepmerge import always_merger


def pager(items_count: int, item_per_page: int, func: Callable[[int, int], dict]) -> dict:
    """
    A pager which executes a function on every page with the start and end item indices
    and deep merge the returned response.

    :param items_count: all items count
    :param item_per_page: items count per page
    :param func: the func called in each page with [start_index, end_index], returns the response dict
    :return all merged response
    """
    page_count = items_count // item_per_page

    remainder = items_count % item_per_page

    response_all = {}

    for page_index in range(page_count + 1):
        start_index = 0
        end_index = (page_index * item_per_page) + (item_per_page - 1)

        if page_index > 0:
            start_index = page_index * item_per_page

        if remainder > 0 and page_index == page_count:
            end_index = start_index + remainder

        response_all = always_merger.merge(response_all, func(start_index, end_index))

    return response_all
