def reference(vectors):
    q = 0
    result = []
    for row in vectors:
        if row.get('reset', 0) & 1:
            q = 0
        else:
            q = row.get('d', 0) & 0xff
        result.append({'q': q})
    return result
