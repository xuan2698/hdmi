def reference(vectors):
    out = 0
    prev = 0
    result = []
    for row in vectors:
        reset = row.get('reset', 0) & 1
        value = row.get('in', 0) & 0xFFFFFFFF
        if reset:
            out = 0
        else:
            out = (out | (prev & ~value)) & 0xFFFFFFFF
        prev = value
        result.append({'out': out})
    return result
