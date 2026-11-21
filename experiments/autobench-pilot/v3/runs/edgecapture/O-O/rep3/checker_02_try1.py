def reference(vectors):
    out = 0
    prev = 0
    res = []
    for row in vectors:
        if row.get('reset', 0):
            out = 0
        else:
            out = out | (prev & ~row['in'] & 0xFFFFFFFF)
        prev = row['in'] & 0xFFFFFFFF
        if 'mid' in row:
            m = row['mid']
            if m.get('reset', 0):
                out = 0
            if 'in' in m:
                out = out | (prev & ~m['in'] & 0xFFFFFFFF)
                prev = m['in'] & 0xFFFFFFFF
        res.append({'out': out & 0xFFFFFFFF})
    return res
