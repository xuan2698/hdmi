def reference(vectors):
    # State
    pht = [0] * 128
    ghr = 0

    out = []

    for vec in vectors:
        # Apply asynchronous reset if asserted (active high)
        if vec.get('areset', 0):
            pht = [0] * 128
            ghr = 0

        # Compute outputs based on current state (before clock edge)
        predict_valid = vec.get('predict_valid', 0)
        predict_pc = vec.get('predict_pc', 0)
        train_valid = vec.get('train_valid', 0)
        train_taken = vec.get('train_taken', 0)
        train_mispredicted = vec.get('train_mispredicted', 0)
        train_history = vec.get('train_history', 0)
        train_pc = vec.get('train_pc', 0)

        # Prediction outputs (combinational, based on current state)
        if predict_valid:
            idx = (predict_pc & 0x7F) ^ (ghr & 0x7F)
            predict_taken = (pht[idx] >> 1) & 1
            predict_history = ghr & 0x7F
        else:
            # Still output current state values
            predict_taken = 0
            predict_history = ghr & 0x7F

        out.append({
            'predict_taken': predict_taken,
            'predict_history': predict_history
        })

        # Clock edge: update state
        # Training takes precedence for GHR
        if train_valid:
            # Update PHT
            tidx = (train_pc & 0x7F) ^ (train_history & 0x7F)
            if train_taken:
                if pht[tidx] < 3:
                    pht[tidx] += 1
            else:
                if pht[tidx] > 0:
                    pht[tidx] -= 1

            # Update GHR
            if train_mispredicted:
                ghr = ((train_history << 1) | (train_taken & 1)) & 0x7F
            # If not mispredicted, GHR not updated by training
        elif predict_valid:
            # Shift in predicted direction
            ghr = ((ghr << 1) | (predict_taken & 1)) & 0x7F

    return out
