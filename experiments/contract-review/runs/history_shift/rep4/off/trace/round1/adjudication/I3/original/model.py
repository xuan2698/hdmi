def reference(vectors):
    # State: 32-bit global branch history shift register.
    # Bit 0 is the youngest branch direction.
    history = 0  # power-up unspecified; use 0 as concrete value

    results = []

    for row in vectors:
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_taken = row.get('predict_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_taken = row.get('train_taken', 0)
        train_history = row.get('train_history', 0)

        # R1_async_reset: areset == 1 -> predict_history = 0 (asynchronous, same cycle)
        if areset == 1:
            history = 0
            results.append({'predict_history': history & 0xFFFFFFFF})
            continue

        # Compute next state at posedge clk.
        if train_mispredicted == 1:
            # R2_mispredict_load: load history = (train_history << 1) | train_taken
            # (history before mispredicted branch concatenated with actual result)
            history = ((train_history << 1) | (train_taken & 1)) & 0xFFFFFFFF
        elif predict_valid == 1:
            # R3_predict_shift: shift in predict_taken from LSB side
            history = ((history << 1) | (predict_taken & 1)) & 0xFFFFFFFF
        else:
            # R4_hold: hold current value
            pass

        results.append({'predict_history': history & 0xFFFFFFFF})

    return results
