def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0)
        b = v.get('b', 0)
        q = state ^ a ^ b
        out.append({'q': q, 'state': state})
        state = q
    return out
