from pipeline.schema import SCHEMA, REQUIRED_FIELDS

#from string to int,float
def coerce(value, type_name):
    if type_name == "str":
        return value
    if type_name == "int":
        try:
            return int(value)
        except:
            return None
    if type_name == "float":
        try:
            return float(value)
        except:
            return None
    return value

def validate(row, seen):
    reasons = []

    #check for missing required fields
    for field in REQUIRED_FIELDS:
        if row.get(field, "") == "":
            reasons.append(f"{field} is missing")

    #type coercion and range/allowed checks
    for field, rules in SCHEMA.items():
        value = row.get(field, "")
        if value == "":
            row[field] = None
            continue
        
        coerced = coerce(value, rules["type"])

        if coerced is None:
            reasons.append(f"{field} has wrong type, excpected {rules['type']}")
            continue

        if "min" in rules and coerced < rules["min"]:
            reasons.append(f"{field} is too low: {coerced}")

        if "max" in rules and coerced > rules["max"]:
            reasons.append(f"{field} is too high: {coerced}")

        if "allowed" in rules and coerced not in rules["allowed"]:
            reasons.append(f"{field} has invalid value: {coerced}")
#duplicate detection
    row_id = row.get("id", "")
    if row_id in seen:
        reasons.append(f"duplicate id: {row_id}")
    else:
        seen.add(row_id) 
    return{
        "valid": len(reasons) == 0,
        "record": row,
        "reasons": reasons
    }       

#testing
if __name__ == "__main__":
    from pipeline.ingestion import load_csv

    seen = set()
    count_valid = 0
    count_invalid = 0
    for row in load_csv("data/train.csv"):
        result = validate(row,seen)
        if result["valid"]:
            count_valid += 1
        else:
            count_invalid += 1
    print(f"Valid: {count_valid}")
    print(f"Invalid: {count_invalid}")
            