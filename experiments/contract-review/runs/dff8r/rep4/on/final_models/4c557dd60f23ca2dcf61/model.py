def reference(vectors):
    # Registered 8-bit D flip-flop state; concrete power-up value chosen as 0.
    q = 0

    # Carried input state at start of each row. Mid changes update these for the next row.
    carried_d = 0
    carried_reset = 0

    outputs = []

    for row in vectors:
        # Row values are driven before the sampled posedge and override carried values.
        if "d" in row:
            carried_d = row["d"]
        if "reset" in row:
            carried_reset = row["reset"]

        # Rule sync_reset_high: reset == 1 at posedge clk synchronously clears q to zero.
        if carried_reset:
            q = 0
        else:
            # Rule dff_load_d: reset == 0 at posedge clk loads d into q.
            q = carried_d & 255

        # Output is visible same cycle after the posedge has settled.
        outputs.append({"q": q & 255})

        # Optional mid changes occur after sampling and are carried to the next row start.
        mid = row.get("mid")
        if mid:
            if "d" in mid:
                carried_d = mid["d"]
            if "reset" in mid:
                carried_reset = mid["reset"]

    return outputs
