import unittest
from os import path
import sys
import podcastparser

here = path.dirname(__file__)
sys.path.insert(0, path.join(here, ".."))

from overcast_parser import OvercastParser, utils
from overcast_parser.itunes_podcast_rss import feed_url


class TestOvercastParser(unittest.TestCase):
    def test_parse_overcast(self):
        parser = OvercastParser()

        with open(path.join(here, "data", "overcast.htm"), "r") as f:
            data = f.read()

        (itunes_id, stream_url, overcast_id, title) = parser.parse_overcast(data)

        self.assertEqual(itunes_id, 1042433083)
        self.assertEqual(stream_url, "https://traffic.megaphone.fm/VMP2975209749.mp3")
        self.assertEqual(overcast_id, 367482639706188)
        self.assertEqual(title, "The reparations primary")

    def test_extract_feed_id(self):
        itunes_data = {
            "resultCount": 1,
            "results": [
                {
                    "wrapperType": "track",
                    "kind": "podcast",
                    "artistId": 1439215748,
                    "collectionId": 1042433083,
                    "trackId": 1042433083,
                    "artistName": "Vox",
                    "collectionName": "Vox's The Weeds",
                    "trackName": "Vox's The Weeds",
                    "collectionCensoredName": "Vox's The Weeds",
                    "trackCensoredName": "Vox's The Weeds",
                    "artistViewUrl": "https://itunes.apple.com/us/artist/vox/1439215748?mt=2&uo=4",
                    "collectionViewUrl": "https://itunes.apple.com/us/podcast/voxs-the-weeds/id1042433083?mt=2&uo=4",
                    "feedUrl": "https://feeds.megaphone.fm/theweeds",
                    "trackViewUrl": "https://itunes.apple.com/us/podcast/voxs-the-weeds/id1042433083?mt=2&uo=4",
                    "artworkUrl30": "https://is4-ssl.mzstatic.com/image/thumb/Music124/v4/5e/ab/72/5eab7235-f01e-81a5-d720-50771ec447b6/source/30x30bb.jpg",
                    "artworkUrl60": "https://is4-ssl.mzstatic.com/image/thumb/Music124/v4/5e/ab/72/5eab7235-f01e-81a5-d720-50771ec447b6/source/60x60bb.jpg",
                    "artworkUrl100": "https://is4-ssl.mzstatic.com/image/thumb/Music124/v4/5e/ab/72/5eab7235-f01e-81a5-d720-50771ec447b6/source/100x100bb.jpg",
                    "collectionPrice": 0.0,
                    "trackPrice": 0.0,
                    "trackRentalPrice": 0,
                    "collectionHdPrice": 0,
                    "trackHdPrice": 0,
                    "trackHdRentalPrice": 0,
                    "releaseDate": "2019-03-19T19:00:00Z",
                    "collectionExplicitness": "notExplicit",
                    "trackExplicitness": "notExplicit",
                    "trackCount": 300,
                    "country": "USA",
                    "currency": "USD",
                    "primaryGenreName": "News & Politics",
                    "artworkUrl600": "https://is4-ssl.mzstatic.com/image/thumb/Music124/v4/5e/ab/72/5eab7235-f01e-81a5-d720-50771ec447b6/source/600x600bb.jpg",
                    "genreIds": ["1311", "26", "1325", "1324"],
                    "genres": [
                        "News & Politics",
                        "Podcasts",
                        "Government & Organizations",
                        "Society & Culture",
                    ],
                }
            ],
        }

        url = feed_url(itunes_data)
        self.assertEqual(url, "https://feeds.megaphone.fm/theweeds")

    def test_find_episode(self):
        feed_url = "https://feeds.megaphone.fm/theweeds"
        podcast = podcastparser.parse(feed_url, path.join(here, "data", "theweeds.rss"))

        title = "The reparations primary"
        stream_url = "https://traffic.megaphone.fm/VMP2975209749.mp3"

        item = utils.find_episode(podcast["episodes"], title, stream_url)

        self.assertEqual(item["guid"], "9aa25a44-ff17-11e8-89e8-dbfe1fc6a68f")
        self.assertEqual(item["total_time"], 3466)
        self.assertEqual(item["published"], 1553022019)


if __name__ == "__main__":
    unittest.main()
