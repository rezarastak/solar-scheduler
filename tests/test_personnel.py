import calendar
from typing import List

import numpy as np

from scheduler.personnel import Person, get_personnal_count_for_day, get_personnal_count, get_a_few_people_from_list, \
    get_daily_capacity_matrix


def test_get_people_count_on_a_day(seven_people: List[Person]):
    assert get_personnal_count_for_day(seven_people, calendar.MONDAY) == (2, 1, 3)
    assert get_personnal_count_for_day(seven_people, calendar.TUESDAY) == (3, 0, 3)
    assert get_personnal_count_for_day(seven_people, calendar.WEDNESDAY) == (3, 1, 3)
    assert get_personnal_count_for_day(seven_people, calendar.FRIDAY) == (3, 0, 2)


def test_get_a_few_people(seven_people: List[Person]):
    found, rest = get_a_few_people_from_list(seven_people, (1, 0, 2))
    assert len(found) == 3
    assert len(rest) == 4
    assert get_personnal_count(found) == (1, 0, 2)
    assert get_personnal_count(rest) == (2, 1, 1)


def test_daily_capacity_matrix(seven_people: List[Person]):
    capacity_matrix = get_daily_capacity_matrix(seven_people, [calendar.MONDAY, calendar.WEDNESDAY])
    assert np.array_equal(capacity_matrix, ((2, 1, 3), (3, 1, 3)))
