def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        L = row.get('L', 0)
        r_in = row.get('r_in', 0)
        q_in = row.get('q_in', 0)
        if L:
            nq = r_in & 1
        else:
            nq = (q_in ^ q) & 1
        q = nq
        out.append({'Q': q & 1})
        if 'mid' in row:
            m = row['mid']
            if 'L' in m:
                L = m['L']
            if 'r_in' in m:
                r_in = m['r_in']
            if 'q_in' in m:
                q_in = m['q_in']
            if L:
                q = r_in & 1
            else:
                q = (q_in ^ q) & 1
    return out
