import re

from bs4 import BeautifulSoup
from datetime import date, datetime

from exceptions import HTTPError, ScrapeError
from util import load_website


class WikiCFP:
    """
    Utility class for WikiCFP website.
    """

    _WIKICFP_URL_ = "http://www.wikicfp.com/cfp/"

    @staticmethod
    def load_latest_cfp_by_url(url: str):
        """
        Loads the most recent CFP data from direct WikiCFP page.

        :param url: Full URL of the conference detail on WikiCFP (e.g. http://www.wikicfp.com/cfp/program?id=1)
        :return: Triplet of (conference date, submission deadline, conference location)
        :raises ConnectionError: The url cannot be connected to
        :raises HTTPError: Data cannot be loaded for some reason
        :raises ScrapeError: The website downloaded correctly, but scraping it failed
        """

        website = load_website(url)

        soup = BeautifulSoup(website, 'html.parser')
        mainContent = soup.select_one('div.contsec table')
        if mainContent is None:
            raise ScrapeError("Cannot find main content.")

        tables = soup.select_one('div.contsec table').find_all('table')
        cfpTable = None
        for table in tables:
            firstCell = table.tr.td.string
            if (firstCell is not None) and (firstCell.strip() == "Event"):
                cfpTable = table
        if cfpTable is None:
            raise ScrapeError("Cannot find the table with CFP details")

        rows = cfpTable.find_all('tr')
        if rows is None or len(rows) < 3:
            raise ScrapeError("Malformed table with CFP details")

        cells = rows[2].find_all('td')
        if cells is None or len(cells) < 3:
            raise ScrapeError("Malformed CFP detail row, missing data cells")

        conferenceDate = cells[0].string.strip() if cells[0].string is not None else None
        if conferenceDate is not None:
            confDates = conferenceDate.split(' - ')
            if len(confDates) > 1:
                try:
                    confDateFrom = datetime.strptime(confDates[0], "%b %d, %Y").date()
                    confDateTo = datetime.strptime(confDates[1], "%b %d, %Y").date()
                    conferenceDate = (confDateFrom, confDateTo)
                except ValueError:
                    pass

        submissionDeadline = cells[2].string.strip() if cells[2].string is not None else None
        abstractRegistration = None
        if submissionDeadline is not None:
            try:
                res = re.search(r'([a-zA-Z]+ \d+, \d+)\s+\(([a-zA-Z]+ \d+, \d+)\)', submissionDeadline)
                if res is not None:
                    submissionDeadline = datetime.strptime(res.group(1), "%b %d, %Y").date()
                    abstractRegistration = datetime.strptime(res.group(2), "%b %d, %Y").date()
                else:
                    submissionDeadline = datetime.strptime(submissionDeadline, "%b %d, %Y").date()
            except ValueError:
                pass

        conferenceLocation = cells[1].string.strip() if cells[1].string is not None else None

        return conferenceDate, submissionDeadline, abstractRegistration, conferenceLocation
