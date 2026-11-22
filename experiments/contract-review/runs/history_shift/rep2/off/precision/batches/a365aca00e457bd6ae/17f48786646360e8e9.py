def reference(vectors):
    history = 0
    out = []
    for v in vectors:
        if v['areset']:
            history = 0
            out.append({'predict_history': 0})
            continue
        out.append({'predict_history': history})
        if v['train_mispredicted']:
            history = ((v['train_history'] << 1) | v['train_taken']) & 0xFFFFFFFF
        elif v['predict_valid']:
            history = ((history << 1) | v['predict_taken']) & 0xFFFFFFFF
    return out
