import pytest
from scheduler import sites, personnel
from scheduler.optimize import schedule_simple, schedule_cvxpy_separate_for_each_day


@pytest.fixture(params=[schedule_simple, schedule_cvxpy_separate_for_each_day])
def schedule(request):
    return request.param


def test_single_building_one_installer(schedule):
    building = sites.SingleStoryHome("The owen's house")
    installer = personnel.CertifiedInstaller('Jack', days_not_available=[])
    job_assignments = schedule([building], [installer])
    assert len(job_assignments) == 1
    assert job_assignments[0].building == building
