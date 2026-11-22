def reference(vectors):
    # State: 32-bit global branch history shift register.
    # bit 0 = direction of youngest branch.
    history = 0  # power-up unspecified; use 0

    out = []
    for row in vectors:
        # ---- sample inputs (values driven before the sampled posedge) ----
        areset = row.get("areset", 0) & 1
        predict_valid = row.get("predict_valid", 0) & 1
        predict_taken = row.get("predict_taken", 0) & 1
        train_mispredicted = row.get("train_mispredicted", 0) & 1
        train_taken = row.get("train_taken", 0) & 1
        train_history = row.get("train_history", 0) & 0xFFFFFFFF

        # R1_async_reset: areset==1 -> history=0, visible same cycle (async).
        if areset == 1:
            history = 0
        else:
            # R2_mispredict_priority: train_mispredicted==1 takes precedence.
            # Load history = train_history concatenated with train_taken.
            # train_history is the history BEFORE the mispredicted branch;
            # train_taken is the actual result (youngest bit).
            if train_mispredicted == 1:
                history = ((train_history << 1) | train_taken) & 0xFFFFFFFF
            # R3_predict_shift: predict_valid==1 -> shift in predict_taken at LSB.
            elif predict_valid == 1:
                history = ((history << 1) | predict_taken) & 0xFFFFFFFF
            # R4_hold: otherwise hold.

        # Output reflects current (post-edge) history value.
        out.append({"predict_history": history & 0xFFFFFFFF})

    return out
