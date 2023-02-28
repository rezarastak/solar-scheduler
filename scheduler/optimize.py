import calendar
from typing import Iterable, List, Sequence

import cvxpy as cp
import numpy as np

from scheduler.workdays import workdays_this_week
from scheduler.sites import Building
from scheduler.personnel import Person, get_personnal_count_for_day, get_daily_capacity_matrix
from scheduler.assignments import WorkAssignment, building_requirements_map, building_requirement_sum_indices, \
    convert_personnel_assignment_matrix_to_list


def schedule_simple(buildings: Sequence[Building], employees: Sequence[Person]) -> Iterable[WorkAssignment]:
    return [WorkAssignment(calendar.MONDAY, buildings[0], employees)]


def schedule_cvxpy_separate_for_each_day(buildings: Sequence[Building],
                                         employees: Sequence[Person]) -> Iterable[WorkAssignment]:
    result: List[WorkAssignment] = []
    rest_of_buildings = list(buildings)
    for day in workdays_this_week:
        if not rest_of_buildings:
            break
        personnel_count = get_personnal_count_for_day(employees, day)
        one_day_assignment = cvxpy_schedule_one_day(rest_of_buildings, personnel_count)
        result.extend(convert_personnel_assignment_matrix_to_list(one_day_assignment, day, rest_of_buildings,
                                                                  employees))
        rest_of_buildings = rest_of_buildings[len(one_day_assignment):]
    return result


def cvxpy_schedule_one_day(buildings, employee_count):
    n_person_type = 3
    n_building = len(buildings)
    person_building_assignment = cp.Variable((n_building, n_person_type), integer=True)
    total_employee_constraint = cp.sum(person_building_assignment, axis=0) <= np.array(employee_count)
    building_employee_requirements = np.zeros((n_building, 4))
    for i, building in enumerate(buildings):
        building_employee_requirements[i, :] = building_requirements_map[type(building)]
    linear_transformer = np.array(building_requirement_sum_indices).transpose()
    building_requirements_constraint = \
        person_building_assignment @ linear_transformer == building_employee_requirements
    optimization_problem = cp.Problem(cp.Maximize(0), [total_employee_constraint, building_requirements_constraint])
    optimization_problem.solve(verbose=True)
    assert optimization_problem.status == 'optimal'
    return person_building_assignment.value


def cvxpy_schedule_all_at_once(buildings: Sequence[Building],
                               employees: Sequence[Person]) -> Iterable[WorkAssignment]:
    '''This algorithm uses the cvxpy library to solve for all days at once.
    However, this solution did not work because the resulting optimization algorithm was not convex.
    '''
    n_building = len(buildings)
    n_person_type = 3
    n_day = len(workdays_this_week)
    person_building_assignment = cp.Variable((n_building, n_person_type), integer=True)
    building_day_assignment = cp.Variable((n_day, n_building), boolean=True)
    building_employee_requirements = np.zeros((n_building, 4))
    for i, building in enumerate(buildings):
        building_employee_requirements[i, :] = building_requirements_map[type(building)]
    linear_transformer = np.array(building_requirement_sum_indices).transpose()
    building_requirements_constraint = \
        person_building_assignment @ linear_transformer == building_employee_requirements
    daily_capacity_matrix = np.array(get_daily_capacity_matrix(employees, workdays_this_week))
    print(building_day_assignment.shape)
    print(person_building_assignment.shape)
    print(daily_capacity_matrix)
    day_constraint = (building_day_assignment @ person_building_assignment) <= daily_capacity_matrix
    day_priorities = np.arange(n_day)
    building_priorities = np.arange(n_building, 0, -1)
    objective = cp.Minimize(day_priorities @ building_day_assignment @ building_priorities)
    problem = cp.Problem(objective, [building_requirements_constraint, day_constraint])
    problem.solve()
    assert problem.status == 'optimal'
    return building_day_assignment.value, person_building_assignment.value
