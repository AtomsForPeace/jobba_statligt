import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement
from pydantic import BaseModel

from jobba_statligt.constants import BASE_URL


class JobAdvert(BaseModel):
    place: str
    published: datetime
    title: str
    link: str


def parse_job_advert(element: PageElement) -> JobAdvert:
    """
    Goes through one of the <article> elements on the search results
    page and builds a JobAdvert object out of it. If there are any
    problems with the format then an exception will be thrown.
    """
    link_element = element.find_next("a", href=True)
    if not link_element:
        raise Exception("Missing link")

    if not isinstance(link_element, Tag):
        raise Exception("Incorrect format")

    link = link_element["href"]
    if not link:
        raise Exception("Missing link")

    if not isinstance(link, str):
        raise Exception("Incorrect format")

    title_element = element.find_next("h2")
    if not title_element:
        raise Exception("Missing title")
    title = title_element.text

    main_div = element.find_next("div")
    if not main_div:
        raise Exception("Missing contents")

    if not isinstance(main_div, Tag):
        raise Exception("Incorrect format")

    spans = main_div.find_all("span")
    outer_span = spans[-3]

    if not isinstance(outer_span, Tag):
        raise Exception("Incorrect format")

    city_texts = [
        text for text in outer_span.contents
        if isinstance(text, str)
    ]
    place = ''.join(city_texts).strip()

    date_span = outer_span.find('span', class_='text-greyDark')
    if not date_span:
        raise Exception("Missing published date")

    date_match = re.search(r'\d{4}-\d{2}-\d{2}', date_span.text)
    if date_match:
        date_str = date_match.group()
        published = datetime.strptime(date_str, '%Y-%m-%d')
    else:
        raise Exception("Missing published date")

    return JobAdvert(
        place=place,
        published=published,
        title=title,
        link=f"{BASE_URL}{link}"
    )


def parse_job_adverts(search_url: str):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")
    return [parse_job_advert(element=article) for article in articles]
