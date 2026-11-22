def reference(vectors):
    # 32-bit global branch history shift register with flush/rollback.
    # Priority: async areset > train_mispredicted (load) > predict_valid (shift).
    # predict_history[0] is youngest branch.
    out = []
    state = 0  # power-up unspecified; reset establishes it
    for row in vectors:
        # Mid-cycle changes are applied after sampling; here we model the
        # value seen at the posedge. areset is async and dominates.
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_taken = row.get('predict_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_taken = row.get('train_taken', 0)
        train_history = row.get('train_history', 0) & 0xFFFFFFFF

        if areset:
            state = 0
        elif train_mispredicted:
            # Load: history before mispredicted branch concatenated with actual result
            state = ((train_history << 1) | (train_taken & 1)) & 0xFFFFFFFF
        elif predict_valid:
            # Shift left, insert predicted direction at LSB
            state = ((state << 1) | (predict_taken & 1)) & 0xFFFFFFFF
        # else: hold

        out.append({'predict_history': state & 0xFFFFFFFF})
    return out
