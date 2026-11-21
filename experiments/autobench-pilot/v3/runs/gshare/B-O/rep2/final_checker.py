def reference(vectors):
    pht = [1] * 128
    ghr = 0
    out = []
    for row in vectors:
        if row.get('areset'):
            pht = [1] * 128
            ghr = 0
        pv = row.get('predict_valid', 0)
        tv = row.get('train_valid', 0)
        pt = 0
        ph = ghr
        if pv:
            idx = (row['predict_pc'] ^ ghr) & 0x7f
            c = pht[idx]
            pt = 1 if c >= 2 else 0
            ph = ghr
        if tv:
            idx = (row['train_pc'] ^ row['train_history']) & 0x7f
            c = pht[idx]
            if row['train_taken']:
                if c < 3:
                    pht[idx] = c + 1
            else:
                if c > 0:
                    pht[idx] = c - 1
        if tv and row.get('train_mispredicted'):
            ghr = ((row['train_history'] << 1) | row['train_taken']) & 0x7f
        elif pv:
            ghr = ((ghr << 1) | pt) & 0x7f
        out.append({'predict_taken': pt, 'predict_history': ph})
        if 'mid' in row:
            m = row['mid']
            if 'areset' in m and m['areset']:
                pht = [1] * 128
                ghr = 0
            if 'predict_valid' in m:
                pv = m['predict_valid']
            if 'train_valid' in m:
                tv = m['train_valid']
    return out
