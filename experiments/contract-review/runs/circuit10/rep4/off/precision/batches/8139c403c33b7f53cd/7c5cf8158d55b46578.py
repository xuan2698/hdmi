def reference(vectors):
    state = 0
    q = 0
    out = []
    for v in vectors:
        a = v.get('a', 0)
        b = v.get('b', 0)
        out.append({'q': q, 'state': state})
        state = 1 - state
        q = 1 if (a and b) else 0
    return out
