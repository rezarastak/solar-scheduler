from dataclasses import dataclass
from typing import Protocol


class Building(Protocol):
    name: str


@dataclass
class SingleStoryHome:
    name: str


@dataclass
class TwoStoryHome:
    name: str


@dataclass
class CommercialBuilding:
    name: str
