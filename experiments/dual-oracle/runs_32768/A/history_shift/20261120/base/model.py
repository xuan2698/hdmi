def reference(vectors):
    M = 0xffffffff
    h = 0
    cur = {}
    out = []
    for row in vectors:
        for k, v in row.items():
            if k != 'mid' and k != 'clk':
                cur[k] = v
        if cur.get('areset', 0):
            h = 0
        elif cur.get('train_mispredicted', 0):
            h = (((cur.get('train_history', 0) & M) << 1) | (cur.get('train_taken', 0) & 1)) & M
        elif cur.get('predict_valid', 0):
            h = ((h << 1) | (cur.get('predict_taken', 0) & 1)) & M
        out.append({'predict_history': h & M})
        if 'mid' in row:
            for k, v in row['mid'].items():
                if k != 'clk':
                    cur[k] = v
            if cur.get('areset', 0):
                h = 0
    return out
