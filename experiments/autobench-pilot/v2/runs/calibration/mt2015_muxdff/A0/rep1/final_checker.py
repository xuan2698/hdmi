def reference(vectors):
    q = None
    out = []
    for v in vectors:
        L = v['L']
        q_in = v['q_in']
        r_in = v['r_in']
        if L:
            q = r_in & 1
        else:
            if q is None:
                q = None
            else:
                q = ((q_in ^ q) & 1)
        out.append({'Q': q})
    return out
