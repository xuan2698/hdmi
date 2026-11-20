def reference(vectors):
    results = []
    q = None
    for row in vectors:
        d = row.get('d')
        r = row.get('r')
        if r == 1:
            q = 0
        elif d is not None:
            q = d & 1
        results.append({'q': q})
    return results
