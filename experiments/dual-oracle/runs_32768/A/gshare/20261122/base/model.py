def reference(vectors):
    h = 0
    p = [0] * 128
    out = []
    for v in vectors:
        a = v.get('areset', 0)
        if a:
            h = 0
            p = [0] * 128
        pc = v.get('predict_pc', 0) & 127
        idx = (pc ^ h) & 127
        c = p[idx]
        pt = 1 if c >= 2 else 0
        out.append({'predict_taken': pt, 'predict_history': h})
        if not a:
            if v.get('train_valid', 0):
                ti = (v.get('train_pc', 0) ^ v.get('train_history', 0)) & 127
                c = p[ti]
                if v.get('train_taken', 0):
                    if c < 3:
                        p[ti] = c + 1
                else:
                    if c > 0:
                        p[ti] = c - 1
            if v.get('train_valid', 0) and v.get('train_mispredicted', 0):
                h = ((v.get('train_history', 0) << 1) | v.get('train_taken', 0)) & 127
            elif v.get('predict_valid', 0):
                h = ((h << 1) | pt) & 127
        m = v.get('mid')
        if m and m.get('areset', 0) == 1:
            h = 0
            p = [0] * 128
    return out
