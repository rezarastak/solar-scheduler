# solar-scheduler
Python package for scheduling solar installations.

## Install prerequisite libraries

To properly install the convex optimization library, please use anaconda:

```
conda create --name scheduler_env
conda activate scheduler_env
conda install -c conda-forge cvxpy
```

## Code example

In order to familiarize yourself with the code, please look at the contents on `tests/test_schedule.py`.
This file contains many code examples which you can use to schedule the solar installations.
For more information about test fixtures defined in this repository, you can look at `tests/conftest.py`.

To use the functionality of this codebase in your python code, you can use the `schedule` function as follows:

```python
from calendar import MONDAY, WEDNESDAY
from scheduler.sites import SingleStoryHome, TwoStoryHome, CommercialBuilding
from scheduler.personnel import CertifiedInstaller, InstallerPendingCertification, Laborer
from scheduler import schedule

buildings = [SingleStoryHome('Home1'), TwoStoryHome('Home2'), CommercialBuilding('office')]
employees = [CertifiedInstaller('Jack'), CertifiedInstaller('Bob', days_not_available=[MONDAY]),
             InstallerPendingCertification('Sara'), InstallerPendingCertification('Larry'),
             Laborer('Andy'), Laborer('Dominic', days_not_available=[WEDNESDAY]), Laborer('Ray'), Laborer('Tom')]
work_assignments = schedule(buildings, employees)
for work in work_assignments:
    print(work)
```

The output of this program is as follows:
```
WorkAssignment(day=0, building=SingleStoryHome(name='Home1'), workers=[CertifiedInstaller(name='Jack', days_not_available=[])])
WorkAssignment(day=1, building=TwoStoryHome(name='Home2'), workers=[CertifiedInstaller(name='Jack', days_not_available=[]), CertifiedInstaller(name='Bob', days_not_available=[0])])
(scheduler_env) root@b9cf03e74357:/solar# python example.py 
WorkAssignment(day=0, building=SingleStoryHome(name='Home1'), workers=[CertifiedInstaller(name='Jack', days_not_available=[])])
WorkAssignment(day=1, building=TwoStoryHome(name='Home2'), workers=[CertifiedInstaller(name='Jack', days_not_available=[]), CertifiedInstaller(name='Bob', days_not_available=[0])])
WorkAssignment(day=3, building=CommercialBuilding(name='office'), workers=[CertifiedInstaller(name='Jack', days_not_available=[]), CertifiedInstaller(name='Bob', days_not_available=[0]), InstallerPendingCertification(name='Sara', days_not_available=[]), InstallerPendingCertification(name='Larry', days_not_available=[]), Laborer(name='Andy', days_not_available=[]), Laborer(name='Dominic', days_not_available=[2]), Laborer(name='Ray', days_not_available=[]), Laborer(name='Tom', days_not_available=[])])
```


## Running tests

First, make sure you have installed all of the necessary dependencies, then run the unittests, linters, and static type analysis.

```
conda install --file requirements-dev.txt
pytest --cov=.
flake8
mypy .
```