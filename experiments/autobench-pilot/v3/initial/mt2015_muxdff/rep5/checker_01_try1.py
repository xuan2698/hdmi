def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        L = row.get('L', 0)
        r_in = row.get('r_in', 0)
        q_in = row.get('q_in', 0)
        if L:
            q = r_in & 7
        else:
            q = ((q >> 1) ^ ((q & 1) << 2)) & 7
        out.append({'Q': q & 7})
        mid = row.get('mid')
        if mid:
            if 'L' in mid:
                L = mid['L']
            if 'r_in' in mid:
                r_in = mid['r_in']
            if 'q_in' in mid:
                q_in = mid['q_in']
    return out
