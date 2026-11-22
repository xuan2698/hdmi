def reference(vectors):
    out_reg = 0
    in_prev = 0
    res = []
    for v in vectors:
        reset = v['reset'] & 1
        inv = v['in'] & 0xFFFFFFFF
        if reset:
            out_reg = 0
            in_prev = inv
            res.append({'out': 0})
        else:
            fall = (~inv) & in_prev & 0xFFFFFFFF
            out_reg = (out_reg | fall) & 0xFFFFFFFF
            in_prev = inv
            res.append({'out': out_reg})
    return res
