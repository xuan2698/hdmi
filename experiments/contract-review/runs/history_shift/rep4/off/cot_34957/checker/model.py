def reference(vectors):
    out = []
    state = 0
    for row in vectors:
        # Apply asynchronous reset immediately if asserted (before edge)
        if row.get('areset', 0):
            state = 0
        else:
            # Determine next state based on inputs at this edge
            if row.get('train_mispredicted', 0):
                th = row.get('train_history', 0) & 0xFFFFFFFF
                tt = row.get('train_taken', 0) & 1
                state = ((th & 0x7FFFFFFF) << 1) | tt
            elif row.get('predict_valid', 0):
                pt = row.get('predict_taken', 0) & 1
                state = ((state & 0x7FFFFFFF) << 1) | pt
            # else hold
        out.append({'predict_history': state & 0xFFFFFFFF})
    return out
