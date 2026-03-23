from pipeline.schema import SCHEMA
def decode_record(record):
    decoded = {}

    for key, value in record.items():
        decoded[key] = value

        rules = SCHEMA.get(key, {})
        decode_map = rules.get("decode")
        if decode_map:
            decoded[f"{key}_label"] = decode_map.get(value, "unknown")

    return decoded
