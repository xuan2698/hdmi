def reference(vectors):
    PHT = [1] * 128
    GHR = 0
    out = []
    for row in vectors:
        if row.get('areset'):
            PHT = [1] * 128
            GHR = 0
        pv = row.get('predict_valid', 0)
        tv = row.get('train_valid', 0)
        pt = 0
        ph = GHR
        if pv:
            idx = (row['predict_pc'] ^ GHR) & 0x7F
            c = PHT[idx]
            pt = 1 if c >= 2 else 0
            ph = GHR
        if tv:
            idx = (row['train_pc'] ^ row['train_history']) & 0x7F
            c = PHT[idx]
            if row['train_taken']:
                if c < 3:
                    PHT[idx] = c + 1
            else:
                if c > 0:
                    PHT[idx] = c - 1
        if tv and row['train_mispredicted']:
            GHR = ((row['train_history'] << 1) | row['train_taken']) & 0x7F
        elif pv:
            GHR = ((GHR << 1) | pt) & 0x7F
        out.append({'predict_taken': pt, 'predict_history': ph})
        if 'mid' in row:
            m = row['mid']
            if 'areset' in m and m['areset']:
                PHT = [1] * 128
                GHR = 0
    return out
