def reference(vectors):
    history = 0
    out = []
    for v in vectors:
        areset = v.get('areset', 0)
        if areset == 1:
            history = 0
        else:
            if v.get('train_mispredicted', 0) == 1:
                train_history = v.get('train_history', 0)
                train_taken = v.get('train_taken', 0) & 1
                history = ((train_history << 1) & 0xFFFFFFFF) | train_taken
            elif v.get('predict_valid', 0) == 1:
                predict_taken = v.get('predict_taken', 0) & 1
                history = ((history << 1) & 0xFFFFFFFF) | predict_taken
            else:
                history = history
        out.append({'predict_history': history})
    return out