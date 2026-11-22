def reference(vectors):
    # 32-bit global branch history shift register.
    # Priority: areset > train_mispredicted > predict_valid > hold.
    # predict_history[0] is the youngest branch direction.
    out = []
    state = 0  # power-up unspecified; reset will establish known value
    for row in vectors:
        # Inputs are driven before the sampled posedge.
        areset = row.get('areset', 0) & 1
        predict_valid = row.get('predict_valid', 0) & 1
        predict_taken = row.get('predict_taken', 0) & 1
        train_mispredicted = row.get('train_mispredicted', 0) & 1
        train_taken = row.get('train_taken', 0) & 1
        train_history = row.get('train_history', 0) & 0xFFFFFFFF

        # Compute next state at the sampled edge using priority ladder.
        if areset:
            state = 0
        elif train_mispredicted:
            state = ((train_history >> 1) & 0x7FFFFFFF) | ((train_taken & 1) << 31)
        elif predict_valid:
            state = ((state >> 1) & 0x7FFFFFFF) | ((predict_taken & 1) << 31)
        # else hold

        out.append({'predict_history': state & 0xFFFFFFFF})
    return out
