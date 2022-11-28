import logging
import re
import requests

from bs4 import BeautifulSoup
from dataclasses import dataclass

from exceptions import HTTPError, ScrapeError
from util import load_website


@dataclass
class CoreConference:
    """
    Represents data about a conference available from CORE website.
    """
    id: int
    """ CORE identifier of the conference """

    name: str
    """ Full name of the conference """

    acronym: str = None
    """ Conference acronym """

    rank: str = None
    """ Rank of the conference """

    rank_src: str = None
    """ Source in which was the conference ranked """

    dblp: str = None
    """ Link to the DBLP conference database """


class Core:
    """
    Utility class for CORE conference ranking portal.
    """

    _CORE_URL_ = 'http://portal.core.edu.au/conf-ranks/'
    _SEARCH_BY_ = 'all'
    _SORT_ = 'arank'
    _SOURCE_ = 'all'

    conferences: list[CoreConference] = []
    """ List of all conferences available through the CORE portal """

    def __init__(
        self,
        url: str = _CORE_URL_,
        search: str = None,
        search_by: str = _SEARCH_BY_,
        sort: str = _SORT_,
        source: str = _SOURCE_
    ):
        """
        Initializes the CORE class.

        :param url: URL of the conference ranks portal (Default: http://portal.core.edu.au/conf-ranks/)
        :param search: Search string which will be used to filter only matching conferences,
               if None do not filter the result set (Default: None)
        :param search_by: Identifier of the field that should match the search term. Available identifiers:
               [all, title, acronym, rank, for] (Default: all)
        :param sort: Defines the field which should the result set be sorted upon.
                     Prefix defines the direction (a = AZ direction, d = ZA direction) while the rest
                     defines the field [title, acronym, source, rank, dblp, changed, for1, comment, rating].
                     (Default: arank)
        :param source: The ranking source which shall be checked [all, CORE{YEAR}, ERA2010]. (Default: all)
        """

        self._url = url
        self._search = search
        self._search_by = search_by
        self._sort = sort
        self._source = source

        self._logger = logging.getLogger('__main__')

    def load_conferences(self):
        """
        Scrapes the CORE website and loads the conference data into self.conferences

        :raises ConnectionError: Connection to the CORE ranking portal failed.
        :raises HTTPError: Data cannot be loaded for some reason
        :raises ScrapeError: The website downloaded correctly, but scraping it failed
        """
        self._logger.info('Starting the CORE conference scrape')
        self.conferences.clear()

        website = load_website(self._url, params={
            'search': self._search,
            'by': self._search_by,
            'sort': self._sort,
            'source': self._source
        })

        soup = BeautifulSoup(website, 'html.parser')

        # Get information about number of conferences
        totalConfCnt = None
        searchForm = soup.select_one('form#searchform')
        sumText = None
        for searchFormText in searchForm.stripped_strings:
            sumText = searchFormText
        try:
            summary = re.search(
                r'Showing results \d+ - \d+ of (\d+)',
                sumText
            )
            totalConfCnt = int(summary.group(1))
        except (TypeError, AttributeError):
            self._logger.warning("Cannot load CORE conference summary, will try to continue blind")
        else:
            self._logger.info("Found " + str(totalConfCnt) + " CORE ranked conferences in total")

        # Parse current page
        conf_tbl = soup.find('table')
        if conf_tbl is None:
            raise ScrapeError("Cannot find the conferences table")

        self._parse_conf_table(conf_tbl)
        self._logger.info(
            f"Scraped {str(len(self.conferences))}/{str(totalConfCnt)} CORE ranked conferences"
            if totalConfCnt is not None else
            f"Scraped {str(len(self.conferences))} CORE ranked conferences"
        )

        # Parse other pages
        searchDiv = soup.select_one('div#search')
        if searchDiv is None:
            raise ScrapeError("Cannot find the search div with pagination")

        links = searchDiv.find_all('a')
        for link in links:
            page = re.search(r'jumpPage\(\'(\d+)\'\)', link.get('href'))
            if page is not None:
                self._parse_conf_page(int(page.group(1)))
                self._logger.info(
                    f"Scraped {str(len(self.conferences))}/{str(totalConfCnt)} CORE ranked conferences"
                    if totalConfCnt is not None else
                    f"Scraped {str(len(self.conferences))} CORE ranked conferences"
                )

    def _parse_conf_page(self, page: int):
        """
        Scrapes one page with conferences and loads the conference data into self.conferences

        :param page: The number of the page which should be parsed
        :raises ConnectionError: Connection to the CORE ranking portal failed
        :raises HTTPError: Data cannot be loaded for some reason
        :raises ScrapeError: The website downloaded correctly, but scraping it failed
        """

        website = load_website(self._url, params={
            'search': self._search,
            'by': self._search_by,
            'sort': self._sort,
            'source': self._source,
            'page': page
        })

        soup = BeautifulSoup(website, 'html.parser')

        conf_tbl = soup.find('table')
        if conf_tbl is None:
            raise ScrapeError("Cannot find the conferences table")

        self._parse_conf_table(conf_tbl)

    def _parse_conf_table(self, table: BeautifulSoup):
        rows = table.find_all('tr')
        if rows is None:
            raise ScrapeError("The conference table does not contain any rows")

        rowIter = iter(rows)
        next(rowIter)  # Skip table head
        for row in rowIter:
            detailLink = row.get('onclick')
            if detailLink is None:
                raise ScrapeError("Cannot find the CORE ID")
            res = re.search(
                r'(\d+)/\'\)$',
                detailLink
            )
            if res is None:
                raise ScrapeError("Cannot find the CORE ID")

            core_id = res.group(1)

            cells = row.select('td')
            if cells is None:
                raise ScrapeError("The conference detail row does not contain any cells")
            if len(cells) < 5:
                raise ScrapeError("The conference detail row does not contain enough cells")

            conf_name = cells[0].string.strip() if cells[0].string is not None else None
            if (conf_name is None) or conf_name == "":
                raise ScrapeError("Missing conference name")

            conf_acronym = cells[1].string.strip() if cells[1].string is not None else None
            conf_rank = cells[3].string.strip() if cells[2].string is not None else None
            conf_rank_src = cells[2].string.strip() if cells[3].string is not None else None

            conf_dblp = cells[4].find('a')
            conf_dblp_link = conf_dblp.get('href') if conf_dblp is not None else None

            self.conferences.append(
                CoreConference(
                    int(core_id),
                    conf_name,
                    conf_acronym,
                    rank=conf_rank,
                    rank_src=conf_rank_src,
                    dblp=conf_dblp_link
                )
            )
