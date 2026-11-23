def reference(vectors):
    s = 0
    out = []
    for row in vectors:
        r = row.get('reset', 0)
        i = row.get('in', 0)
        if r:
            s = 0
        else:
            if s == 0:
                s = 1 if i else 0
            elif s == 1:
                s = 1 if i else 2
            elif s == 2:
                s = 3 if i else 0
            elif s == 3:
                s = 1 if i else 2
        out.append({'out': 1 if s == 3 else 0})
    return out
