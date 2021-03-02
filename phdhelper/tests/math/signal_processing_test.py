from _pytest.outcomes import OutcomeException
from ...math.signal_processing import autocorrelate
from ...exceptions import phdException as phdE
import numpy as np
import pytest


def load_autocorrelate(ftype="beating"):
    if ftype == "bigarray":
        data = np.load(
            "phdhelper/tests/math/autocorrelate_bigarray.npy", allow_pickle=True
        )
    else:
        data = np.load(
            "phdhelper/tests/math/autocorrelate_beating.npy", allow_pickle=True
        )
    x = data.item().get("input")
    r = data.item().get("output")
    return x, r


def test_autocorrelate_empty():
    assert autocorrelate([]) == []


def test_autocorrelate_numpy_array():
    x, r = load_autocorrelate()
    a = autocorrelate(x)
    print(sum(abs(a - r)))
    assert np.allclose(a, r)


def test_autocorrelate_python_array():
    assert type(autocorrelate([1, 2, 3])) == np.ndarray


def test_autocorrelate_numpy_int_array():
    x, _ = load_autocorrelate()
    x2 = np.round(x).astype(int)
    x3 = np.round(x)
    acorr1 = autocorrelate(x2)
    acorr2 = autocorrelate(x3)
    print(x2)
    print(acorr2)
    print(f"Difference: {sum(abs(acorr1 - acorr2)):.3E}")
    assert np.allclose(autocorrelate(x2), autocorrelate(x3))


def test_autocorrelate_big_array():
    x, r = load_autocorrelate("bigarray")
    assert np.allclose(autocorrelate(x), r)


def test_autocorrelate_stepsTooBig():
    with pytest.raises(phdE.OutOfBoundsException):
        autocorrelate(np.arange(50), steps=100)