import pytest

from scheduler.sites import SingleStoryHome, TwoStoryHome, CommercialBuilding


@pytest.fixture
def six_buildings():
    return [SingleStoryHome('113 Dali Ave'),
            TwoStoryHome('1450 Quillen Ct'),
            SingleStoryHome('198 Gordon Way'),
            CommercialBuilding('Bosch'),
            SingleStoryHome('10002 4th st'),
            SingleStoryHome('98 Crayon Ave')]
