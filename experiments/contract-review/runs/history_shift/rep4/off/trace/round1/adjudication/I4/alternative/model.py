def reference(vectors):
    # State: 32-bit global branch history shift register.
    # Bit 0 is the youngest branch direction.
    history = 0
    prev_areset = 0
    out = []

    for row in vectors:
        areset = row["areset"]
        predict_valid = row["predict_valid"]
        predict_taken = row["predict_taken"]
        train_mispredicted = row["train_mispredicted"]
        train_taken = row["train_taken"]
        train_history = row["train_history"]

        # R1_async_reset: reset occurs only on a rising edge of areset
        # (candidate interpretation: holding areset high does not continuously reset).
        # Visible same cycle.
        if areset == 1 and prev_areset == 0:
            history = 0

        # Output is the current value of the history register (visible same cycle).
        out.append({"predict_history": history & 0xFFFFFFFF})

        # Compute next state at posedge clk.
        if areset == 1:
            # While areset is high, no state update (reset only on rising edge).
            next_history = history
        elif train_mispredicted == 1:
            # R2_mispredict_load: load history after completion of mispredicted branch:
            # train_history concatenated with actual result (train_taken) at LSB.
            next_history = ((train_history << 1) | (train_taken & 1)) & 0xFFFFFFFF
        elif predict_valid == 1:
            # R3_predict_shift: shift in predict_taken from LSB side.
            next_history = ((history << 1) | (predict_taken & 1)) & 0xFFFFFFFF
        else:
            # R4_hold: hold current value.
            next_history = history

        history = next_history
        prev_areset = areset

    return out
