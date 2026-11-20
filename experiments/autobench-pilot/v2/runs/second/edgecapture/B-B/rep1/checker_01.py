def reference(vectors):
    out = []
    state = 0
    for v in vectors:
        reset = v.get('reset', 0)
        inp = v.get('in', 0)
        if reset:
            state = 0
        else:
            state = (state | (inp & ~v.get('_prev_in', 0))) & 0xFFFFFFFF
        out.append({'out': state})
        v['_prev_in'] = inp
    return out
