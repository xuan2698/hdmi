def reference(vectors):
    # State: 32-bit global branch history shift register.
    # Bit 0 is the direction of the youngest branch.
    history = 0
    out = []

    for row in vectors:
        # R1_async_reset: asynchronous reset forces history to 0 immediately.
        if row["areset"] == 1:
            history = 0
        else:
            # R2_mispredict_priority: misprediction takes precedence over prediction.
            if row["train_mispredicted"] == 1:
                # Load history = train_history concatenated with train_taken.
                # train_history is the history before the mispredicted branch;
                # train_taken is the actual result of the branch.
                # Shift train_history left by 1 and insert train_taken at LSB.
                history = ((row["train_history"] << 1) | (row["train_taken"] & 1)) & 0xFFFFFFFF
            # R3_predict_shift: shift in predict_taken from LSB side.
            elif row["predict_valid"] == 1:
                history = ((history << 1) | (row["predict_taken"] & 1)) & 0xFFFFFFFF
            # R4_hold: no change.
            else:
                pass

        out.append({"predict_history": history & 0xFFFFFFFF})

    return out
