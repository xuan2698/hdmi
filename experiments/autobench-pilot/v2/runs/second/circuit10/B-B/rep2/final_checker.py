def reference(vectors):
    state = None
    out = []
    for v in vectors:
        a = v.get('a')
        b = v.get('b')
        clk = v.get('clk')
        if clk == 1:
            if state is None:
                if a is not None and b is not None:
                    state = a ^ b
            else:
                if a is not None and b is not None:
                    state = a ^ b
        q = state
        out.append({'q': q, 'state': state})
    return out
