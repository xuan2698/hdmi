def reference(vectors):
    state = 0
    out = []
    mask = 0xffffffff
    for row in vectors:
        if row.get('areset', 0):
            state = 0
        elif row.get('train_mispredicted', 0):
            hist = row.get('train_history', 0) & mask
            taken = row.get('train_taken', 0) & 1
            state = ((hist << 1) | taken) & mask
        elif row.get('predict_valid', 0):
            taken = row.get('predict_taken', 0) & 1
            state = ((state << 1) | taken) & mask
        out.append({'predict_history': state})
    return out
