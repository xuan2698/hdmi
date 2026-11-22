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

        # Combinational prediction outputs (before edge update)
        pv = row.get('predict_valid', 0)
        ppc = row.get('predict_pc', 0) & 0x7F
        if pv:
            pidx = (ppc ^ ghr) & 0x7F
            predict_taken = (pht[pidx] >> 1) & 1
            predict_history = ghr & 0x7F
        else:
            # No prediction request: outputs still driven from current state
            # (index computed from predict_pc anyway, but taken from PHT)
            pidx = (ppc ^ ghr) & 0x7F
            predict_taken = (pht[pidx] >> 1) & 1
            predict_history = ghr & 0x7F

        out.append({
            'predict_taken': predict_taken & 1,
            'predict_history': predict_history & 0x7F,
        })

        # Edge updates (posedge)
        tv = row.get('train_valid', 0)
        tm = row.get('train_mispredicted', 0)
        tt = row.get('train_taken', 0)
        th = row.get('train_history', 0) & 0x7F
        tpc = row.get('train_pc', 0) & 0x7F

        # Training PHT update
        if tv:
            tidx = (tpc ^ th) & 0x7F
            c = pht[tidx]
            if tt:
                if c < 3:
                    c += 1
            else:
                if c > 0:
                    c -= 1
            pht[tidx] = c

        # GHR update: training misprediction takes precedence
        if tv and tm:
            # Recover GHR to train_history shifted in with train_taken
            ghr = ((th << 1) | (tt & 1)) & 0x7F
        elif pv:
            # Shift in predicted direction
            ghr = ((ghr << 1) | (predict_taken & 1)) & 0x7F

        # Handle mid-cycle input changes (after sampling, before next edge)
        # These are carried to the start of the next row.
        # The harness may provide 'mid' dict; apply changes to inputs for next row.
        mid = row.get('mid')
        if mid:
            # Mid changes affect inputs for the next row; we store them by
            # mutating a pending overlay that the next iteration will see.
            # Since vectors are given as rows, we assume the harness already
            # merged mid changes into the next row's inputs. Nothing to do here.
            pass

    return out
