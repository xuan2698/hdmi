def reference(vectors):
    # State: 32-bit global branch history shift register.
    # bit 0 = youngest branch direction.
    history = 0
    out = []

    for row in vectors:
        # ---- sample inputs (driven before the sampled posedge) ----
        areset = row.get("areset", 0) & 1
        predict_valid = row.get("predict_valid", 0) & 1
        predict_taken = row.get("predict_taken", 0) & 1
        train_mispredicted = row.get("train_mispredicted", 0) & 1
        train_taken = row.get("train_taken", 0) & 1
        train_history = row.get("train_history", 0) & 0xFFFFFFFF

        # R1_async_reset: areset==1 forces history to 0 (asynchronous, same cycle).
        if areset:
            history = 0
        else:
            # R2_mispredict_priority: misprediction takes precedence over prediction.
            if train_mispredicted:
                # history = train_history concatenated with train_taken,
                # where train_taken becomes the new LSB (youngest).
                history = ((train_history << 1) | train_taken) & 0xFFFFFFFF
            # R3_predict_shift: shift in predict_taken from LSB side.
            elif predict_valid:
                history = ((history << 1) | predict_taken) & 0xFFFFFFFF
            # R4_hold: no update, history unchanged.

        # Output reflects the (possibly updated) history register.
        out.append({"predict_history": history & 0xFFFFFFFF})

    return out
