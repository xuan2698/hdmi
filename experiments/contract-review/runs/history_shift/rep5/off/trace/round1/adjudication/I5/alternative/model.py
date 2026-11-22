def reference(vectors):
    # State: 32-bit global branch history shift register.
    # bit 0 is the direction of the youngest branch.
    history = 0

    results = []

    for vec in vectors:
        # Read inputs for this row (driven before the sampled edge).
        areset = vec.get("areset", 0) & 1
        predict_valid = vec.get("predict_valid", 0) & 1
        predict_taken = vec.get("predict_taken", 0) & 1
        train_mispredicted = vec.get("train_mispredicted", 0) & 1
        train_taken = vec.get("train_taken", 0) & 1
        train_history = vec.get("train_history", 0) & 0xFFFFFFFF

        # R1_async_reset: asynchronous reset forces history to zero,
        # visible in the same cycle.
        if areset == 1:
            history = 0
        else:
            # R2_mispredict_priority: misprediction takes precedence over
            # prediction. Load history = {train_taken, train_history[31:1]}?
            # Spec: history before mispredicted branch (train_history)
            # concatenated with actual result (train_taken).
            # train_history is the history BEFORE the mispredicted branch,
            # so the youngest bit is train_taken at LSB, and train_history
            # shifted left by 1 (train_history[30:0] << 1 | train_taken).
            if train_mispredicted == 1:
                history = ((train_history << 1) | train_taken) & 0xFFFFFFFF
            # R3_predict_shift: shift right and insert predict_taken at MSB
            # per candidate interpretation: new = {predict_taken, history[31:1]}
            elif predict_valid == 1:
                history = ((predict_taken << 31) | (history >> 1)) & 0xFFFFFFFF
            # R4_hold: no update, history unchanged.

        # Output is the current value of the history register.
        results.append({"predict_history": history & 0xFFFFFFFF})

    return results
