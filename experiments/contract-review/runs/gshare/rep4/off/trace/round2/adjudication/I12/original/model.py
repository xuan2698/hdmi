def reference(vectors):
    # State
    pht = [0] * 128          # 2-bit saturating counters
    ghr = 0                  # 7-bit global history register

    outputs = []

    def predict_taken_for(pc, hist):
        idx = (pc ^ hist) & 0x7F
        return 1 if pht[idx] >= 2 else 0

    for row in vectors:
        # Apply asynchronous reset immediately (R6)
        if row.get('areset', 0) == 1:
            pht = [0] * 128
            ghr = 0
            outputs.append({'predict_taken': 0, 'predict_history': 0})
            continue

        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0) & 0x7F
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0) & 1
        train_mispredicted = row.get('train_mispredicted', 0) & 1
        train_history = row.get('train_history', 0) & 0x7F
        train_pc = row.get('train_pc', 0) & 0x7F

        # Combinational prediction outputs (R1): read PHT and GHR before edge update
        if predict_valid:
            pred_taken = predict_taken_for(predict_pc, ghr)
            pred_history = ghr
        else:
            pred_taken = 0
            pred_history = 0

        outputs.append({'predict_taken': pred_taken, 'predict_history': pred_history})

        # Compute next-state updates (applied at posedge)
        new_pht = list(pht)
        new_ghr = ghr

        # R3: train PHT update
        if train_valid:
            idx = (train_pc ^ train_history) & 0x7F
            c = new_pht[idx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            new_pht[idx] = c

        # R4/R5: mispredicted training recovers GHR (takes precedence over prediction)
        if train_valid and train_mispredicted:
            new_ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid:
            # R2: prediction shifts in predicted direction
            new_ghr = ((ghr << 1) | pred_taken) & 0x7F

        pht = new_pht
        ghr = new_ghr

    return outputs
