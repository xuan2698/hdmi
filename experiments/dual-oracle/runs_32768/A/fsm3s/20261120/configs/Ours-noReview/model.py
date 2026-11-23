def reference(vectors):
    s = 0
    result = []
    for r in vectors:
        if r.get('reset', 0):
            s = 0
        else:
            i = r.get('in', 0)
            if s == 0:
                s = 1 if i else 0
            elif s == 1:
                s = 2 if not i else 1
            elif s == 2:
                s = 3 if i else 0
            else:
                s = 2 if not i else 1
        result.append({'out': 1 if s == 3 else 0})
    return result
