def reference(vectors):
    q = 4
    result = []
    for v in vectors:
        if v['a']:
            q = 4
        else:
            q = (q + 1) % 7
        result.append({'q': q})
    return result
