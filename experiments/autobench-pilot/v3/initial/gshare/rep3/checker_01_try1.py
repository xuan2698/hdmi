def reference(vectors):
    pht = [0] * 128
    ghr = 0
    out = []
    for row in vectors:
        def step(inp):
            nonlocal pht, ghr
            predict_taken = 0
            predict_history = ghr
            if inp.get('predict_valid', 0):
                idx = (inp.get('predict_pc', 0) ^ ghr) & 0x7f
                c = pht[idx]
                predict_taken = 1 if c >= 2 else 0
                predict_history = ghr
                ghr = ((ghr << 1) | predict_taken) & 0x7f
            if inp.get('train_valid', 0):
                idx = (inp.get('train_pc', 0) ^ inp.get('train_history', 0)) & 0x7f
                c = pht[idx]
                if inp.get('train_taken', 0):
                    if c < 3:
                        pht[idx] = c + 1
                else:
                    if c > 0:
                        pht[idx] = c - 1
                if inp.get('train_mispredicted', 0):
                    ghr = ((inp.get('train_history', 0) << 1) | inp.get('train_taken', 0)) & 0x7f
            return predict_taken, predict_history
        if row.get('areset', 0):
            pht = [0] * 128
            ghr = 0
            pt, ph = 0, 0
        else:
            pt, ph = step(row)
        if 'mid' in row:
            m = dict(row)
            m.update(row['mid'])
            if m.get('areset', 0):
                pht = [0] * 128
                ghr = 0
            else:
                step(m)
        out.append({'predict_taken': pt & 1, 'predict_history': ph & 0x7f})
    return out
