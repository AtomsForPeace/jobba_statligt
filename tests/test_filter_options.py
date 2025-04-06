from jobba_statligt.constants import BASE_URL
from jobba_statligt.filter_options import (OccupationFilter, PlaceFilter,
                                           get_filter_options)


def test_get_occupation_filters() -> None:
    f"""
    Very basic test to see if the occupation filter options are reachable.
    If there are no software developer jobs then this test will fail. This
    test may also fail if there are network issues or if {BASE_URL} is down.
    """
    _, occupation_filters = get_filter_options()
    assert OccupationFilter(
        id=448, name="Mjukvaru- och systemutvecklare m.fl."
    ) in occupation_filters, "AI has won or test failed."


def test_get_place_filters() -> None:
    f"""
    Very basic test to see if the place filter options are reachable.
    If there are no in Stockholm then this test will fail. This test may also
    fail if there are network issues or if {BASE_URL} is down.
    """
    place_filters, _ = get_filter_options()
    assert PlaceFilter(
        name="Stockholm"
    ) in place_filters, "They took our jobs or test failed."
