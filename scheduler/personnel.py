from collections import Counter
import dataclasses
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Protocol, Tuple


class Person(Protocol):
    name: str
    days_not_available: Sequence[int]


@dataclass
class CertifiedInstaller:
    name: str
    days_not_available: Sequence[int] = dataclasses.field(default_factory=list)


@dataclass
class InstallerPendingCertification:
    name: str
    days_not_available: Sequence[int] = dataclasses.field(default_factory=list)


@dataclass
class Laborer:
    name: str
    days_not_available: Sequence[int] = dataclasses.field(default_factory=list)


def is_available(person: Person, day: int) -> bool:
    return day not in person.days_not_available


def get_personnel_count_for_day(persons: Iterable[Person], day: int) -> Tuple[int, int, int]:
    return get_personnel_count(filter(lambda p: is_available(p, day), persons))


def get_personnel_count(persons: Iterable[Person]) -> Tuple[int, int, int]:
    result: Dict = Counter()
    for person in persons:
        result[type(person)] += 1
    return result[CertifiedInstaller], result[InstallerPendingCertification], result[Laborer]


def get_a_few_people_from_list(persons: Iterable[Person], count: Tuple[int, int, int]) -> Tuple[List[Person],
                                                                                                List[Person]]:
    found = []
    rest = []
    remaining = {CertifiedInstaller: count[0], InstallerPendingCertification: count[1], Laborer: count[2]}
    for person in persons:
        person_type = type(person)
        if remaining[person_type] > 0:
            found.append(person)
            remaining[person_type] -= 1
        else:
            rest.append(person)
    return found, rest


def get_daily_capacity_matrix(persons: Sequence[Person], days: Sequence[int]):
    return [get_personnel_count_for_day(persons, day) for day in days]
