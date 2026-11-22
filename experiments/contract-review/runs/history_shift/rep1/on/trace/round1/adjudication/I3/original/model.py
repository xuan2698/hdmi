def reference(vectors):
    MASK = 0xFFFFFFFF
    history = 0
    result = []

    for v in vectors:
        # reset_async: priority 0, asynchronous active-high reset forces zero.
        if v["areset"] == 1:
            history = 0
        else:
            # mispredict_rollback: priority 1, overrides prediction.
            if v["train_mispredicted"] == 1:
                history = (
                    ((v["train_history"] & MASK) << 1)
                    | (v["train_taken"] & 1)
                ) & MASK
            # predict_shift: priority 2, shift in predicted direction.
            elif v["predict_valid"] == 1:
                history = ((history << 1) | (v["predict_taken"] & 1)) & MASK
            else:
                # hold_no_update: priority 3, retain previous history.
                history = history & MASK

        result.append({"predict_history": history & MASK})

    return result
