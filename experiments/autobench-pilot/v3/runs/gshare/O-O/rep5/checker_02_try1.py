def reference(vectors):
    pht = [0] * 128
    ghr = 0
    out = []
    for row in vectors:
        if row.get('areset'):
            pht = [0] * 128
            ghr = 0
        pv = row.get('predict_valid', 0)
        tv = row.get('train_valid', 0)
        pt = 0
        ph = ghr
        if pv:
            idx = (row['predict_pc'] ^ ghr) & 0x7F
            pt = 1 if pht[idx] >= 2 else 0
            ph = ghr
        if tv:
            idx = (row['train_pc'] ^ row['train_history']) & 0x7F
            c = pht[idx]
            if row['train_taken']:
                if c < 3:
                    pht[idx] = c + 1
            else:
                if c > 0:
                    pht[idx] = c - 1
            if row['train_mispredicted']:
                ghr = ((row['train_history'] << 1) | row['train_taken']) & 0x7F
            elif pv:
                ghr = ((ghr << 1) | pt) & 0x7F
        elif pv:
            ghr = ((ghr << 1) | pt) & 0x7F
        out.append({'predict_taken': pt, 'predict_history': ph})
        if 'mid' in row:
            m = row['mid']
            if m.get('areset'):
                pht = [0] * 128
                ghr = 0
            mpv = m.get('predict_valid', pv)
            mtv = m.get('train_valid', tv)
            mpt = 0
            mph = ghr
            if mpv:
                mpc = m.get('predict_pc', row.get('predict_pc', 0))
                idx = (mpc ^ ghr) & 0x7F
                mpt = 1 if pht[idx] >= 2 else 0
                mph = ghr
            if mtv:
                mtpc = m.get('train_pc', row.get('train_pc', 0))
                mth = m.get('train_history', row.get('train_history', 0))
                mtt = m.get('train_taken', row.get('train_taken', 0))
                mtm = m.get('train_mispredicted', row.get('train_mispredicted', 0))
                idx = (mtpc ^ mth) & 0x7F
                c = pht[idx]
                if mtt:
                    if c < 3:
                        pht[idx] = c + 1
                else:
                    if c > 0:
                        pht[idx] = c - 1
                if mtm:
                    ghr = ((mth << 1) | mtt) & 0x7F
                elif mpv:
                    ghr = ((ghr << 1) | mpt) & 0x7F
            elif mpv:
                ghr = ((ghr << 1) | mpt) & 0x7F
    return out
