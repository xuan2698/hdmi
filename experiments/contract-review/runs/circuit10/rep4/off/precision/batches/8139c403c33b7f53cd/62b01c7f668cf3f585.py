def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0)
        b = v.get('b', 0)
        out.append({'q': state, 'state': state})
        state = 1 if (a or b) else 0
    return out
