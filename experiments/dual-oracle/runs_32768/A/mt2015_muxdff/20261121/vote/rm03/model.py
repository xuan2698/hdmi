def reference(vectors):
    out = []
    for row in vectors:
        L = row['L']
        q_in = row['q_in']
        r_in = row['r_in']
        Q = r_in if L else q_in
        out.append({'Q': Q & 1})
    return out
