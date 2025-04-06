from pydantic import BaseModel

from jobba_statligt.constants import BASE_URL
from jobba_statligt.job_advert import JobAdvert, parse_job_adverts
from jobba_statligt.occupation import Occupation
from jobba_statligt.place import Place


class FilterOptions(BaseModel):
    places: list[Place]
    occupations: list[Occupation]
    limit: int = 999


class JobbaStatligt:

    def __init__(self) -> None:
        self._filter_options = None

    def search(self, filter_options: FilterOptions) -> list[JobAdvert]:
        """
        This builds the query needed based on the filter_options passed.
        This query will the be made and the results formatted into
        JobAdvert objects.
        """
        search_url = f"{BASE_URL}/sok?query="

        if filter_options.places:
            search_url += "&searchfield-3786="
        for place_filter in filter_options.places:
            search_url += f"&Area={place_filter.value}"

        if filter_options.occupations:
            search_url += "&searchfield-3792="
        for occupation_filter in filter_options.occupations:
            search_url += f"&Occupation={occupation_filter.value}"

        search_url += f"&display={filter_options.limit}"

        return parse_job_adverts(search_url=search_url)
