def reference(vectors):
    out = 0
    prev = 0
    mask = (1 << 32) - 1
    result = []
    for row in vectors:
        reset = row['reset'] & 1
        cur = row['in'] & mask
        if reset:
            out = 0
        else:
            out = (out | (prev & (~cur & mask))) & mask
        prev = cur
        result.append({'out': out})
    return result
