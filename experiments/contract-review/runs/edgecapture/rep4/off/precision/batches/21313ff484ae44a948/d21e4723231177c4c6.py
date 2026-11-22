def reference(vectors):
    out = 0
    prev = 0
    res = []
    for v in vectors:
        r = v['reset']
        i = v['in']
        if r == 1:
            out = 0
        else:
            out = out | (prev & ~i)
        res.append({'out': out & 0xFFFFFFFF})
        prev = i
    return res
