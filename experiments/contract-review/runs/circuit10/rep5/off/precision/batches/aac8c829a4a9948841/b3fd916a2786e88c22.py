def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v['a']
        b = v['b']
        q = (a ^ b) & 1
        out.append({'q': q, 'state': state})
        state = q
    return out