def reference(vectors):
    history = 0
    mask = 0xFFFFFFFF
    outputs = []
    for row in vectors:
        areset = row["areset"]
        # async_reset: priority 0, asynchronous clear to zero while areset high
        if areset:
            history = 0
        else:
            # mispredict_load: priority 1
            if row["train_mispredicted"]:
                train_history = row["train_history"] & mask
                train_taken = row["train_taken"] & 1
                history = ((train_history << 1) & mask) | train_taken
            # predict_shift: priority 2
            elif row["predict_valid"]:
                predict_taken = row["predict_taken"] & 1
                history = ((history << 1) & mask) | predict_taken
            # hold: priority 3, retain history when no update event occurs
            else:
                history = history
        outputs.append({"predict_history": history & mask})
    return outputs
