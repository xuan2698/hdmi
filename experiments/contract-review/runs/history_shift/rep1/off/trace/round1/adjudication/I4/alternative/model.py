def reference(vectors):
    # State: 32-bit global branch history shift register.
    # bit 0 is the youngest branch direction.
    history = 0
    prev_areset = 0
    out = []

    for row in vectors:
        areset = row["areset"] & 1
        predict_valid = row["predict_valid"] & 1
        predict_taken = row["predict_taken"] & 1
        train_mispredicted = row["train_mispredicted"] & 1
        train_taken = row["train_taken"] & 1
        train_history = row["train_history"] & 0xFFFFFFFF

        # R1_async_reset: reset occurs only on the rising edge of areset,
        # not while areset remains high. Visible same cycle.
        if areset == 1 and prev_areset == 0:
            history = 0

        # Output is the current value of the history register.
        out.append({"predict_history": history & 0xFFFFFFFF})

        # Clock edge (posedge) updates. Reset has priority (async reset
        # behavior modeled as edge-triggered per candidate interpretation).
        if areset == 1:
            # While areset is high, no clocked update occurs.
            pass
        else:
            if train_mispredicted == 1:
                # R2_mispredict_priority: misprediction takes precedence.
                # Load history = train_history concatenated with train_taken.
                # train_history holds the history before the mispredicted
                # branch; train_taken is the actual result (youngest bit).
                history = ((train_history << 1) | train_taken) & 0xFFFFFFFF
            elif predict_valid == 1:
                # R3_predict_shift: shift in predict_taken from LSB side.
                history = ((history << 1) | predict_taken) & 0xFFFFFFFF
            else:
                # R4_hold: hold current value.
                pass

        prev_areset = areset

    return out
