def reference(vectors):
    # State
    out = [0] * 32
    prev = [0] * 32
    have_prev = False
    seen_reset = False

    results = []

    for row in vectors:
        # Sampled values for this row
        reset = row.get('reset', 0) & 1
        in_val = row.get('in', 0) & 0xFFFFFFFF

        # Process sampled edge
        if reset:
            # Synchronous active-high reset: force outputs to 0, no capture
            out = [0] * 32
            seen_reset = True
            # Still update history to sampled input
            for i in range(32):
                prev[i] = (in_val >> i) & 1
            have_prev = True
        else:
            if have_prev:
                for i in range(32):
                    cur = (in_val >> i) & 1
                    if prev[i] == 1 and cur == 0:
                        out[i] = 1
                    prev[i] = cur
            else:
                # First sampled input without prior reset: track history only
                for i in range(32):
                    prev[i] = (in_val >> i) & 1
                have_prev = True

        # Build output value
        out_val = 0
        for i in range(32):
            if out[i]:
                out_val |= (1 << i)

        results.append({'out': out_val})

        # Mid changes occur after sampling; they do not affect current row.
        # They are carried to the start of the next row, but since we read
        # 'in' from the next row's dict, mid changes are already reflected
        # there. Nothing extra to do.

    return results
