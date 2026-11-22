def reference(vectors):
    history = 0
    prev_areset = 0
    outputs = []

    for row in vectors:
        areset = row.get("areset", 0)
        predict_valid = row.get("predict_valid", 0)
        predict_taken = row.get("predict_taken", 0)
        train_mispredicted = row.get("train_mispredicted", 0)
        train_taken = row.get("train_taken", 0)
        train_history = row.get("train_history", 0)

        # Rule reset_async: reset only on a rising edge of areset;
        # holding areset high does not block later posedge history updates.
        if areset == 1 and prev_areset == 0:
            history = 0
        else:
            # Rule mispredict_rollback: misprediction has highest update priority.
            if train_mispredicted == 1:
                history = (((train_history & 0xFFFFFFFF) << 1) | (train_taken & 1)) & 0xFFFFFFFF
            # Rule predict_shift: shift in predicted branch direction at LSB.
            elif predict_valid == 1:
                history = ((history << 1) | (predict_taken & 1)) & 0xFFFFFFFF
            # Rule hold_no_update: no update event, hold previous history.
            else:
                history = history & 0xFFFFFFFF

        outputs.append({"predict_history": history & 0xFFFFFFFF})
        prev_areset = areset

    return outputs
