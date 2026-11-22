def reference(vectors):
    # Contract implementation.
    # State: history (32-bit global branch history shift register).
    # Bit 0 is the youngest branch direction.
    #
    # Timing model:
    #   - Each row's inputs are driven before the sampled posedge.
    #   - We sample after the posedge has settled.
    #   - areset is asynchronous, active high, positive-edge triggered reset:
    #     when areset==1 the output is 0 in the same cycle (R1_async_reset).
    #   - Otherwise, on posedge:
    #       * train_mispredicted==1 -> history = (train_history << 1 | train_taken) & 0xFFFFFFFF
    #         (R2_mispredict_priority, takes precedence over predict)
    #       * else predict_valid==1 -> history = (history << 1 | predict_taken) & 0xFFFFFFFF
    #         (R3_predict_shift)
    #       * else hold (R4_hold)
    #   - "mid" changes occur after sampling and are carried to next row; since
    #     we only sample at posedge and the next row's inputs are driven before
    #     the next sampled edge, mid changes simply become the next row's inputs.
    #     We model this by using each row's inputs directly at its sample point.

    MASK = 0xFFFFFFFF
    history = 0  # power-up unspecified; use 0 as concrete value

    results = []
    for row in vectors:
        areset = int(row.get("areset", 0)) & 1
        predict_valid = int(row.get("predict_valid", 0)) & 1
        predict_taken = int(row.get("predict_taken", 0)) & 1
        train_mispredicted = int(row.get("train_mispredicted", 0)) & 1
        train_taken = int(row.get("train_taken", 0)) & 1
        train_history = int(row.get("train_history", 0)) & MASK

        # R1_async_reset: asynchronous reset visible same cycle, highest priority.
        if areset == 1:
            history = 0
            results.append({"predict_history": history & MASK})
            continue

        # R2_mispredict_priority: misprediction takes precedence over prediction.
        if train_mispredicted == 1:
            history = ((train_history << 1) | train_taken) & MASK
        # R3_predict_shift: shift in predict_taken from LSB side.
        elif predict_valid == 1:
            history = ((history << 1) | predict_taken) & MASK
        # R4_hold: no update, keep history.

        results.append({"predict_history": history & MASK})

    return results
