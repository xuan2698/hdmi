def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v['a']; b = v['b']
        nxt = ((a & b) ^ state) & 1
        out.append({'q': state, 'state': state})
        state = nxt
    return out
