def reference(vectors):
    out = []
    state = 0
    for row in vectors:
        # Apply asynchronous reset if asserted (positive-edge triggered async reset)
        # In this contract, areset is asynchronous active-high; if areset is 1, output is 0.
        # We process combinational/asynchronous reset before the clock edge.
        # The row values are driven before the sampled edge.
        areset = row.get('areset', 0)
        if areset:
            state = 0
        else:
            # Clock edge processing
            train_mispredicted = row.get('train_mispredicted', 0)
            predict_valid = row.get('predict_valid', 0)
            if train_mispredicted:
                train_history = row.get('train_history', 0) & 0xFFFFFFFF
                train_taken = row.get('train_taken', 0) & 1
                state = ((train_history << 1) | train_taken) & 0xFFFFFFFF
            elif predict_valid:
                predict_taken = row.get('predict_taken', 0) & 1
                state = ((state << 1) | predict_taken) & 0xFFFFFFFF
            # else hold
        out.append({'predict_history': state & 0xFFFFFFFF})
    return out
