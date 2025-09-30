from coding_challenges_core import limits
import pytest

def test_limits_preprocessing_statements():
    src = """
a = 1
b = 2
c = a + b
print(c)
"""
    lim = limits.Limits(max_statements=3)
    with pytest.raises(ValueError, match="exceeding the limit"):
        limits.validate(lim, src)
    lim = limits.Limits(max_statements=5)
    limits.validate(lim, src) # should not raise

def test_limits_preprocessing_imports():
    src = """
import math
import os as operating_system
from statistics import mean
"""
    lim = limits.Limits(allowed_imports=['math'])
    with pytest.raises(ValueError, match="not allowed"):
        limits.validate(lim, src)
    lim = limits.Limits(allowed_imports=['statistics', 'math', 'os'])
    limits.validate(lim, src)  # should not raise


