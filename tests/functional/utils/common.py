import uuid
from datetime import datetime


def replace_dynamic_attrs(
        expected_values: dict,
        data: dict
):
    for expected_attr in expected_values:
        if expected_values[expected_attr] != '...':
            continue
        if isinstance(data[expected_attr], uuid.UUID):
            data[expected_attr] = str(data[expected_attr])
        if expected_attr[-3:] == '_at' and isinstance(data[expected_attr], str):
            data[expected_attr] = datetime.fromisoformat(data[expected_attr])
        if isinstance(data[expected_attr], datetime):
            data[expected_attr] = data[expected_attr].isoformat()
            data[expected_attr] = data[expected_attr][:-3] + "000"
        expected_values[expected_attr] = data[expected_attr]

    return expected_values


def to_str(data):
    if isinstance(data, dict):
        for key in data:
            if isinstance(data[key], uuid.UUID):
                data[key] = str(data[key])
            elif isinstance(data[key], datetime):
                data[key] = data[key].isoformat()
                data[key] = data[key][:-3] + "000"
            elif isinstance(data[key], dict) or isinstance(data[key], list):
                to_str(data[key])
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], uuid.UUID):
                data[i] = str(data[i])
            elif isinstance(data[i], datetime):
                data[i] = data[i].isoformat()
                data[i] = data[i][:-3] + "000"
            elif isinstance(data[i], dict) or isinstance(data[i], list):
                to_str(data[i])
    return data
