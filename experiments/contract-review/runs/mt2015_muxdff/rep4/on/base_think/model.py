def reference(vectors):
    Q = 0
    held = {'L': 0, 'q_in': 0, 'r_in': 0}
    out = []
    names = ('L', 'q_in', 'r_in')
    for row in vectors:
        for k in names:
            if k in row:
                held[k] = row[k] & 1
        Q = (held['r_in'] if held['L'] else held['q_in']) & 1
        out.append({'Q': Q})
        mid = row.get('mid')
        if mid:
            for k in names:
                if k in mid:
                    held[k] = mid[k] & 1
    return out
