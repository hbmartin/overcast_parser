# ruff: noqa: EM101,TRY003
"""(c) 2016 Michal Holub / wotaen released under MIT License.

Source: https://github.com/wotaen/itunes_podcast_rss

Modified 2019 by Harold Martin
"""

import json
import re

import requests
from requests.adapters import HTTPAdapter

URL_TEMPLATE = "https://itunes.apple.com/lookup?id=%s&entity=podcast"


def id_from_url(url: str) -> int:
    """Extract ID from iTunes podcast URL."""
    return int(re.findall(r"/id([0-9]+)", url)[0])


def fetch_id(itunes_id: int) -> dict:
    """Look up podcast ID in iTunes lookup service."""
    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=3))
    response = s.get(URL_TEMPLATE % itunes_id)
    return json.loads(response.content.decode("utf-8"))


def _feed_url(itunes_response: dict) -> str:
    """Return feed URL from the itunes lookup response."""
    if len(itunes_response.get("results")) == 0:
        raise LookupError("iTunes response has no results")
    url = itunes_response.get("results")[0].get("feedUrl")
    if url is None:
        raise LookupError("feedUrl field is not present in response")
    return url


def extract_feed_url_for_id(itunes_id: int) -> str:
    response = fetch_id(itunes_id)
    return _feed_url(response)
