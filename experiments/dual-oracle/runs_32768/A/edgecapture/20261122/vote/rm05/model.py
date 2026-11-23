def reference(vectors):
    out = 0
    prev = 0
    res = []
    for row in vectors:
        r = int(row.get('reset', 0)) & 1
        iv = int(row.get('in', 0)) & 0xFFFFFFFF
        if r:
            out = 0
            prev = 0
        else:
            out = (out | (prev & ((~iv) & 0xFFFFFFFF))) & 0xFFFFFFFF
            prev = iv
        res.append({'out': out})
    return res
