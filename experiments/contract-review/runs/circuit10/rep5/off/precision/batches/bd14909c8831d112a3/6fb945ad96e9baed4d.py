def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v['a'] & 1
        b = v['b'] & 1
        q = state
        out.append({'q': q, 'state': state})
        state = (a ^ b ^ state) & 1
    return out