def reference(vectors):
    MASK = 0xFFFFFFFF
    history = 0
    outputs = []

    for row in vectors:
        # Read sampled input values before the sampled posedge.
        areset = int(row.get("areset", 0)) & 1
        predict_valid = int(row.get("predict_valid", 0)) & 1
        predict_taken = int(row.get("predict_taken", 0)) & 1
        train_mispredicted = int(row.get("train_mispredicted", 0)) & 1
        train_taken = int(row.get("train_taken", 0)) & 1
        train_history = int(row.get("train_history", 0)) & MASK

        if areset:
            # Rule async_reset: asynchronous high reset clears history to zero.
            history = 0
        elif train_mispredicted:
            # Rule mispredict_load: highest-priority normal update.
            # history_next = ((train_history << 1) & 0xFFFFFFFF) | train_taken
            history = (((train_history << 1) & MASK) | train_taken) & MASK
        elif predict_valid:
            # Rule predict_shift: shift in predict_taken from LSB.
            # history_next = ((history << 1) & 0xFFFFFFFF) | predict_taken
            history = (((history << 1) & MASK) | predict_taken) & MASK
        else:
            # Rule hold, using supplied unresolved interpretation:
            # idle cycles shift left and insert zero at LSB.
            history = (history << 1) & MASK

        outputs.append({"predict_history": history & MASK})

    return outputs
