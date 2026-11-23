def reference(vectors):
    ghr = 0
    pht = [0] * 128
    out = []
    for v in vectors:
        areset = v['areset'] & 1
        if areset:
            ghr = 0
            pht = [0] * 128

        idx = (v['predict_pc'] & 0x7f) ^ ghr
        predict_taken = (pht[idx] >> 1) & 1
        predict_history = ghr & 0x7f
        out.append({
            'predict_taken': predict_taken,
            'predict_history': predict_history
        })

        if not areset:
            if v['train_valid'] & 1:
                tidx = (v['train_pc'] & 0x7f) ^ (v['train_history'] & 0x7f)
                c = pht[tidx]
                if v['train_taken'] & 1:
                    if c < 3:
                        c += 1
                else:
                    if c > 0:
                        c -= 1
                pht[tidx] = c

            if (v['train_valid'] & 1) and (v['train_mispredicted'] & 1):
                ghr = (((v['train_history'] & 0x7f) << 1) | (v['train_taken'] & 1)) & 0x7f
            elif v['predict_valid'] & 1:
                ghr = ((ghr << 1) | predict_taken) & 0x7f
        else:
            ghr = 0
            pht = [0] * 128

    return out
