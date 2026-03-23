import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline.analysis import mean, median, std_dev, value_distribution, disease_rate_by_group

# test 1 — mean simple
def test_mean_simple():
    result = mean([1, 2, 3, 4, 5])
    if result == 3.0:
        print("test 1 passed")
    else:
        print("test 1 FAILED")

# test 2 — mean with nones
def test_mean_with_nones():
    result = mean([1, None, 3, None, 5])
    if result == 3.0:
        print("test 2 passed")
    else:
        print("test 2 FAILED")

# test 3 — mean empty list
def test_mean_empty_list():
    result = mean([])
    if result is None:
        print("test 3 passed")
    else:
        print("test 3 FAILED")

# test 4 — median odd length
def test_median_odd_length():
    result = median([1, 2, 3, 4, 5])
    if result == 3:
        print("test 4 passed")
    else:
        print("test 4 FAILED")

# test 5 — median even length
def test_median_even_length():
    result = median([1, 2, 3, 4])
    if result == 2.5:
        print("test 5 passed")
    else:
        print("test 5 FAILED")

# test 6 — std dev known value
def test_std_dev_known_value():
    result = std_dev([2, 4, 4, 4, 5, 5, 7, 9])
    if abs(result - 2.0) < 1e-9:
        print("test 6 passed")
    else:
        print("test 6 FAILED")

# test 7 — disease rate by group
def test_disease_rate_by_group():
    records = [
        {"Sex": "1", "Heart Disease": "Presence"},
        {"Sex": "1", "Heart Disease": "Absence"},
        {"Sex": "0", "Heart Disease": "Presence"},
        {"Sex": "0", "Heart Disease": "Presence"},
    ]
    result = disease_rate_by_group(records, "Sex")
    if result["1"]["rate"] == 50.0 and result["0"]["rate"] == 100.0:
        print("test 7 passed")
    else:
        print("test 7 FAILED")

if __name__ == "__main__":
    test_mean_simple()
    test_mean_with_nones()
    test_mean_empty_list()
    test_median_odd_length()
    test_median_even_length()
    test_std_dev_known_value()
    test_disease_rate_by_group()
    print("all tests done")