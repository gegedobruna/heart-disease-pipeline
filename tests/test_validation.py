import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.validation import validate

valid_row = {
    "id": "1",
    "Age": "54",
    "Sex": "1",
    "Chest pain type": "3",
    "BP": "130",
    "Cholesterol": "250",
    "FBS over 120": "0",
    "EKG results": "0",
    "Max HR": "150",
    "Exercise angina": "0",
    "ST depression": "1.5",
    "Slope of ST": "2",
    "Number of vessels fluro": "0",
    "Thallium": "3",
    "Heart Disease": "Absence"
}

# test 1 — valid row
def test_valid_row():
    seen = set()
    result = validate(valid_row, seen)
    assert result["valid"] == True
    print("test 1 passed" if result["valid"] == True else "test 1 FAILED")

# test 2 — wrong type
def test_wrong_type():
    seen = set()
    row = dict(valid_row)
    row["Age"] = "abc" 
    result = validate(row, seen)
    if result["valid"] == False:
        print("test 2 passed")
    else:
        print("test 2 FAILED")
        
# test 3 — impossible value
def test_impossible_value():
    seen = set()
    row = dict(valid_row)
    row["Max HR"] = 0 
    result = validate(row, seen)
    if result["valid"] == False:
        print("test 3 passed")
    else:
        print("test 3 FAILED")

# test 4 — duplicate
def test_duplicate():
    seen = set()
    row1 = dict(valid_row)
    row2 = dict(valid_row)
    result1 = validate(row1, seen)
    result2 = validate(row2, seen)
    if result1["valid"] == True and result2["valid"] == False:
        print("test 4 passed")
    else:        
        print("test 4 FAILED")


# test 5 — missing required field
def test_missing_required():
    seen = set()
    row = dict(valid_row)
    row["Age"] = None
    result = validate(row, seen)
    if result["valid"] == False:
        print("test 5 passed")
    else:        
        print("test 5 FAILED")

if __name__ == "__main__":
    test_valid_row()
    test_wrong_type()
    test_impossible_value()
    test_duplicate()
    test_missing_required()
    print("all tests done")