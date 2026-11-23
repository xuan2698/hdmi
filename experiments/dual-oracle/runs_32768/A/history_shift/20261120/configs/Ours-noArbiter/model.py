def reference(vectors):
    hist = 0
    mask = 0xFFFFFFFF
    result = []
    for row in vectors:
        if row.get('areset', 0):
            hist = 0
        elif row.get('train_mispredicted', 0):
            train_history = row.get('train_history', 0) & mask
            train_taken = row.get('train_taken', 0) & 1
            hist = ((train_history << 1) | train_taken) & mask
        elif row.get('predict_valid', 0):
            predict_taken = row.get('predict_taken', 0) & 1
            hist = ((hist << 1) | predict_taken) & mask
        result.append({'predict_history': hist})
    return result
