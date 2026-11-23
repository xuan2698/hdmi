def reference(vectors):
    if isinstance(vectors, dict):
        keys = list(vectors.keys())
        n = len(vectors[keys[0]]) if keys else 0
        rows = [{k: vectors[k][i] for k in keys} for i in range(n)]
    else:
        rows = vectors
    history = 0
    pht = [0] * 128
    out = []
    for row in rows:
        areset = row.get('areset', 0) & 1
        if areset:
            history = 0
            pht = [0] * 128
        predict_pc = row.get('predict_pc', 0) & 0x7F
        idx = (predict_pc ^ history) & 0x7F
        c = pht[idx]
        predict_taken = 1 if c >= 2 else 0
        predict_history = history & 0x7F
        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})
        if areset:
            continue
        predict_valid = row.get('predict_valid', 0) & 1
        train_valid = row.get('train_valid', 0) & 1
        if train_valid:
            train_pc = row.get('train_pc', 0) & 0x7F
            train_history = row.get('train_history', 0) & 0x7F
            train_taken = row.get('train_taken', 0) & 1
            train_mispredicted = row.get('train_mispredicted', 0) & 1
            tidx = (train_pc ^ train_history) & 0x7F
            old = pht[tidx]
            if train_taken:
                if old < 3:
                    pht[tidx] = old + 1
            else:
                if old > 0:
                    pht[tidx] = old - 1
            if train_mispredicted:
                history = ((train_history << 1) & 0x7F) | train_taken
            else:
                if predict_valid:
                    history = ((history << 1) & 0x7F) | predict_taken
        else:
            if predict_valid:
                history = ((history << 1) & 0x7F) | predict_taken
    return out
