def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        out.append({'q': state, 'state': state})
        state = 1 - state
    return out
