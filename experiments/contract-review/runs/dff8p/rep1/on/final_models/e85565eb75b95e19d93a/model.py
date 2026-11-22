def reference(vectors):
    # State: q is the 8-bit D flip-flop output register.
    # Initial concrete power-up value chosen as 0 (unspecified until first negedge).
    q = 0
    # Inputs carried across rows. Initial values are 0.
    cur_d = 0
    cur_reset = 0
    out = []

    for row in vectors:
        # Each row's values are driven before the sampled negedge.
        # Apply any explicitly provided main input values.
        if "d" in row:
            cur_d = row["d"]
        if "reset" in row:
            cur_reset = row["reset"]

        # Rule sync_reset_high: reset == 1 on a negedge; q becomes 52 (0x34)
        # regardless of d. This has priority over the D update.
        # Rule negedge_d_update: reset == 0 on a negedge; q captures d.
        if cur_reset == 1:
            q = 52
        else:
            q = cur_d & 255  # keep within 8-bit unsigned width

        # Output is visible same cycle after the negedge has settled.
        out.append({"q": q})

        # Optional mid input changes occur AFTER sampling and before the other edge.
        # They are carried to the start of the next row.
        if "mid" in row:
            mid = row["mid"]
            if "d" in mid:
                cur_d = mid["d"]
            if "reset" in mid:
                cur_reset = mid["reset"]

    return out
