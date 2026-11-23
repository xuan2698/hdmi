def reference(vectors):
    h = 0
    mask = (1 << 32) - 1
    out = []
    for v in vectors:
        if v.get('areset', 0):
            h = 0
        elif v.get('train_mispredicted', 0):
            h = ((v.get('train_history', 0) << 1) | v.get('train_taken', 0)) & mask
        elif v.get('predict_valid', 0):
            h = ((h << 1) | v.get('predict_taken', 0)) & mask
        out.append({'predict_history': h})
    return out
