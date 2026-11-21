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
            if mid.get('L', L):
                q = mid.get('r_in', r_in) & 1
            else:
                q = (mid.get('q_in', q_in) ^ q) & 1
    return out
