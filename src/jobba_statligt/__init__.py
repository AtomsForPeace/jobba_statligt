from jobba_statligt.constants import BASE_URL
from jobba_statligt.filter_options import FilterOptions, get_filter_options
from jobba_statligt.job_advert import JobAdvert, parse_job_adverts


class JobbaStaatligt:

    def __init__(self) -> None:
        self._filter_options = None

    @property
    def filter_options(self) -> FilterOptions:
        """
        This is set as a property as it should only need to be fetched
        once. This saves making multiple requests.
        """
        if self._filter_options is None:
            self._filter_options = get_filter_options()
        return self._filter_options

    def search(self, filter_options: FilterOptions) -> list[JobAdvert]:
        """
        This builds the query needed based on the filter_options passed.
        This query will the be made and the results formatted into
        JobAdvert objects.
        """
        search_url = f"{BASE_URL}/sok?query="

        if filter_options.place_filters:
            search_url += "&searchfield-3786="
        for place_filter in filter_options.place_filters:
            search_url += f"&Area={place_filter.name}"

        if filter_options.occupation_filters:
            search_url += "&searchfield-3792="
        for occupation_filter in filter_options.occupation_filters:
            search_url += f"&Occupation={occupation_filter.id}"

        return parse_job_adverts(search_url=search_url)
