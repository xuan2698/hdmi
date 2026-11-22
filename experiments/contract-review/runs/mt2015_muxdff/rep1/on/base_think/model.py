def reference(vectors):
    Q = 0
    inp = {'L': 0, 'q_in': 0, 'r_in': 0}
    out = []
    for row in vectors:
        for k, v in row.items():
            if k != 'mid':
                inp[k] = v
        Q = inp['r_in'] if inp['L'] else inp['q_in']
        out.append({'Q': Q & 1})
        if 'mid' in row:
            for k, v in row['mid'].items():
                inp[k] = v
    return out
