def reference(vectors):
    res = []
    prev = 0
    out = 0
    M = 0xFFFFFFFF
    for row in vectors:
        reset = row['reset']
        cur = row['in'] & M
        if reset:
            out = 0
        else:
            out = (out | (prev & (cur ^ M))) & M
        prev = cur
        res.append({'out': out})
    return res
