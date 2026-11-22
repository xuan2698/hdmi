def reference(vectors):
    # State: 32-bit global branch history shift register.
    # bit 0 is the youngest branch direction.
    history = 0  # power-up unspecified; use 0 as concrete value

    results = []

    for vec in vectors:
        areset = vec["areset"]
        predict_valid = vec["predict_valid"]
        predict_taken = vec["predict_taken"]
        train_mispredicted = vec["train_mispredicted"]
        train_taken = vec["train_taken"]
        train_history = vec["train_history"]

        # R1_async_reset: areset==1 asynchronously resets history to 0,
        # visible same cycle.
        if areset == 1:
            history = 0
            results.append({"predict_history": history & 0xFFFFFFFF})
            continue

        # Compute next state at posedge clk.
        # R2_mispredict_priority: train_mispredicted takes precedence.
        # Candidate interpretation: new history = train_history (ignoring train_taken).
        if train_mispredicted == 1:
            next_history = train_history & 0xFFFFFFFF
        # R3_predict_shift: shift in predict_taken from LSB side.
        elif predict_valid == 1:
            next_history = ((history << 1) | (predict_taken & 1)) & 0xFFFFFFFF
        # R4_hold: hold value.
        else:
            next_history = history

        # Output is the current register value (visible this cycle, before edge update).
        results.append({"predict_history": history & 0xFFFFFFFF})

        # Apply posedge update for next cycle.
        history = next_history

    return results
