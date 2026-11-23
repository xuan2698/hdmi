def reference(vectors):
    state = 0
    cur = {'a': 0, 'b': 0}
    out = []
    for v in vectors:
        for k in ('a', 'b'):
            if k in v:
                cur[k] = v[k]
        a, b = cur['a'], cur['b']
        state = (a & b) | (a & state) | (b & state)
        out.append({'q': a ^ b ^ state, 'state': state})
        m = v.get('mid', {})
        for k in ('a', 'b'):
            if k in m:
                cur[k] = m[k]
    return out
