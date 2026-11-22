def reference(vectors):
    q = 0
    reset = 0
    out = []
    for row in vectors:
        for k in row:
            if k != 'mid':
                if k == 'reset':
                    reset = row[k]
        if reset:
            q = 0
        else:
            q = (q + 1) % 10
        out.append({'q': q})
        if 'mid' in row:
            for k, v in row['mid'].items():
                if k == 'reset':
                    reset = v
    return out
