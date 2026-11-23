def reference(vectors):
    hist = 0
    mask = (1 << 32) - 1
    out = []
    for row in vectors:
        if row['areset']:
            hist = 0
        elif row['train_mispredicted']:
            hist = ((row['train_history'] << 1) | row['train_taken']) & mask
        elif row['predict_valid']:
            hist = ((hist << 1) | row['predict_taken']) & mask
        out.append({'predict_history': hist & mask})
    return out
