def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    out = []

    for row in vectors:
        # Inputs for this row (driven before the sampled edge)
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0)
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_history = row.get('train_history', 0)
        train_pc = row.get('train_pc', 0)

        # Asynchronous active-high reset
        if areset:
            ghr = 0
            pht = [0] * 128
            out.append({
                'predict_taken': 0,
                'predict_history': 0,
            })
            continue

        # --- Combinational prediction outputs (before edge) ---
        predict_taken = 0
        predict_history = 0
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            predict_taken = 1 if pht[idx] >= 2 else 0
            predict_history = ghr & 0x7F

        # --- Compute next state (applied at posedge) ---
        next_ghr = ghr
        next_pht = list(pht)

        # Training updates PHT (takes effect at edge)
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            c = next_pht[tidx]
            if train_taken:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            next_pht[tidx] = c

        # GHR update: training has priority over prediction
        if train_valid and train_mispredicted:
            # Recover GHR to state after the mispredicting branch
            next_ghr = ((train_history << 1) | (train_taken & 1)) & 0x7F
        elif predict_valid:
            # Shift in predicted direction
            next_ghr = ((ghr << 1) | (predict_taken & 1)) & 0x7F
        # else: no change

        # Commit state at posedge
        ghr = next_ghr
        pht = next_pht

        out.append({
            'predict_taken': predict_taken,
            'predict_history': predict_history,
        })

    return out
