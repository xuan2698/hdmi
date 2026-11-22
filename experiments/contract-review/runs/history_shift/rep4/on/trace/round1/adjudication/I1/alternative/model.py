def reference(vectors):
    history = 0
    prev_areset = 0
    results = []
    for row in vectors:
        areset = row.get("areset", 0)
        predict_valid = row.get("predict_valid", 0)
        predict_taken = row.get("predict_taken", 0)
        train_mispredicted = row.get("train_mispredicted", 0)
        train_taken = row.get("train_taken", 0)
        train_history = row.get("train_history", 0)

        # async_reset: edge-sensitive reset on rising areset; reset has priority.
        if areset == 1 and prev_areset == 0:
            history = 0
        # mispredict_load: load train_history concatenated with train_taken.
        elif train_mispredicted == 1:
            history = (((train_history << 1) & 0xFFFFFFFF) | (train_taken & 1)) & 0xFFFFFFFF
        # predict_shift: shift in predict_taken from the LSB side.
        elif predict_valid == 1:
            history = (((history << 1) & 0xFFFFFFFF) | (predict_taken & 1)) & 0xFFFFFFFF
        # hold: retain history when no update event occurs.
        else:
            history = history & 0xFFFFFFFF

        prev_areset = areset
        results.append({"predict_history": history & 0xFFFFFFFF})
    return results
