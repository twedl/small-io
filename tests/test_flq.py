import numpy as np
import pandas as pd

from small_io.flq import cilq_matrix, flq_lambda, flq_matrix, regionalize


def test_cilq_uses_slq_on_diagonal():
    slq = pd.Series([0.5, 2.0], index=["a", "b"])
    m = cilq_matrix(slq)
    assert m.loc["a", "b"] == 0.25
    assert m.loc["b", "a"] == 4.0
    assert m.loc["a", "a"] == 0.5 and m.loc["b", "b"] == 2.0


def test_lambda_is_one_for_whole_nation_and_with_delta_zero():
    assert flq_lambda(1.0, 0.3) == 1.0
    assert flq_lambda(0.02, 0.0) == 1.0
    assert flq_lambda(0.02, 0.3) < flq_lambda(0.4, 0.3) < 1.0


def test_regionalize_caps_quotient_at_one():
    A = pd.DataFrame([[0.2, 0.1], [0.3, 0.4]], index=["a", "b"], columns=["a", "b"])
    slq = pd.Series([0.5, 2.0], index=["a", "b"])
    r = regionalize(A, flq_matrix(slq, region_share=1.0, delta=0.3))
    expected = A.to_numpy() * np.array([[0.5, 0.25], [1.0, 1.0]])
    np.testing.assert_allclose(r.to_numpy(), expected)


def test_seller_and_buyer_both_absent_gives_zero():
    slq = pd.Series([0.0, 0.0, 1.0], index=["a", "b", "c"])
    m = cilq_matrix(slq)
    assert m.loc["a", "b"] == 0.0
    assert np.isinf(m.loc["c", "a"])
