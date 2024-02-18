def find_episode(episodes: dict, title: str, stream_url: str) -> dict | None:
    for ep in episodes:
        if ep["title"] == title or ep["enclosures"][0]["url"] == stream_url:
            return ep
    return None
