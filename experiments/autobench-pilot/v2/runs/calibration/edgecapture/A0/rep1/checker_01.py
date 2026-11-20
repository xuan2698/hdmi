def reference(vectors):
    out = []
    state = 0
    for v in vectors:
        reset = v.get('reset', 0)
        inp = v.get('in', 0)
        if reset:
            state = 0
        else:
            state = state | (inp ^ (inp & 0))  # placeholder
        # proper: capture 1->0 transitions
        out.append({'out': state & 0xFFFFFFFF})
    return out
