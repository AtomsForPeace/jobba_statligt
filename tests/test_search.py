from jobba_statligt import JobbaStaatligt
from jobba_statligt.constants import BASE_URL
from jobba_statligt.filter_options import (FilterOptions, OccupationFilter,
                                           PlaceFilter)


def test_search() -> None:
    f"""
    Very basic test to see if the search returns results.
    If there are no software developer jobs in Stockholm then
    this test will fail. This test may also fail if there are
    network issues or if {BASE_URL} is down.
    """
    client = JobbaStaatligt()
    filter_options = FilterOptions(
        place_filters=[
            PlaceFilter(
                name="Stockholm"
            ),
        ],
        occupation_filters=[
            OccupationFilter(
                id=448,
                name="Mjukvaru- och systemutvecklare m.fl."
            ),
        ]
    )
    results = client.search(filter_options=filter_options)
    assert len(results) > 0, "Stockholm has fallen or test failed."
