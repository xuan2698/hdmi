def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0)
        b = v.get('b', 0)
        state = a ^ b
        out.append({'state': state, 'q': state})
    return out