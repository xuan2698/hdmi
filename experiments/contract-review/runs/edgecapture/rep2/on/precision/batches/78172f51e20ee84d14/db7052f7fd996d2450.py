def reference(vectors):
    # Named state registers for the synchronous contract.
    out = 0
    prev_in = 0
    cur_reset = 0
    cur_in = 0
    mask = (1 << 32) - 1
    result = []

    for row in vectors:
        if row is None:
            row = {}

        # Drive explicit row input values before the sampled posedge.
        if "reset" in row:
            cur_reset = row["reset"] & 1
        if "in" in row:
            cur_in = row["in"] & mask

        sampled_reset = cur_reset & 1
        sampled_in = cur_in & mask

        # reset_clear: active-high synchronous reset has priority and clears out.
        # capture_fall: without reset, set bits sampled as a 1-to-0 transition.
        # hold_state: bits without a falling edge retain their previous value.
        if sampled_reset == 1:
            next_out = 0  # reset_clear
        else:
            falls = prev_in & (mask ^ sampled_in)  # capture_fall
            next_out = (out | falls) & mask  # capture_fall + hold_state

        # prev_in tracks in on every posedge, including reset cycles.
        out = next_out & mask
        prev_in = sampled_in

        # Same-cycle visible output after the posedge sampling settles.
        result.append({"out": out})

        # Apply optional mid changes after this posedge and before the next edge.
        # These carried values are used by the next row unless explicitly overridden.
        mid = row.get("mid", {})
        if mid:
            if "reset" in mid:
                cur_reset = mid["reset"] & 1
            if "in" in mid:
                cur_in = mid["in"] & mask

    return result
