# ruff: noqa: INP001,ANN001,ANN201,PTH118,PTH120,PTH123

import unittest
from os import path

import podcastparser

from overcast_parser import OvercastParser, utils
from overcast_parser.itunes_podcast_rss.extract import _feed_url

here = path.dirname(__file__)


class TestOvercastParser(unittest.TestCase):
    def test_parse_overcast(self):
        parser = OvercastParser()

        with open(path.join(here, "data", "overcast.htm")) as f:
            data = f.read()

        (
            itunes_id,
            stream_url,
            overcast_id,
            ep_title,
            feed_url,
        ) = parser.parse_overcast(data)

        self.assertEqual(itunes_id, 1602541473)
        self.assertEqual(
            stream_url,
            "https://chtbl.com/track/39E17/podtrac.com/pts/redirect.mp3/"
            "pdrl.fm/060f2a/traffic.omny.fm/d/clips/e73c998e-6e60-432f-8610-ae210140c5b1/"
            "32c25e85-1667-4acb-99fd-ae3c0021f33e/299405db-0bc5-4924-8c60-b10f0154960a/"
            "audio.mp3?utm_source=Podcast&in_playlist=beacef48-19d2-4f52-b9e8-ae3c0021f347",
        )
        self.assertEqual(overcast_id, 4023019428512817)
        self.assertEqual(ep_title, "Using AI to Help Doctors Save Lives")
        self.assertEqual(
            feed_url,
            "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/"
            "32c25e85-1667-4acb-99fd-ae3c0021f33e/beacef48-19d2-4f52-b9e8-ae3c0021f347/podcast.rss",
        )

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
                },
            ],
        }

        url = _feed_url(itunes_data)
        self.assertEqual(url, "https://feeds.megaphone.fm/theweeds")

    def test_find_episode(self):
        podcast = podcastparser.parse(
            url="https://feeds.megaphone.fm/theweeds",
            stream=path.join(here, "data", "theweeds.rss"),
        )

        title = "The reparations primary"
        stream_url = "https://traffic.megaphone.fm/VMP2975209749.mp3"

        item = utils.find_episode(podcast["episodes"], title, stream_url)

        self.assertEqual(item["guid"], "9aa25a44-ff17-11e8-89e8-dbfe1fc6a68f")
        self.assertEqual(item["total_time"], 3466)
        self.assertEqual(item["published"], 1553022019)


if __name__ == "__main__":
    unittest.main()
