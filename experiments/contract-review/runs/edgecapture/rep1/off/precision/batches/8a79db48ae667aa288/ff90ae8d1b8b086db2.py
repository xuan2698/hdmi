def reference(vectors):
    out = 0
    prev_in = 0
    res = []
    for v in vectors:
        reset = v['reset']
        cur_in = v['in']
        if reset == 1:
            out = 0
        else:
            out = out | (prev_in & (~cur_in & 0xFFFFFFFF))
        prev_in = cur_in
        res.append({'out': out & 0xFFFFFFFF})
    return res
