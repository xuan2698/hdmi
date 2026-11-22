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

        # Combinational prediction outputs (based on current state, before edge)
        predict_valid = row.get('predict_valid', 0)
        predict_pc = row.get('predict_pc', 0) & 0x7F
        train_valid = row.get('train_valid', 0)
        train_taken = row.get('train_taken', 0) & 1
        train_mispredicted = row.get('train_mispredicted', 0) & 1
        train_history = row.get('train_history', 0) & 0x7F
        train_pc = row.get('train_pc', 0) & 0x7F

        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            predict_taken = (pht[idx] >> 1) & 1
            predict_history = ghr & 0x7F
        else:
            predict_taken = 0
            predict_history = 0

        out.append({
            'predict_taken': predict_taken,
            'predict_history': predict_history,
        })

        # Sequential updates at posedge (skip if reset asserted)
        if not row.get('areset', 0):
            # Compute new GHR
            new_ghr = ghr
            if train_valid and train_mispredicted:
                # Training history recovery takes precedence
                new_ghr = ((train_history << 1) | train_taken) & 0x7F
            elif predict_valid:
                new_ghr = ((ghr << 1) | predict_taken) & 0x7F

            # PHT update
            if train_valid:
                tidx = (train_pc ^ train_history) & 0x7F
                c = pht[tidx]
                if train_taken:
                    if c < 3:
                        c += 1
                else:
                    if c > 0:
                        c -= 1
                pht[tidx] = c

            ghr = new_ghr

    return out
