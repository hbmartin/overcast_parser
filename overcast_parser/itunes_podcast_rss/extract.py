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


def lookup_id(podcast_id: int) -> dict:
    """Look up podcast ID in iTunes lookup service."""
    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=3))
    response = s.get(URL_TEMPLATE % podcast_id)
    return json.loads(response.content.decode("utf-8"))


def feed_url(itunes_lookup_response: dict) -> str:
    """Return feed URL from the itunes lookup response."""
    if len(itunes_lookup_response.get("results")) == 0:
        raise LookupError("iTunes response has no results")
    url = itunes_lookup_response.get("results")[0].get("feedUrl")
    if url is None:
        raise LookupError("feedUrl field is not present in response")
    return url


def extract_feed_id(feed_id: int) -> str:
    response = lookup_id(feed_id)
    return feed_url(response)


def extract_feed_url(url: str) -> str:
    feed_id = id_from_url(url)
    return extract_feed_id(feed_id)
