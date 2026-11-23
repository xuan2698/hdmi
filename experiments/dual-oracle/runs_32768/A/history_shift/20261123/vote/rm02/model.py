def reference(vectors):
    hist = 0
    mask = (1 << 32) - 1
    out = []
    for row in vectors:
        areset = row.get('areset', 0)
        if areset:
            hist = 0
        else:
            train_mispredicted = row.get('train_mispredicted', 0)
            predict_valid = row.get('predict_valid', 0)
            if train_mispredicted:
                train_history = row.get('train_history', 0) & mask
                train_taken = row.get('train_taken', 0) & 1
                hist = ((train_history << 1) | train_taken) & mask
            elif predict_valid:
                predict_taken = row.get('predict_taken', 0) & 1
                hist = ((hist << 1) | predict_taken) & mask
        out.append({'predict_history': hist & mask})
    return out
