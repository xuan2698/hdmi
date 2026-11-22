def reference(vectors):
    # State: 32-bit global branch history shift register.
    # Bit 0 is the direction of the youngest branch.
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
        if train_mispredicted == 1:
            # R2_mispredict_priority: misprediction takes precedence over prediction.
            # Load history = train_history concatenated with train_taken.
            # train_history is the history before the mispredicted branch;
            # train_taken is the actual result of the branch (youngest bit).
            # Concatenation: (train_history << 1) | train_taken, keeping 32 bits.
            history = ((train_history << 1) | train_taken) & 0xFFFFFFFF
        elif predict_valid == 1:
            # R3_predict_shift: shift in predict_taken from the LSB side.
            # Candidate interpretation: shift right inserting predict_taken at MSB.
            history = ((predict_taken << 31) | (history >> 1)) & 0xFFFFFFFF
        else:
            # R4_hold: hold history.
            history = history & 0xFFFFFFFF

        results.append({"predict_history": history & 0xFFFFFFFF})

    return results
