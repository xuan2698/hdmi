def reference(vectors):
    out = []
    prev = 0
    reg = 0
    for row in vectors:
        reset = row['reset'] & 1
        cur = row['in'] & 0xffffffff
        if reset:
            reg = 0
        else:
            reg = (reg | (prev & (~cur))) & 0xffffffff
        prev = cur
        out.append({'out': reg & 0xffffffff})
    return out
