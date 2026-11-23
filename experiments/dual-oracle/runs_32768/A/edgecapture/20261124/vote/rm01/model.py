def reference(vectors):
    out = 0
    prev = 0
    mask = 0xFFFFFFFF
    result = []
    for row in vectors:
        reset = row['reset'] & 1
        x = row['in'] & mask
        if reset:
            out = 0
        else:
            out = (out | (prev & (~x & mask))) & mask
        prev = x
        result.append({'out': out})
    return result
