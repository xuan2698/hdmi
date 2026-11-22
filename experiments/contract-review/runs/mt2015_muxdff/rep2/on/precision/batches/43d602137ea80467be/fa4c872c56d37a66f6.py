def reference(vectors):
    Q = 0
    out = []
    for v in vectors:
        L = v['L']
        q_in = v['q_in']
        r_in = v['r_in']
        if L == 1:
            Q = r_in
        else:
            Q = q_in
        out.append({'Q': Q})
    return out
