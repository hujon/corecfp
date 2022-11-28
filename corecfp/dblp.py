import re

from bs4 import BeautifulSoup
from exceptions import HTTPError, ScrapeError
from util import load_website


class Dblp:
    """
    Utility class for DBLP website.

    Unfortunately DBLP provides only a limited search API, which does not contain venue details, so this class parses
    the information directly from the website.
    TODO: Once DBLP provides a more complete API, rewrite to load data via API and not scrape the web.
    """

    _DBLP_URL_ = 'https://dblp.uni-trier.de/'

    @staticmethod
    def find_wikicfp_by_url(url: str):
        """

        :param url: Full URL of the conference detail on DBLP (e.g. https://dblp.uni-trier.de/db/conf/yourconf)
        :return: URL of the WikiCFP page or None if WikiCFP wasn't found
        :raises ConnectionError: The url cannot be connected to
        :raises HTTPError: Data cannot be loaded for some reason
        :raises ScrapeError: The website downloaded correctly, but scraping it failed
        """

        website = load_website(url)

        soup = BeautifulSoup(website, 'html.parser')
        navigation = soup.select_one('header#headline nav.head')
        if navigation is None:
            raise ScrapeError("Cannot find the navigation menu for the conference.")

        visit_menu = navigation.select_one('li.visit')
        if visit_menu is None:
            return None

        wikicfp = None
        for visit_link in visit_menu.find_all('a'):
            res = re.search(r'www\.wikicfp\.com', visit_link['href'])
            if res is not None:
                wikicfp = res.string
                break

        return wikicfp
