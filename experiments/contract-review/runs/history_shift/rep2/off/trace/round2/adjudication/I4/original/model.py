def reference(vectors):
    # State: 32-bit global branch history shift register.
    # bit 0 is the youngest branch direction.
    history = 0
    out = []

    for row in vectors:
        # R1_async_reset: asynchronous reset forces history to 0 (visible same cycle).
        if row["areset"] == 1:
            history = 0
        else:
            # R2_mispredict_priority: misprediction takes precedence over prediction.
            if row["train_mispredicted"] == 1:
                # history = train_history concatenated with train_taken
                # train_history is the history before the mispredicted branch;
                # train_taken is the actual result (youngest bit).
                history = ((row["train_history"] << 1) | (row["train_taken"] & 1)) & 0xFFFFFFFF
            # R3_predict_shift: shift in predict_taken from LSB side.
            elif row["predict_valid"] == 1:
                history = ((history << 1) | (row["predict_taken"] & 1)) & 0xFFFFFFFF
            # R4_hold: no update, history retains its value.
            else:
                pass

        out.append({"predict_history": history & 0xFFFFFFFF})

    return out
