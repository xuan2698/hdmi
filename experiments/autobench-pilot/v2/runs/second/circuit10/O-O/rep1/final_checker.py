def reference(vectors):
    out = []
    state = None
    for v in vectors:
        a = v.get('a')
        b = v.get('b')
        clk = v.get('clk')
        if clk == 1:
            if state is None:
                state = 0
            if a is not None and b is not None:
                state = (state ^ a ^ b) & 1
        q = state
        out.append({'q': q, 'state': state})
    return out
