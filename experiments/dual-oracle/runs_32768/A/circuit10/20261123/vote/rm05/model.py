def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v['a'] & 1
        b = v['b'] & 1
        q = (state ^ a ^ b) & 1
        out.append({'q': q, 'state': state})
        state = ((state & a) | (state & b) | (a & b)) & 1
    return out
