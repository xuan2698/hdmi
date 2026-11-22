def reference(vectors):
    history = 0
    outputs = []
    for v in vectors:
        if v.get('areset', 0):
            history = 0
            outputs.append({'predict_history': history})
            continue
        if v.get('train_mispredicted', 0):
            history = ((v.get('train_history', 0) << 1) | v.get('train_taken', 0)) & 0xFFFFFFFF
        elif v.get('predict_valid', 0):
            history = ((history << 1) | v.get('predict_taken', 0)) & 0xFFFFFFFF
        outputs.append({'predict_history': history})
    return outputs