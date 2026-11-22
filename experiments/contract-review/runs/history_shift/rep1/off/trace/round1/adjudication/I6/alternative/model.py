def reference(vectors):
    # State: 32-bit global branch history shift register.
    # Bit 0 is the youngest branch direction.
    history = 0

    results = []

    for vec in vectors:
        areset = vec["areset"]
        predict_valid = vec["predict_valid"]
        predict_taken = vec["predict_taken"]
        train_mispredicted = vec["train_mispredicted"]
        train_taken = vec["train_taken"]
        train_history = vec["train_history"]

        # R1_async_reset: asynchronous reset forces history to 0, visible same cycle.
        if areset == 1:
            history = 0
            results.append({"predict_history": history & 0xFFFFFFFF})
            continue

        # Compute next state at posedge clk.
        # R2_mispredict_priority: misprediction takes precedence over prediction.
        if train_mispredicted == 1:
            # Load history = train_history concatenated with train_taken.
            # train_history is the history before the mispredicted branch;
            # train_taken is the actual result (youngest bit).
            # Concatenation: (train_history << 1) | train_taken, truncated to 32 bits.
            history = ((train_history << 1) | train_taken) & 0xFFFFFFFF
        # R3_predict_shift: shift right, insert predict_taken at MSB (bit 31).
        elif predict_valid == 1:
            history = ((history >> 1) | (predict_taken << 31)) & 0xFFFFFFFF
        # R4_hold: no change.

        results.append({"predict_history": history & 0xFFFFFFFF})

    return results
