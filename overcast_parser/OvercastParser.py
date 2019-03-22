"""
(c) 2019 Harold Martin / hbmartin released under MIT License
"""
import re
from html.parser import HTMLParser

ITUNES = re.compile(r"/itunes(\d+)/([A-Za-z0-9_-]?)")


def _d(attrs):
    return {a[0]: a[1] for a in attrs}


class OvercastParser(HTMLParser):
    def __init__(self):
        super(OvercastParser, self).__init__()
        self.itunes_id = None
        self.stream_url = None
        self.overcast_id = None
        self.title = None
        self._found_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            attrs_dict = _d(attrs)
            if attrs_dict["name"] == "twitter:player:stream":
                self.stream_url = attrs_dict["content"].split("#")[0]
            elif attrs_dict["name"] == "twitter:app:url:iphone":
                self.overcast_id = int(attrs_dict["content"].split("/")[-1])
        elif tag == "a":
            attrs_dict = _d(attrs)
            result = ITUNES.match(attrs_dict["href"])
            if result:
                self.itunes_id = int(result.group(1))
        elif tag == "div":
            attrs_dict = _d(attrs)
            if "class" in attrs_dict and attrs_dict["class"] == "title":
                self._found_title = True

    def handle_data(self, data):
        if self._found_title:
            self.title = data.strip()
            self._found_title = False

    def close(self):
        super(OvercastParser, self).close()

        tmp_itunes = self.itunes_id
        tmp_stream_url = self.stream_url
        tmp_overcast = self.overcast_id
        tmp_title = self.title

        self.reset()

        self.itunes_id = None
        self.stream_url = None
        self.overcast_id = None
        self.title = None
        self._found_title = False

        return tmp_itunes, tmp_stream_url, tmp_overcast, tmp_title

    def parse_overcast(self, data):
        self.feed(data)
        return self.close()
