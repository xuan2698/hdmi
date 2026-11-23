def reference(vectors):
    h = 0
    M = (1 << 32) - 1
    out = []
    for v in vectors:
        if v.get('areset', 0):
            h = 0
        elif v.get('train_mispredicted', 0):
            h = ((int(v.get('train_history', 0)) << 1) | int(v.get('train_taken', 0))) & M
        elif v.get('predict_valid', 0):
            h = ((h << 1) | int(v.get('predict_taken', 0))) & M
        out.append({'predict_history': h & M})
    return out
