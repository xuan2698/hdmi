def reference(vectors):
    # State: 32-bit global branch history shift register.
    # bit 0 = direction of youngest branch.
    history = 0
    out = []

    for row in vectors:
        areset = row.get("areset", 0)
        predict_valid = row.get("predict_valid", 0)
        predict_taken = row.get("predict_taken", 0)
        train_mispredicted = row.get("train_mispredicted", 0)
        train_taken = row.get("train_taken", 0)
        train_history = row.get("train_history", 0)

        # R1_async_reset: asynchronous reset forces history to 0, visible same cycle.
        if areset == 1:
            history = 0
            out.append({"predict_history": history & 0xFFFFFFFF})
            continue

        # Compute next state at posedge clk.
        if train_mispredicted == 1:
            # R2_mispredict_priority: misprediction takes precedence over prediction.
            # history = train_history concatenated with train_taken (train_taken as LSB).
            history = ((train_history << 1) | (train_taken & 1)) & 0xFFFFFFFF
        elif predict_valid == 1:
            # R3_predict_shift: shift in predict_taken from LSB side.
            history = ((history << 1) | (predict_taken & 1)) & 0xFFFFFFFF
        else:
            # R4_hold: hold current value.
            history = history & 0xFFFFFFFF

        out.append({"predict_history": history & 0xFFFFFFFF})

    return out
