def reference(vectors):
    out = []
    state = 0  # 32-bit history register
    for row in vectors:
        # Apply asynchronous reset if asserted (before edge sampling)
        if row.get('areset', 0):
            state = 0
        # Sample at posedge: compute next state
        if not row.get('areset', 0):
            if row.get('train_mispredicted', 0):
                th = row.get('train_history', 0) & 0xFFFFFFFF
                tt = row.get('train_taken', 0) & 1
                state = ((th << 1) | tt) & 0xFFFFFFFF
            elif row.get('predict_valid', 0):
                pt = row.get('predict_taken', 0) & 1
                state = ((state << 1) | pt) & 0xFFFFFFFF
        out.append({'predict_history': state & 0xFFFFFFFF})
    return out
