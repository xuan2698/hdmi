def reference(vectors):
    q = 0
    res = []
    for row in vectors:
        L = row.get('L', 0)
        r_in = row.get('r_in', 0)
        q_in = row.get('q_in', 0)
        if L:
            q = r_in & 7
        else:
            q = ((q >> 1) ^ ((q & 1) << 2)) & 7
        out = {'Q': q & 7}
        res.append(out)
        if 'mid' in row:
            m = row['mid']
            if 'L' in m:
                L = m['L']
            if 'r_in' in m:
                r_in = m['r_in']
            if 'q_in' in m:
                q_in = m['q_in']
            if L:
                q = r_in & 7
            else:
                q = ((q >> 1) ^ ((q & 1) << 2)) & 7
    return res
