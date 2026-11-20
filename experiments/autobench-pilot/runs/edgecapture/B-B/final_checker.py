def reference(vectors):
    out = None
    prev = None
    result = []
    for v in vectors:
        reset = v['reset']
        inp = v['in'] & 0xFFFFFFFF
        if reset:
            out = 0
            prev = inp
        else:
            if prev is not None and out is not None:
                fall = (~inp) & prev & 0xFFFFFFFF
                out = out | fall
            prev = inp
        result.append({'out': out})
    return result
