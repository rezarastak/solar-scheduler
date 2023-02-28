import cvxpy as cp
import numpy as np


def test_linear_integer_programming():
    x = cp.Variable(4, integer=True)
    problem = cp.Problem(cp.Maximize(x[1]), [x <= 1, x >= 0])
    problem.solve()
    assert np.array_equal(x.value, [0, 1, 0, 0])
