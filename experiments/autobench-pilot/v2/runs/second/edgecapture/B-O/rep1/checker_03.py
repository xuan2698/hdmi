def reference(vectors):
    out = []
    state = 0
    prev = 0
    for v in vectors:
        reset = v.get('reset', 0)
        inp = v.get('in', 0) & 0xFFFFFFFF
        if reset:
            state = 0
        else:
            state = (state | (prev & (~inp))) & 0xFFFFFFFF
        prev = inp
        out.append({'out': state & 0xFFFFFFFF})
    return out
