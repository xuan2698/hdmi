def reference(vectors):
    state = 0
    a = 0
    b = 0
    out = []
    for v in vectors:
        a = v.get('a', a)
        b = v.get('b', b)
        ns = (a & b) | (state & (a | b))
        q = ns ^ a ^ b
        out.append({'q': q & 1, 'state': ns & 1})
        state = ns
        if 'mid' in v:
            m = v['mid']
            a = m.get('a', a)
            b = m.get('b', b)
    return out
