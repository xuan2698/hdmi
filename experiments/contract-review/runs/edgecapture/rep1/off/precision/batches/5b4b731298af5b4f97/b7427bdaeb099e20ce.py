def reference(vectors):
    out_reg = 0
    prev_in = 0
    res = []
    for v in vectors:
        reset = v['reset']
        inp = v['in']
        if reset == 1:
            out_reg = 0
        else:
            out_reg = out_reg | (prev_in & ~inp)
        prev_in = inp
        res.append({'out': out_reg & 0xFFFFFFFF})
    return res