from collections import OrderedDict
from gendiff.parser import convertator
from gendiff.formatters import FORMATTERS
import os


PREFIX_ADD = '  + '
PREFIX_DEL = '  - '
PREFIX_NCh = '    '


def read_data(path):
    """
    Open file
    """
    return open(path)


def get_format(pathfile: str) -> str:
    """
    Read filename and return extension of a file
    """
    extension = os.path.splitext(pathfile)[1].lstrip('.')
    return extension


def get_diff(old: dict, new: dict) -> OrderedDict:
    """
    Compares two python dict and generates one common OrderDict with differences.  # noqa: E501
    old (dict): first dict
    new (dict): second dict
    return (OrderDict): OrderDict with differences
    """
    res = {}
    old_keys = set(old.keys()) - set(new.keys())
    for key in old_keys:
        res[key] = {'status': 'removed', 'value': old[key]}

    new_keys = set(new.keys()) - set(old.keys())
    for key in new_keys:
        res[key] = {'status': 'added', 'value': new[key]}

    for key in old.keys() & new.keys():
        old_val = old[key]
        new_val = new[key]
        if isinstance(old[key], dict) and isinstance(new[key], dict):
            res[key] = \
                {'status': 'nested', 'value': get_diff(old_val, new_val)}
        elif old_val == new_val:
            res[key] = \
                {'status': 'unchanged', 'value': old_val}
        elif old_val != new_val:
            res[key] = \
                {'status': 'changed', 'old_value': old_val, 'new_value': new_val}  # noqa: E501
    return OrderedDict(sorted(res.items()))


def generate_diff(path1: str, path2: str, format_name='stylish') -> str:
    """
    Finds differences between two files
    path1 (str): pathfile to first file
    path2 (str): pathfile to second file
    format_name (str): format output data, default=stylish
    return (str): depends on param "format_name"
    """
    data1 = convertator(read_data(file_path1), get_format(file_path1))
    data2 = convertator(read_data(file_path2), get_format(file_path2))
    diff = get_diff(data1, data2)
    return FORMATTERS[format_name].format(diff)
