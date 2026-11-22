def reference(vectors):
    # Contract implementation.
    # State: Q = stored flip-flop value (initial unspecified; we pick 0 as a concrete choice).
    # R1: posedge, r==1 -> q=0 (sync reset, priority 1)
    # R2: posedge, r==0 -> q=d (priority 2)
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # We model: each row's inputs are driven before the sampled posedge.
    # Mid changes: after sampling this row's posedge, inputs may change; those
    # changes are carried to the start of the next row. Since we only sample at
    # posedge and mid changes happen after sampling, they don't affect this row's
    # output but do affect the next row's starting inputs. We track pending mid
    # values to apply at the start of the next row.

    Q = 0  # initial value unspecified; concrete choice 0
    out = []
    pending = None  # mid changes carried to next row

    for row in vectors:
        # Apply carried mid changes from previous row (they occur before this row's posedge)
        if pending is not None:
            d = pending.get('d', row.get('d', 0))
            r = pending.get('r', row.get('r', 0))
        else:
            d = row.get('d', 0)
            r = row.get('r', 0)

        # Sample at posedge: compute next Q
        # R1: r==1 -> q=0 (priority 1)
        # R2: r==0 -> q=d (priority 2)
        if r == 1:
            Q = 0  # R1
        else:
            Q = d & 1  # R2

        out.append({'q': Q & 1})

        # Mid changes: after sampling, before other edge. We don't have explicit
        # mid data in the row format, so pending stays None unless provided.
        # (No mid field in vectors per contract; carried changes handled above.)
        pending = None

    return out
