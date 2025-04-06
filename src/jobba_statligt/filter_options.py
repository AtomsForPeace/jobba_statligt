from pathlib import Path
from typing import cast

import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag
from pydantic import BaseModel

from jobba_statligt.constants import BASE_URL, CACHE_FILE_PATH


class PlaceFilter(BaseModel):
    name: str


class OccupationFilter(BaseModel):
    id: int
    name: str


def parse_place_filter(element: PageElement) -> list[PlaceFilter]:

    if not isinstance(element, Tag):
        raise Exception("Incorrect format")

    place_filters = []

    label_tags = element.find_all('label')

    for label_tag in label_tags:

        label_text = label_tag.get_text(strip=True)
        if label_text:
            place_filters.append(
                PlaceFilter(
                    name=label_text
                )
            )
        else:
            raise

    return place_filters


def parse_occupation_filter(element: PageElement) -> list[OccupationFilter]:

    if not isinstance(element, Tag):
        raise Exception("Incorrect format")

    occupation_filters = []

    input_tags = element.find_all('input', {'type': 'checkbox'})
    label_tags = element.find_all('label')

    if len(input_tags) != len(label_tags):
        raise Exception("Incorrect format")

    for input_tag, label_tag in zip(input_tags, label_tags):
        if not isinstance(input_tag, Tag):
            raise Exception("Incorrect format")

        input_id = cast(int, input_tag.get('value'))
        if not input_id:
            raise Exception("No occupation filter id found")

        label_text = label_tag.get_text(strip=True)
        if input_id and label_text:
            occupation_filters.append(
                OccupationFilter(
                    id=int(input_id),
                    name=label_text
                )
            )
        else:
            raise

    return occupation_filters


def get_filter_options() -> tuple[list[PlaceFilter], list[OccupationFilter]]:
    if Path(CACHE_FILE_PATH).exists():
        with open(CACHE_FILE_PATH) as f:
            soup = BeautifulSoup(f.read(), "html.parser")
    else:
        response = requests.get(BASE_URL)
        text = response.text
        with open(CACHE_FILE_PATH, "w") as f:
            f.write(text)
        soup = BeautifulSoup(text, "html.parser")

    place_filters: list[PlaceFilter] = []
    place_fieldset = soup.find_all("fieldset")[0]

    if not isinstance(place_fieldset, Tag):
        raise Exception("Incorrect format")

    for element in place_fieldset.find_all('div', recursive=False):
        _filters = parse_place_filter(element=element)
        place_filters.extend(_filters)

    occupation_filters: list[OccupationFilter] = []
    occupation_fieldset = soup.find_all("fieldset")[1]

    if not isinstance(occupation_fieldset, Tag):
        raise Exception("Incorrect format")

    for element in occupation_fieldset.find_all('div', recursive=False):
        _filters = parse_occupation_filter(element=element)
        occupation_filters.extend(_filters)

    return (place_filters, occupation_filters)
