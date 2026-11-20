def reference(vectors):
    q = None
    out = []
    for row in vectors:
        d = row.get('d')
        r = row.get('r')
        if r == 1:
            q = 0
        elif d is not None:
            q = d & 1
        out.append({'q': q})
    return out
