def reference(vectors):
    # sync_reset_high: active-high synchronous reset forces q=0 at a sampled posedge.
    # count_decade_mod10: when reset==0, q increments modulo 10.
    q = 0
    inputs = {"reset": 0}
    result = []
    for row in vectors:
        # Each row's values are driven before the sampled posedge.
        if "reset" in row:
            inputs["reset"] = row["reset"] & 1
        reset = inputs["reset"]
        # At the sampled posedge, update state; reset has priority.
        if reset:
            q = 0
        else:
            q = q + 1
            if q == 10:
                q = 0
        # Output is visible in the same cycle after the posedge has settled.
        result.append({"q": q})
        # Optional mid changes occur after sampling and are carried to the next row.
        if "mid" in row:
            m = row["mid"]
            if m:
                try:
                    inputs["reset"] = m["reset"] & 1
                except:
                    inputs["reset"] = m & 1
    return result
