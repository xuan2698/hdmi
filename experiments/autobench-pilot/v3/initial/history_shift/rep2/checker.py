def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        areset = row.get('areset', 0)
        pv = row.get('predict_valid', 0)
        pt = row.get('predict_taken', 0)
        tm = row.get('train_mispredicted', 0)
        tt = row.get('train_taken', 0)
        th = row.get('train_history', 0)
        if areset:
            state = 0
        else:
            if tm:
                state = ((th << 1) | tt) & 0xFFFFFFFF
            elif pv:
                state = ((state << 1) | pt) & 0xFFFFFFFF
        out.append({'predict_history': state & 0xFFFFFFFF})
        mid = row.get('mid')
        if mid:
            areset = mid.get('areset', areset)
            pv = mid.get('predict_valid', pv)
            pt = mid.get('predict_taken', pt)
            tm = mid.get('train_mispredicted', tm)
            tt = mid.get('train_taken', tt)
            th = mid.get('train_history', th)
            if areset:
                state = 0
            else:
                if tm:
                    state = ((th << 1) | tt) & 0xFFFFFFFF
                elif pv:
                    state = ((state << 1) | pt) & 0xFFFFFFFF
    return out
