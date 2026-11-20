def reference(vectors):
    out = []
    state = 0
    for v in vectors:
        reset = v.get('reset', 0) & 1
        inp = v.get('in', 0) & 0xFFFFFFFF
        if reset:
            state = 0
        else:
            state = (state | (state & ~inp)) & 0xFFFFFFFF
        out.append({'out': state & 0xFFFFFFFF})
    return out
