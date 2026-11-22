def reference(vectors):
    out = []
    state = 0
    for row in vectors:
        clk = row.get('clk', 0)
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_taken = row.get('predict_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_taken = row.get('train_taken', 0)
        train_history = row.get('train_history', 0)

        # Asynchronous reset
        if areset:
            state = 0

        # Positive edge update
        if clk == 1:
            if train_mispredicted:
                state = ((train_history & 0x7FFFFFFF) << 1) | (train_taken & 1)
                state &= 0xFFFFFFFF
            elif predict_valid:
                state = ((state >> 1) | ((predict_taken & 1) << 31)) & 0xFFFFFFFF

        out.append({'predict_history': state & 0xFFFFFFFF})
    return out
