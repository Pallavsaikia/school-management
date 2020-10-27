def Merge(dict1, dict2):
    return (dict2.update(dict1))


def Convert(tup, di):
    for a, b in tup:
        di.setdefault(a, []).append(b)
    return di
