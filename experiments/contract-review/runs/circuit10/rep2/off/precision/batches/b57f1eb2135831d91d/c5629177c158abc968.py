def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0)
        b = v.get('b', 0)
        q = a ^ b
        out.append({'q': q, 'state': state})
        state = a ^ b
    return out