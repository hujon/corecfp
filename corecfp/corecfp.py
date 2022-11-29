import bisect
import datetime
import logging
import sys

from conference import Conference
from core import Core
from datetime import date
from dblp import Dblp
from wikicfp import WikiCFP

from exceptions import ScrapeError, HTTPError


class CoreCFP:

    conferences: list[Conference] = []

    def __init__(self):
        self._logger = logging.getLogger('__main__')
        core = Core()

        core.load_conferences()
        confNo = 0
        confCNT = len(core.conferences)
        for coreConference in core.conferences:
            confNo += 1
            conference = Conference(
                core_id=coreConference.id,
                acronym=coreConference.acronym,
                name=coreConference.name,
                rank=coreConference.rank,
                rank_src=coreConference.rank_src,
                dblp_link=coreConference.dblp
            )
            if conference.dblp_link is not None:
                self._logger.info(f"Scraping additional info for {confNo}/{confCNT} ({conference.name})")
                try:
                    conference.wikicfp_link = Dblp.find_wikicfp_by_url(conference.dblp_link)
                except (ConnectionError, HTTPError, ScrapeError) as error:
                    self._logger.error(str(error))

            if conference.wikicfp_link is not None:
                try:
                    conference.date, conference.submission, conference.abstract_reg, conference.location = \
                        WikiCFP.load_latest_cfp_by_url(conference.wikicfp_link)
                except (ConnectionError, HTTPError, ScrapeError) as error:
                    self._logger.error(str(error))

            self.conferences.append(conference)

    def upcoming(self, date_from: datetime.date = datetime.date.today()):
        """
        Returns upcoming conferences (based on submission/abstract registration deadline)

        :param date_from: Earliest deadline date which shall appear in the result
        :return: List of conferences with submission/abstract registration from the specified date
        """
        conferences = sorted(self.conferences, key=Conference.upcoming_key)
        idx = bisect.bisect_left(conferences, date_from, key=Conference.upcoming_key)
        return conferences[idx:]


if __name__ == '__main__':
    import csv

    logger = logging.getLogger('__main__')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    corecfp = CoreCFP()
    writer = csv.writer(sys.stdout)
    writer.writerow([
        'Acronym',
        'Name',
        'Rank',
        'Dates',
        'Submission deadline',
        'Abstract registration',
        'Location',
        'Rank source',
        'CORE ID',
        'DBLP',
        'WikiCFP',
    ])
    for conf in corecfp.upcoming():
        dates = f"{conf.date[0].isoformat()} - {conf.date[1].isoformat()}" if type(conf.date) is tuple else conf.date
        submission = conf.submission.isoformat() if isinstance(conf.submission, date) else conf.submission
        abstract_reg = conf.abstract_reg.isoformat() if isinstance(conf.abstract_reg, date) else conf.abstract_reg
        writer.writerow([
            conf.acronym,
            conf.name,
            conf.rank,
            dates,
            submission,
            abstract_reg,
            conf.location,
            conf.rank_src,
            conf.core_id,
            conf.dblp_link,
            conf.wikicfp_link,
        ])
