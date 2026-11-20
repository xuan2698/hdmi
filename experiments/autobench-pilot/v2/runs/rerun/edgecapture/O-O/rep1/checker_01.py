def reference(vectors):
    out = []
    state = 0
    for v in vectors:
        reset = v.get('reset', 0)
        inp = v.get('in', 0)
        if reset:
            state = 0
        else:
            prev = state
            # capture 1->0 transitions: previous captured value 1, current input 0
            # We need to track previous input, not previous output.
            pass
        out.append({'out': state & 0xFFFFFFFF})
    return out
