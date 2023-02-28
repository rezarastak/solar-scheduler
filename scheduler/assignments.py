from dataclasses import dataclass
from typing import Sequence, NamedTuple

from scheduler import sites, personnel


@dataclass
class WorkAssignment:
    day: int
    building: sites.Building
    workers: Sequence[personnel.Person]


class BuildingRequirements(NamedTuple):
    n_certified_installer: int = 0
    n_installer_pending_certification: int = 0
    n_any_installer: int = 0
    n_any_laborer: int = 0


building_requirement_sum_indices = [
    # certified-installer   installer-pending-certification   laborer
    (1,                     0,                                0),      # certified installer
    (0,                     1,                                0),      # installer pending certification
    (1,                     1,                                0),      # any installer
    (1,                     1,                                1),      # any laborer
]


building_requirements_map = {
    sites.SingleStoryHome: BuildingRequirements(n_certified_installer=1, n_any_installer=1, n_any_laborer=1),
    sites.TwoStoryHome: BuildingRequirements(n_certified_installer=1, n_any_installer=2, n_any_laborer=2),
    sites.CommercialBuilding: BuildingRequirements(n_certified_installer=2, n_installer_pending_certification=2,
                                                   n_any_installer=4, n_any_laborer=8)
}


def convert_personnel_assignment_matrix_to_list(assignment_matrix, day: int,
                                                buildings: Sequence[sites.Building],
                                                employees: Sequence[personnel.Person]) -> Sequence[WorkAssignment]:
    available_personnel = [p for p in employees if personnel.is_available(p, day)]
    result = []
    for i, employee_count in enumerate(assignment_matrix):
        assigned_personnel, available_personnel = personnel.get_a_few_people_from_list(available_personnel,
                                                                                       employee_count)
        result.append(WorkAssignment(day, buildings[i], assigned_personnel))
    return result
