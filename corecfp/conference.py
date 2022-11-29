import datetime

from dataclasses import dataclass


@dataclass
class Conference:
    core_id: int
    name: str
    acronym: str = None
    date: str | tuple[datetime.date, datetime.date] = None
    location: str = None
    submission: datetime.date = None
    abstract_reg: datetime.date = None
    rank: str = None
    rank_src: str = None
    dblp_link: str = None
    wikicfp_link: str = None

    @staticmethod
    def upcoming_key(conference: 'Conference') -> datetime.date:
        if isinstance(conference.abstract_reg, datetime.date):
            return conference.abstract_reg

        if isinstance(conference.submission, datetime.date):
            return conference.submission

        return datetime.date(datetime.MINYEAR, 1, 1)
