def find_episode(episodes, title, stream_url):
    for ep in episodes:
        if ep["title"] == title or ep["enclosures"][0]["url"] == stream_url:
            return ep
    return None
