def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v['a']
        b = v['b']
        q = state | (a ^ b)
        out.append({'q': q, 'state': state})
        state = a ^ b
    return out