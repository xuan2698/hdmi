def reference(vectors):
    prev = 0
    out = 0
    mask = 0xFFFFFFFF
    result = []
    for row in vectors:
        reset = row['reset'] & 1
        cur = row['in'] & mask
        if reset:
            out = 0
        else:
            out = (out | (prev & (cur ^ mask))) & mask
        prev = cur
        result.append({'out': out})
    return result
