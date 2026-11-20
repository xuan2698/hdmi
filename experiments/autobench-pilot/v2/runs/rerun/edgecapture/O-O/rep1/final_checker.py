def reference(vectors):
    out = []
    state = 0
    prev_in = 0
    for v in vectors:
        reset = v.get('reset', 0)
        inp = v.get('in', 0) & 0xFFFFFFFF
        if reset:
            state = 0
        else:
            state = state | (prev_in & ~inp & 0xFFFFFFFF)
        out.append({'out': state & 0xFFFFFFFF})
        prev_in = inp
    return out
