import collections
from functools import total_ordering

def mean(values):
    clean = [v for v in values if v is not None]
    if len(clean) == 0:
        return None
    return sum(clean) / len(clean)

def median(values):
    clean = sorted([v for v in values if v is not None])
    if len(clean) == 0:
        return None
    mid = len(clean) // 2
    if len(clean) % 2 == 0:
        return (clean[mid - 1] + clean[mid]) / 2
    return clean[mid]

def std_dev(values):
    clean = [v for v in values if v is not None]
    if len(clean) == 0:
        return None
    avg = mean(clean)
    variance = sum((v - avg) ** 2 for v in clean) / len(clean)
    return variance ** 0.5

def mode(values):
    clean = [v for v in values if v is not None]
    if len(clean) == 0:
        return None
    counter = collections.Counter(clean)
    return counter.most_common(1)[0][0]

def field_summary(records, field):
    values = []
    for row in records:
        v = row.get(field)
        if v is not None:
            try:
                values.append(float(v))
            except:
                values.append(v)
    return {
        "mean": mean(values),
        "median": median(values),
        "std_dev": std_dev(values),
        "mode": mode(values)
    }


def value_distribution(values):
    clean = [v for v in values if v is not None]
    if len(clean) == 0:
        return {}
    counter = collections.Counter(clean)
    total = len(clean)
    result = {}
    for value, count in counter.most_common():
        result[value] = {
            "count": count,
            "pct": round(count / total * 100, 1)
        }
    return result

# what % of each group has heart disease
def disease_rate_by_group(records, group_field):
    groups = {}
    for record in records:
        if record.get("Heart Disease") is None:
            continue
        key = record.get(group_field)
        if key not in groups:
            groups[key] = {"total": 0, "presence":0}
        groups[key]["total"] += 1
        if record.get("Heart Disease") == "Presence":
            groups[key]["presence"] += 1
    
    result = {}
    for key, counts in groups.items():
        result[key] = {
            "total": counts["total"],
            "presence": counts["presence"],
            "rate": round(counts["presence"]/counts["total"] * 100, 1)
        }
    return result

# what age group has most heart disease
def age_group_analysis(records):
    groups = {}
    for record in records:
        if record.get("Age") is None or record.get("Heart Disease") is None:
            continue
        age = int(record.get("Age"))
        group_start = age // 10 * 10
        key = f"{group_start} - {group_start + 9}"
        if key not in groups:
            groups[key] = {"total": 0, "presence": 0}
        groups[key]["total"] += 1
        if record.get("Heart Disease") == "Presence":
            groups[key]["presence"] += 1
        
    result = {}
    for key, counts in groups.items():
        result[key] = {
            "total": counts["total"],
            "presence": counts["presence"],
            "rate": round(counts["presence"] / counts["total"] * 100, 1) if counts["total"] > 0 else 0
        }
    return result

def generate_insights(records):
    return {
        "disease_by_sex": disease_rate_by_group(records, "Sex"),
        "disease_by_chest_pain": disease_rate_by_group(records, "Chest pain type"),
        "disease_by_age": age_group_analysis(records)
    }