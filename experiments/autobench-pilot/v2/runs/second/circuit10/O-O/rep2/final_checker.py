def reference(vectors):
    state = None
    out = []
    for v in vectors:
        clk = v.get('clk', 0)
        a = v.get('a')
        b = v.get('b')
        if clk == 1:
            if state is None:
                state = 0
            if a is not None and b is not None:
                state = (state ^ a ^ b) & 1
        q = state
        out.append({'q': q, 'state': state})
    return out
