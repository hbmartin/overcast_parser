"""
(c) 2019 Harold Martin / hbmartin released under MIT License
"""

import json
import urllib

import podcastparser
import requests
import appex
import console
import sys
import webbrowser
from urllib.parse import unquote

from overcast_parser import utils
from overcast_parser import OvercastParser
from overcast_parser.itunes_podcast_rss import extract_feed_id
from overcast_parser.stores.Reminders import Reminders


def main():
    console.clear()

    url = None
    if appex.is_running_extension():
        url = appex.get_url()
    elif len(sys.argv) > 1:
        url = unquote(sys.argv[1])

    if url is None:
        print("No URL found")
        webbrowser.open("overcast://")
        return

    console.show_activity()
    print(url)

    parser = OvercastParser()
    reminders = Reminders()

    data = requests.get(url).text
    parser.feed(data)
    (itunes_id, stream_url, overcast_id, title) = parser.close()
    print(title)

    feed_url = extract_feed_id(itunes_id)
    print(feed_url)

    podcast = podcastparser.parse(feed_url, urllib.request.urlopen(feed_url))
    print(podcast["link"])

    item = utils.find_episode(podcast["episodes"], title, stream_url)
    print(item)

    result = {
        "title": title,
        "itunes_channel_id": itunes_id,
        "enclosure_url": stream_url,
        "overcast_id": overcast_id,
        "guid": item["guid"],
        "channel_link": podcast["link"],
        "duration": item["total_time"],
        "published_time": item["published"],
    }

    reminders.add(json.dumps(result))
    print("Added to reminders")

    console.hide_activity()
    webbrowser.open("overcast://")


if __name__ == "__main__":
    main()
