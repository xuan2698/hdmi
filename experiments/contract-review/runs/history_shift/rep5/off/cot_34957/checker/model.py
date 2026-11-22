def reference(vectors):
    # 32-bit global branch history shift register with flush/rollback.
    # State updates on posedge clk. Output is post-edge state.
    # Priority: areset > train_mispredicted > predict_valid.
    # predict: history = ((history << 1) | predict_taken) & 0xFFFFFFFF
    # train:   history = ((train_history << 1) | train_taken) & 0xFFFFFFFF
    # areset:  history = 0
    # Power-up undefined; use sentinel until first reset observed.
    out = []
    state = None  # sentinel: undefined until reset
    for row in vectors:
        areset = row.get('areset', 0) & 1
        predict_valid = row.get('predict_valid', 0) & 1
        predict_taken = row.get('predict_taken', 0) & 1
        train_mispredicted = row.get('train_mispredicted', 0) & 1
        train_taken = row.get('train_taken', 0) & 1
        train_history = row.get('train_history', 0) & 0xFFFFFFFF

        if areset:
            state = 0
        elif train_mispredicted:
            state = ((train_history << 1) | train_taken) & 0xFFFFFFFF
        elif predict_valid:
            if state is None:
                state = 0
            state = ((state << 1) | predict_taken) & 0xFFFFFFFF
        # else: hold state

        if state is None:
            # undefined power-up; emit 0 as concrete value
            out.append({'predict_history': 0})
        else:
            out.append({'predict_history': state & 0xFFFFFFFF})
    return out
