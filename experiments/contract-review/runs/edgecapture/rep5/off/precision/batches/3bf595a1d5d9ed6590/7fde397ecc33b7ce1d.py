def reference(vectors):
    out = 0
    prev_in = 0
    res = []
    for v in vectors:
        reset = v['reset']
        inp = v['in']
        if reset == 1:
            out = 0
        else:
            out = out | (prev_in & (~inp & 0xFFFFFFFF))
        res.append({'out': out & 0xFFFFFFFF})
        prev_in = inp
    return res
