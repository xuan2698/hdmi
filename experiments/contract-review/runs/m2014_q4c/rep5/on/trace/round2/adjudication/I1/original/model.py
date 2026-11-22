def reference(vectors):
    # Power-up unspecified; choose a concrete initial output value.
    q = 0
    d = 0
    r = 0
    result = []

    for v in vectors:
        # Each row's values are driven before the sampled posedge edge.
        if "d" in v:
            d = v["d"]
        if "r" in v:
            r = v["r"]

        # Rule sync_active_high_reset: active-high synchronous reset.
        # Rule d_update_when_not_reset: when reset is inactive, q captures d.
        if r == 1:
            q = 0
        else:
            q = d & 1  # keep a concrete 1-bit unsigned value

        result.append({"q": q})

        # Optional mid changes occur AFTER sampling and are carried
        # to the start of the next row.
        if "mid" in v:
            mid = v["mid"]
            if "d" in mid:
                d = mid["d"]
            if "r" in mid:
                r = mid["r"]

    return result
