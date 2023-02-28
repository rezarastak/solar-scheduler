from typing import Iterable, Sequence

from scheduler import personnel, sites, assignments, optimize


def schedule(buildings: Sequence[sites.Building],
             employees: Sequence[personnel.Person]) -> Iterable[assignments.WorkAssignment]:
    return optimize.schedule_simple(buildings, employees)
