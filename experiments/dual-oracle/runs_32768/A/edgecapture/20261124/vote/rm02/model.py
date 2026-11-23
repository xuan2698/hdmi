def reference(vectors):
    prev = 0
    out = 0
    result = []
    for row in vectors:
        rst = row['reset'] & 1
        cur = row['in'] & 0xffffffff
        if rst:
            out = 0
        else:
            out = (out | (prev & (~cur & 0xffffffff))) & 0xffffffff
        prev = cur
        result.append({'out': out})
    return result
