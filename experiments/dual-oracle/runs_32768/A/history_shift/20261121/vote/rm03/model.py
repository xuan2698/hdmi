def reference(vectors):
    history = 0
    mask = 0xFFFFFFFF
    result = []
    for row in vectors:
        if row.get('areset', 0):
            history = 0
        elif row.get('train_mispredicted', 0):
            history = ((int(row.get('train_history', 0)) << 1) | int(row.get('train_taken', 0))) & mask
        elif row.get('predict_valid', 0):
            history = ((history << 1) | int(row.get('predict_taken', 0))) & mask
        result.append({'predict_history': history & mask})
    return result
