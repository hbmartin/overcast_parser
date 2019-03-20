"""
(c) 2019 Harold Martin / hbmartin released under MIT License
"""

import json
import requests
import appex
import console
import sys
import webbrowser
from urllib.parse import unquote

from overcast_parser.OvercastParser import OvercastParser
from overcast_parser.itunes_podcast_rss.extract import extract_feed_id
from overcast_parser.pyPodcastParser.Podcast import Podcast
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

    response = requests.get(feed_url)
    podcast = Podcast(response.content)
    print(podcast)
    item = podcast.find_item(title, stream_url)
    print(item)

    result = {
        "title": title,
        "itunes_channel_id": itunes_id,
        "enclosure_url": stream_url,
        "overcast_id": overcast_id,
        "guid": item.guid,
        "itunes_new_feed_url": podcast.itunes_new_feed_url,
        "channel_link": podcast.link,
        "duration": item.itunes_duration,
        "published_time": item.time_published,
    }

    reminders.add(json.dumps(result))
    print("check guid already exists")
    console.hide_activity()
    webbrowser.open("overcast://")


if __name__ == "__main__":
    main()
