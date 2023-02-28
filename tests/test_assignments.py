import calendar

from scheduler import assignments, sites
from tests.test_personnel import seven_people  # noqa: F401
from tests.test_sites import six_buildings  # noqa: F401


def test_convert_daily_assignment_matrix(seven_people, six_buildings):  # noqa: F811
    work_assignment_matrix = ((1, 0, 0),
                              (1, 1, 0),
                              (1, 0, 0))
    day_work = assignments.convert_personnel_assignment_matrix_to_list(work_assignment_matrix, calendar.WEDNESDAY,
                                                                       six_buildings, seven_people)
    assert len(day_work) == 3
    assert isinstance(day_work[1].building, sites.TwoStoryHome)
    assert day_work[1].workers[1].name == 'Ahmad'
    assert day_work[2].workers[0].name == 'Craig'
