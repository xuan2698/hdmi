def reference(vectors):
    out = 0
    prev_in = 0
    prev_valid = False
    res = []
    for v in vectors:
        reset = v.get('reset', 0)
        inp = v.get('in', 0)
        if reset:
            out = 0
            prev_valid = False
        else:
            if prev_valid:
                out = out | (prev_in & (~inp & 0xFFFFFFFF))
            prev_valid = True
        prev_in = inp
        res.append({'out': out & 0xFFFFFFFF})
    return res
