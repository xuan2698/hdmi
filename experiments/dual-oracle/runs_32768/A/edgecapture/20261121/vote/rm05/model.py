def reference(vectors):
    out = 0
    prev = 0
    mask = 0xFFFFFFFF
    result = []
    for row in vectors:
        reset = row['reset'] & 1
        inp = row['in'] & mask
        if reset:
            out = 0
        else:
            out = (out | (prev & (~inp & mask))) & mask
        prev = inp
        result.append({'out': out & mask})
    return result
