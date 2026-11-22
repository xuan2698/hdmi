def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v['a']
        b = v['b']
        nxt = a ^ b ^ state
        out.append({'q': nxt, 'state': state})
        state = nxt
    return out