import pytest
import numpy as np
from ...helpers import array_summary


def test_int_array():
    assert (
        array_summary(np.arange(10))
        == """1-D array of length (10,).
    mean:  004.500 
    std:   002.872 
    %_0:   010.000 
    %_nan: 000.000"""
    )


def test_array_of_random_float():
    np.random.seed(123456)
    assert (
        array_summary(np.random.random(1000))
        == """1-D array of length (1000,).
    mean:  000.508 
    std:   000.285 
    %_0:   000.000 
    %_nan: 000.000"""
    )


def test_2d_array_of_int():
    assert (
        array_summary(np.arange(64).reshape((-1, 4)))
        == """2-D array of length (16, 4).
    Index: 001/004     Index: 002/004     Index: 003/004     Index: 004/004 
    mean:  030.000     mean:  031.000     mean:  032.000     mean:  033.000 
    std:   018.439     std:   018.439     std:   018.439     std:   018.439 
    %_0:   006.250     %_0:   000.000     %_0:   000.000     %_0:   000.000 
    %_nan: 000.000     %_nan: 000.000     %_nan: 000.000     %_nan: 000.000"""
    )


def test_2d_of_float():
    np.random.seed(123456)
    assert (
        array_summary(np.random.random((10, 10)))
        == """2-D array of length (10, 10).
    Index: 001/010     Index: 002/010     Index: 003/010     Index: 004/010 
    mean:  000.513     mean:  000.582     mean:  000.353     mean:  000.571 
    std:   000.288     std:   000.300     std:   000.302     std:   000.282 
    %_0:   000.000     %_0:   000.000     %_0:   000.000     %_0:   000.000 
    %_nan: 000.000     %_nan: 000.000     %_nan: 000.000     %_nan: 000.000"""
    )


def test_2d_short_array():
    np.random.seed(123456)
    assert (
        array_summary(np.random.random((10, 2)))
        == """2-D array of length (10, 2).
    Index: 001/002     Index: 002/002 
    mean:  000.349     mean:  000.616 
    std:   000.216     std:   000.274 
    %_0:   000.000     %_0:   000.000 
    %_nan: 000.000     %_nan: 000.000"""
    )
