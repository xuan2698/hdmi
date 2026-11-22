def reference(vectors):
    out = []
    state = 0  # power-up unspecified; use 0
    for row in vectors:
        # Apply asynchronous reset if asserted (before edge sampling)
        if row.get('areset', 0):
            state = 0
        # Sample on posedge: compute next state
        if row.get('train_mispredicted', 0):
            state = ((row.get('train_history', 0) & 0xFFFFFFFF) << 1) | (row.get('train_taken', 0) & 1)
            state &= 0xFFFFFFFF
        elif row.get('predict_valid', 0):
            state = ((state << 1) | (row.get('predict_taken', 0) & 1)) & 0xFFFFFFFF
        # else hold
        out.append({'predict_history': state & 0xFFFFFFFF})
    return out
