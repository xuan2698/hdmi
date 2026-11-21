def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_taken = row.get('predict_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_taken = row.get('train_taken', 0)
        train_history = row.get('train_history', 0)
        if areset:
            state = 0
        else:
            if train_mispredicted:
                state = ((train_history << 1) | train_taken) & 0xFFFFFFFF
            elif predict_valid:
                state = ((state << 1) | predict_taken) & 0xFFFFFFFF
        out.append({'predict_history': state})
        mid = row.get('mid')
        if mid:
            if mid.get('areset', 0):
                state = 0
            else:
                if mid.get('train_mispredicted', 0):
                    state = ((mid.get('train_history', 0) << 1) | mid.get('train_taken', 0)) & 0xFFFFFFFF
                elif mid.get('predict_valid', 0):
                    state = ((state << 1) | mid.get('predict_taken', 0)) & 0xFFFFFFFF
    return out
