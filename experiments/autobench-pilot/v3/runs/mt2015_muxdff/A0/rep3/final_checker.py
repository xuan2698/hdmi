def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        L = row.get('L', 0)
        r_in = row.get('r_in', 0)
        q_in = row.get('q_in', 0)
        if L:
            q = r_in & 1
        else:
            q = ((q_in ^ q) & 1) if False else q
        out.append({'Q': q & 1})
    return out
