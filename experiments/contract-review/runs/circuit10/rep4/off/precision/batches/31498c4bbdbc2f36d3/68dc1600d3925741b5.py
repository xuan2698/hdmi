def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0)
        b = v.get('b', 0)
        nxt = a & b
        out.append({'q': state, 'state': state})
        state = nxt
    return out
