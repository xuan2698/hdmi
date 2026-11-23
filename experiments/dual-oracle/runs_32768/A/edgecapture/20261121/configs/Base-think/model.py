def reference(vectors):
    out = 0
    prev = 0
    reset = 0
    inp = 0
    res = []
    for row in vectors:
        if 'reset' in row:
            reset = row['reset'] & 1
        if 'in' in row:
            inp = row['in'] & 0xFFFFFFFF
        if reset:
            out = 0
        else:
            out = (out | (prev & (~inp))) & 0xFFFFFFFF
        prev = inp
        res.append({'out': out})
        if 'mid' in row and row['mid']:
            mid = row['mid']
            if 'reset' in mid:
                reset = mid['reset'] & 1
            if 'in' in mid:
                inp = mid['in'] & 0xFFFFFFFF
    return res
