def reference(vectors):
    hist = 0
    mask = (1 << 32) - 1
    out = []
    for row in vectors:
        if row.get('areset', 0):
            hist = 0
        elif row.get('train_mispredicted', 0):
            hist = ((row.get('train_history', 0) << 1) | (row.get('train_taken', 0) & 1)) & mask
        elif row.get('predict_valid', 0):
            hist = ((hist << 1) | (row.get('predict_taken', 0) & 1)) & mask
        out.append({'predict_history': hist & mask})
    return out
