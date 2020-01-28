from collections import OrderedDict


def alphabetically(x):
    keys = list(x.keys())
    keys.sort()
    out = OrderedDict()
    for k in keys:
        out[k] = x[k]
    return out


def by_value(x, key):
    out = OrderedDict()
    tmp = []
    for k, v in x.items():
        tmp.append([k, v])
    tmp.sort(key=key)
    for item in tmp:
        out[item[0]] = item[1]
    return out
