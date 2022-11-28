import requests


class HTTPError(requests.exceptions.HTTPError):
    pass


class ScrapeError(RuntimeError):
    pass
