def reference(vectors):
    state = None
    out = []
    for v in vectors:
        a = v.get('a')
        b = v.get('b')
        if state is None:
            q = None
            ns = None
        else:
            q = state
            if a is None or b is None:
                ns = None
            else:
                ns = (a ^ b) ^ state
        out.append({'q': q, 'state': state})
        state = ns
    return out
