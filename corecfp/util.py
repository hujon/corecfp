import logging
import time
import requests

from exceptions import HTTPError


__logger = logging.getLogger('__main__')


def load_website(url: str, params=None, attempt: int = 1) -> bytes:
    """
    Loads content of a website specified by URL.

    :param url: Full URL of the website which should be loaded
    :param params: URL parameters that should be sent with the request
    :param attempt: Counter of attempts, which is used to limit the retries to 10 maximum.
    :return: Website content packed in bytes array
    :raises ConnectionError: The url cannot be connected to
    :raises HTTPError: Data cannot be loaded for some reason
    """
    try:
        website = requests.get(url, params)
        website.raise_for_status()
    except (ConnectionError, requests.exceptions.ConnectionError) as error:
        raise ConnectionError(str(error))
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 429:  # Too many requests
            if attempt <= 10:
                __logger.warning(f"Connection failed because the request limit was reached. Retry {attempt}")
                attempt += 1
                time.sleep(attempt * 2)  # throttle down to bypass request limits
                return load_website(url, params, attempt)
            else:
                raise HTTPError(str(error))
        else:
            raise HTTPError(str(error))
    return website.content
