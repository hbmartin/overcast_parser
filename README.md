# Overcast URL to podcast information
Python library to obtain RSS feed URL from Overcast link, built especially for Pythonista

## Installation / Upgrade

```
pip install overcast_parser --upgrade
```

## Usage
#### See demo.py for full pythonista script
```
from overcast_parser.OvercastParser import OvercastParser
parser = OvercastParser()
data = requests.get(overcast_url).text
parser.feed(data)
(itunes_id, stream_url, overcast_id, title) = parser.close()
print(title)
```

## Built With

* [itunes_podcast_rss](https://github.com/wotaen/itunes_podcast_rss) - obtain RSS feed URL from iTunes link
* [pyPodcastParser](https://github.com/jrigden/pyPodcastParser) - parsing podcast RSS feeds

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Code Formatting

This project is linted with [pyflakes](https://github.com/PyCQA/pyflakes) and makes strict use of [Black](https://github.com/ambv/black) for code formatting.

## Authors

* [Harold Martin](https://www.linkedin.com/in/harold-martin-98526971/) - harold.martin at gmail


## License

[MIT](LICENSE.txt)