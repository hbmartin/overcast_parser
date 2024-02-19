import sys
import urllib
import webbrowser
from urllib.parse import unquote

import podcastparser
import requests

from overcast_parser import utils
from overcast_parser.itunes_podcast_rss import extract_feed_url_for_id
from overcast_parser.overcast_parser import OvercastParser


def main() -> None:
    url = unquote(sys.argv[1])

    parser = OvercastParser()

    data = requests.get(url).text

    parser.feed(data)
    (itunes_id, stream_url, overcast_id, title, feed_url) = parser.close()
    print(title)

    feed_url = extract_feed_url_for_id(itunes_id)
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
    print(result)

    webbrowser.open("overcast://")


if __name__ == "__main__":
    main()
