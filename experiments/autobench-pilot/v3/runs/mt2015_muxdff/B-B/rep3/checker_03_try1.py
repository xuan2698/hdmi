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
            q = (q_in ^ q) & 1
        out.append({'Q': q})
        mid = row.get('mid')
        if mid:
            L2 = mid.get('L', L)
            r2 = mid.get('r_in', r_in)
            q2 = mid.get('q_in', q_in)
            if L2:
                q = r2 & 1
            else:
                q = (q2 ^ q) & 1
    return out
