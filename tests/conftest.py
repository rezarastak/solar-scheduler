import calendar
from typing import List

import pytest

from scheduler import personnel, sites


@pytest.fixture
def seven_people() -> List[personnel.Person]:
    from scheduler.personnel import CertifiedInstaller, InstallerPendingCertification, Laborer
    return [
        CertifiedInstaller('Luke', [calendar.MONDAY]),
        CertifiedInstaller('Jack'),
        Laborer('Tom'),
        Laborer('Sara'),
        InstallerPendingCertification('Ahmad', [calendar.TUESDAY, calendar.FRIDAY]),
        CertifiedInstaller('Craig'),
        Laborer('Ian', [calendar.FRIDAY])
    ]


@pytest.fixture
def ten_people() -> List[personnel.Person]:
    from scheduler.personnel import CertifiedInstaller, InstallerPendingCertification, Laborer
    return [
        Laborer('Reza'),
        InstallerPendingCertification('Bryan', [calendar.TUESDAY]),
        CertifiedInstaller('Tram', [calendar.WEDNESDAY]),
        CertifiedInstaller('Roy'),
        InstallerPendingCertification('Sara', [calendar.MONDAY, calendar.FRIDAY]),
        Laborer('Marquez'),
        Laborer('Susan'),
        CertifiedInstaller('Donna', [calendar.WEDNESDAY, calendar.THURSDAY]),
        InstallerPendingCertification('Zack'),
        CertifiedInstaller('Matt')
    ]


@pytest.fixture
def six_buildings() -> List[sites.Building]:
    from scheduler.sites import SingleStoryHome, TwoStoryHome, CommercialBuilding
    return [SingleStoryHome('113 Dali Ave'),
            TwoStoryHome('1450 Quillen Ct'),
            SingleStoryHome('198 Gordon Way'),
            CommercialBuilding('Bosch'),
            SingleStoryHome('10002 4th st'),
            SingleStoryHome('98 Crayon Ave')]
