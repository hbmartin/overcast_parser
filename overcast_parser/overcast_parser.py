# ruff: noqa: ANN001,ANN201,C901,PLR0912

import re
from html.parser import HTMLParser

_ITUNES = re.compile(r"https://podcasts\.apple\.com/podcast/id(\d+)(/.*)?")


class OvercastParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.itunes_id = None
        self.enclosure_url = None
        self.overcast_id = None
        self.ep_title = None
        self.feed_url = None
        self._found_title = False
        self._outer_href = None

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            attrs_dict = {a[0]: a[1] for a in attrs}
            if attrs_dict["name"] == "twitter:player:stream":
                self.enclosure_url = attrs_dict["content"].split("#")[0]
            elif attrs_dict["name"] == "twitter:app:url:iphone":
                self.overcast_id = int(attrs_dict["content"].split("/")[-1])
        elif tag == "a":
            for a in attrs:
                if a[0] == "href":
                    self._outer_href = a[1]
                    result = _ITUNES.match(a[1])
                    if result:
                        self.itunes_id = int(result.group(1))
                    return
        elif tag == "h2":
            for a in attrs:
                if a[0] == "class" and "title" in a[1]:
                    self._found_title = True
        elif tag == "img":
            for a in attrs:
                if a[0] == "src":
                    if a[1].endswith("/img/badge-rss.svg"):
                        self.feed_url = self._outer_href
                    return

    def handle_data(self, data):
        if self._found_title:
            self.ep_title = data.strip()
            self._found_title = False

    def close(self) -> tuple:
        super().close()

        tmp_itunes = self.itunes_id
        tmp_stream_url = self.enclosure_url
        tmp_overcast = self.overcast_id
        tmp_title = self.ep_title
        tmp_feed_url = self.feed_url

        self.reset()

        self.itunes_id = None
        self.enclosure_url = None
        self.overcast_id = None
        self.ep_title = None
        self._found_title = False
        self._outer_href = None
        self.feed_url = None

        return tmp_itunes, tmp_stream_url, tmp_overcast, tmp_title, tmp_feed_url

    def parse_overcast(self, data) -> tuple:
        self.feed(data)
        return self.close()
