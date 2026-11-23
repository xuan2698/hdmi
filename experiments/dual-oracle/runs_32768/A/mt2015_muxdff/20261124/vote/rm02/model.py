def reference(vectors):
    Q = 0
    out = []
    for v in vectors:
        L = v['L'] & 1
        r_in = v['r_in'] & 1
        q_in = v['q_in'] & 1
        Q = r_in if L else q_in
        out.append({'Q': Q & 1})
    return out
