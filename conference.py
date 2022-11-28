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
