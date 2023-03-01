import calendar

from scheduler import sites, personnel, schedule


def test_single_building_one_installer():
    building = sites.SingleStoryHome("The owen's house")
    installer = personnel.CertifiedInstaller('Jack', days_not_available=[])
    job_assignments = schedule([building], [installer])
    assert len(job_assignments) == 1
    assert job_assignments[0].building == building


def test_multiple_buildings_not_enough_employees(six_buildings, seven_people):
    job_assignments = schedule(six_buildings, seven_people)
    assert len(job_assignments) == 3
    assert job_assignments[0].day == calendar.MONDAY
    assert job_assignments[1].building.name == '1450 Quillen Ct'
    assert job_assignments[2].workers[0].name == 'Luke'


def test_multiple_buildings_multiple_people(six_buildings, ten_people):
    job_assignments = schedule(six_buildings, ten_people)
    assert len(job_assignments) == 6
    assert job_assignments[0].workers[0].name == 'Tram'
    assert job_assignments[1].day == calendar.MONDAY
    assert job_assignments[2].building.name == '198 Gordon Way'
    assert job_assignments[3].day == calendar.WEDNESDAY
    assert job_assignments[4].day == calendar.THURSDAY
    assert job_assignments[4].workers[0].name == 'Tram'
    assert job_assignments[5].day == calendar.THURSDAY
    assert job_assignments[5].workers[0].name == 'Roy'


def test_no_buildings(seven_people):
    job_assignments = schedule([], seven_people)
    assert job_assignments == []


def test_no_employees(six_buildings):
    job_assignments = schedule(six_buildings, [])
    assert job_assignments == []


def test_5_days_is_not_enough(ten_people):
    buildings = [sites.SingleStoryHome(f'bldg #{i + 1}') for i in range(40)]
    job_assignments = schedule(buildings, ten_people)
    assert len(job_assignments) == 17
    assert job_assignments[0].day == calendar.MONDAY
    assert job_assignments[16].day == calendar.FRIDAY
