def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    out = []

    for row in vectors:
        # Apply asynchronous reset if asserted (active high)
        if row.get('areset', 0):
            ghr = 0
            pht = [0] * 128

        # Combinational outputs (based on current state, before posedge updates)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0) & 0x7F
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0) & 1
        train_mispredicted = row.get('train_mispredicted', 0) & 1
        train_history = row.get('train_history', 0) & 0x7F
        train_pc = row.get('train_pc', 0) & 0x7F

        # Prediction index and output
        pred_index = (predict_pc ^ ghr) & 0x7F
        predict_taken = (pht[pred_index] >> 1) & 1
        predict_history = ghr & 0x7F

        out.append({
            'predict_taken': predict_taken,
            'predict_history': predict_history,
        })

        # Sequential updates at posedge (after sampling)
        # Training takes precedence for GHR update
        if train_valid:
            # Update PHT entry (saturating 2-bit counter)
            t_index = (train_pc ^ train_history) & 0x7F
            cnt = pht[t_index]
            if train_taken:
                if cnt < 3:
                    cnt += 1
            else:
                if cnt > 0:
                    cnt -= 1
            pht[t_index] = cnt

            if train_mispredicted:
                # Recover GHR to train_history shifted left with train_taken inserted
                ghr = ((train_history << 1) | train_taken) & 0x7F
            # If not mispredicted, GHR is not modified by training
        elif predict_valid:
            # Shift GHR left, insert predicted direction
            ghr = ((ghr << 1) | predict_taken) & 0x7F

    return out
