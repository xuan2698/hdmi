def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v['a']
        b = v['b']
        nxt = (a & b) if state == 0 else (a | b)
        state = nxt
        q = a ^ b ^ state
        out.append({'q': q, 'state': state})
    return out
