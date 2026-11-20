def reference(vectors):
    results = []
    history = 0
    for v in vectors:
        areset = v.get('areset', 0)
        predict_valid = v.get('predict_valid', 0)
        predict_taken = v.get('predict_taken', 0)
        train_mispredicted = v.get('train_mispredicted', 0)
        train_taken = v.get('train_taken', 0)
        train_history = v.get('train_history', 0)
        if areset:
            history = 0
        elif train_mispredicted:
            history = ((train_history << 1) | (train_taken & 1)) & 0xFFFFFFFF
        elif predict_valid:
            history = ((history << 1) | (predict_taken & 1)) & 0xFFFFFFFF
        results.append({'predict_history': history & 0xFFFFFFFF})
    return results
