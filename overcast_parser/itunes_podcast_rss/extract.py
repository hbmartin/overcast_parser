"""
(c) 2016 Michal Holub / wotaen released under MIT License
Source: https://github.com/wotaen/itunes_podcast_rss

Modified 2019 by Harold Martin
"""

import json
import re

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3 import Retry

URL_TEMPLATE = "https://itunes.apple.com/lookup?id=%s&entity=podcast"


def id_from_url(url):
    """
    Extract ID from iTunes podcast URL
    :param url (str)
    :return: (str)
    """
    matches = re.findall(r"/id([0-9]+)", url)
    if len(matches) == 0:
        raise LookupError("No ID present in the given URL")
    if len(matches) > 1:
        raise LookupError(
            "More than one ID present in the URL, cannot decide which one to take"
        )
    return matches[0]


def lookup_id(podcast_id):
    """
    Looks up podcast ID in Itunes lookup service
     https://itunes.apple.com/lookup?id=<id>&entity=podcast
    :param podcast_id:
    :return: itunes response for the lookup as dict
    """
    retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=retries))
    response = s.get(URL_TEMPLATE % podcast_id)
    content = json.loads(response.content.decode("utf-8"))
    return content


def feed_url(itunes_lookup_response):
    """
    Returns feed URL from the itunes lookup response
    :param itunes_lookup_response:
    :return: str
    """
    if len(itunes_lookup_response.get("results")) == 0:
        raise LookupError("iTunes response has no results")
    url = itunes_lookup_response.get("results")[0].get("feedUrl")
    if url is None:
        raise LookupError("feedUrl field is not present in response")
    return url


def extract_feed_id(feed_id):
    response = lookup_id(feed_id)
    url = feed_url(response)
    return url


def extract_feed_url(url):
    return extract_feed_id(id_from_url(url))
