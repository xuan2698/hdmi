def reference(vectors):
    # Contract:
    # - 8 D flip-flops, negative-edge triggered.
    # - Active-high synchronous reset; on sampled negedge with reset=1, q <- 0x34.
    # - Otherwise on sampled negedge, q <- d.
    # - Power-up value is unspecified; only commit q after first sampled negedge.
    # - Mid changes occur after sampling, before the other edge, and carry to next row.
    # - Return per-row dict with 'q' as unsigned int in [0, 255].
    out = []
    q = None  # unknown until first sampled negedge
    pending_d = 0
    pending_reset = 0
    for row in vectors:
        # Apply pre-edge driven values for this row
        if 'd' in row:
            pending_d = row['d'] & 0xFF
        if 'reset' in row:
            pending_reset = row['reset'] & 0x1
        # Sampled negative edge: commit
        if pending_reset:
            q = 0x34
        else:
            q = pending_d & 0xFF
        # Mid changes after sampling, before next edge
        if 'mid_d' in row:
            pending_d = row['mid_d'] & 0xFF
        if 'mid_reset' in row:
            pending_reset = row['mid_reset'] & 0x1
        # Report q (concrete; if still None, use 0 as placeholder but it's committed now)
        out.append({'q': q if q is not None else 0})
    return out
