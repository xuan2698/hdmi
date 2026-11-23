def reference(vectors):
    h = 0
    out = []
    mask = (1 << 32) - 1
    for row in vectors:
        if row.get('areset', 0):
            h = 0
        elif row.get('train_mispredicted', 0):
            h = ((row.get('train_history', 0) << 1) | row.get('train_taken', 0)) & mask
        elif row.get('predict_valid', 0):
            h = ((h << 1) | row.get('predict_taken', 0)) & mask
        out.append({'predict_history': h & mask})
    return out
