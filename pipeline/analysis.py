import collections

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

