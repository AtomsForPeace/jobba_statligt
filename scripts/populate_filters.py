#!/usr/bin/env python3
"""
This python script populates both the place.py and occupation.py files.
These are both enums of the valid filters possible to use in the search.
"""
import re

from jobba_statligt.filter_options import (OccupationFilter, PlaceFilter,
                                           get_filter_options)


def swedish_snake_upper(text: str) -> str:
    # Replace all non-letter (including Swedish) characters with space
    text = re.sub(r"[^A-Za-zÅÄÖåäö]+", " ", text)

    # Convert spaces to underscores and uppercase
    return "_".join(text.strip().split()).upper()


def populate_place_filters(filters: list[PlaceFilter]) -> None:
    with open("./src/jobba_statligt/place.py", "w") as f:
        lines = [
            "from enum import StrEnum",
            "",
            "",
            "class Place(StrEnum):",
        ]
        for place_filter in filters:
            member = swedish_snake_upper(place_filter.name)
            lines.append(
                f"    {member} = '{place_filter.name}'"
            )
        lines += ""
        f.writelines("\n".join(lines))


def populate_occupation_filters(filters: list[OccupationFilter]) -> None:
    with open("./src/jobba_statligt/occupation.py", "w") as f:
        lines = [
            "from enum import IntEnum",
            "",
            "",
            "class Occupation(IntEnum):",
        ]
        for occupation_filter in filters:
            member = swedish_snake_upper(occupation_filter.name)
            lines.append(
                f"    {member} = {occupation_filter.id}"
            )

        lines += ""
        f.write("\n".join(lines))


def main() -> None:
    place_filters, occupation_filters = get_filter_options()

    populate_place_filters(filters=place_filters)
    populate_occupation_filters(filters=occupation_filters)


if __name__ == "__main__":
    main()
