def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        areset = row.get('areset', 0)
        if areset:
            state = 0
        else:
            pv = row.get('predict_valid', 0)
            pt = row.get('predict_taken', 0)
            tm = row.get('train_mispredicted', 0)
            tt = row.get('train_taken', 0)
            th = row.get('train_history', 0)
            if tm:
                state = ((th << 1) | tt) & 0xFFFFFFFF
            elif pv:
                state = ((state << 1) | pt) & 0xFFFFFFFF
        out.append({'predict_history': state})
        mid = row.get('mid')
        if mid:
            if mid.get('areset', 0):
                state = 0
            else:
                pv = mid.get('predict_valid', row.get('predict_valid', 0))
                pt = mid.get('predict_taken', row.get('predict_taken', 0))
                tm = mid.get('train_mispredicted', row.get('train_mispredicted', 0))
                tt = mid.get('train_taken', row.get('train_taken', 0))
                th = mid.get('train_history', row.get('train_history', 0))
                if tm:
                    state = ((th << 1) | tt) & 0xFFFFFFFF
                elif pv:
                    state = ((state << 1) | pt) & 0xFFFFFFFF
    return out
