from typing import Iterable, List, Sequence

import cvxpy as cp
import numpy as np

from scheduler.workdays import workdays_this_week
from scheduler.sites import Building
from scheduler.personnel import Person, get_personnal_count_for_day, get_daily_capacity_matrix
from scheduler.assignments import WorkAssignment, building_requirements_map, building_requirement_sum_indices, \
    convert_personnel_assignment_matrix_to_list


def schedule_cvxpy_separate_for_each_day(buildings: Sequence[Building],
                                         employees: Sequence[Person]) -> Iterable[WorkAssignment]:
    result: List[WorkAssignment] = []
    print(buildings)
    print(employees)
    rest_of_buildings = list(buildings)
    for day in workdays_this_week:
        print(f'{day = }')
        if not rest_of_buildings:
            break
        personnel_count = get_personnal_count_for_day(employees, day)
        print(f'{personnel_count = }')
        one_day_assignment = cvxpy_schedule_one_day(rest_of_buildings, personnel_count)
        print(f'{one_day_assignment = }')
        result.extend(convert_personnel_assignment_matrix_to_list(one_day_assignment, day, rest_of_buildings,
                                                                  employees))
        rest_of_buildings = rest_of_buildings[len(one_day_assignment):]
        print(f'{rest_of_buildings = }')
    return result


def cvxpy_schedule_one_day(buildings, employee_count):
    n_building_to_finish_in_one_day = employee_count[0]
    one_day_assignment = get_daily_optimization_result(buildings[:n_building_to_finish_in_one_day], employee_count)
    estimated_n_building_too_high = one_day_assignment is None
    if estimated_n_building_too_high:
        while one_day_assignment is None:
            n_building_to_finish_in_one_day -= 1
            print(f"{n_building_to_finish_in_one_day = }")
            one_day_assignment = get_daily_optimization_result(buildings[:n_building_to_finish_in_one_day],
                                                               employee_count)
    else:
        new_one_day_assignment = one_day_assignment
        while new_one_day_assignment is not None and n_building_to_finish_in_one_day <= len(buildings):
            one_day_assignment = new_one_day_assignment
            n_building_to_finish_in_one_day += 1
            print(f"{n_building_to_finish_in_one_day = }")
            new_one_day_assignment = get_daily_optimization_result(buildings[:n_building_to_finish_in_one_day],
                                                                   employee_count)
    return one_day_assignment


def get_daily_optimization_result(buildings, employee_count):
    n_building = len(buildings)
    if n_building == 0:
        return []
    n_person_type = 3
    person_building_assignment = cp.Variable((n_building, n_person_type), integer=True)
    total_employee_constraint = cp.sum(person_building_assignment, axis=0) <= np.array(employee_count)
    nonnegative_constraint = person_building_assignment >= 0
    building_employee_requirements = np.zeros((n_building, 4))
    for i, building in enumerate(buildings):
        building_employee_requirements[i, :] = building_requirements_map[type(building)]
    linear_transformer = np.array(building_requirement_sum_indices).transpose()
    building_requirements_constraint = \
        person_building_assignment @ linear_transformer >= building_employee_requirements
    optimization_problem = cp.Problem(objective=cp.Minimize(cp.sum(person_building_assignment)),
                                      constraints=[total_employee_constraint, building_requirements_constraint,
                                                   nonnegative_constraint])
    if n_building == 1:
        print(f'  {employee_count = }')
        print(f'  {linear_transformer = }')
        print(f'  {building_employee_requirements = }')
    optimization_problem.solve(verbose=False)
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
