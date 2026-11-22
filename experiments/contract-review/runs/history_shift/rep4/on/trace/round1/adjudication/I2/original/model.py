def reference(vectors):
    # State: 32-bit global branch history shift register (bit 0 = youngest branch)
    history = 0
    outputs = []

    for row in vectors:
        # Rule async_reset: areset == 1 asynchronously clears history to zero.
        if row.get('areset', 0):
            history = 0
            outputs.append({'predict_history': history & 0xFFFFFFFF})
            continue

        # Rule mispredict_load: highest priority after reset.
        if row.get('train_mispredicted', 0):
            train_history = row.get('train_history', 0)
            train_taken = row.get('train_taken', 0)
            history = ((train_history << 1) & 0xFFFFFFFF) | (train_taken & 1)

        # Rule predict_shift: shift in predict_taken from LSB side.
        elif row.get('predict_valid', 0):
            predict_taken = row.get('predict_taken', 0)
            history = ((history << 1) & 0xFFFFFFFF) | (predict_taken & 1)

        # Rule hold: retain history when neither update event occurs.
        else:
            history = history

        outputs.append({'predict_history': history & 0xFFFFFFFF})

    return outputs
