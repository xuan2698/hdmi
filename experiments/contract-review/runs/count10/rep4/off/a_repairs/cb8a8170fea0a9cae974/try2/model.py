def reference(vectors):
    # Contract implementation.
    # State: COUNT (current decade count 0..9), updated at posedge clk.
    # reset is active-high synchronous: on posedge, if reset==1 -> q=0.
    # Otherwise q advances 0..9 then wraps to 0 (period 10).
    #
    # Timing contract:
    #  - Each row's inputs are driven before the sampled posedge.
    #  - Outputs are sampled after the posedge has settled (same_cycle visibility).
    #  - Optional mid input changes occur AFTER sampling, before the other edge,
    #    and are carried to the start of the next row.
    #
    # We model the counter state and apply the posedge update for each row
    # using the row's inputs (which include any carried mid changes from the
    # previous row). The output q reflects the state after that posedge.

    q = 0  # COUNT state; power-up unspecified but we use concrete 0.
    out = []

    for row in vectors:
        reset = row.get("reset", 0)

        # R1: reset == 1 at posedge -> q becomes 0 (priority 1).
        # R2: reset == 0 && q < 9 at posedge -> q becomes q + 1.
        # R3: reset == 0 && q == 9 at posedge -> q becomes 0.
        if reset == 1:
            # R1
            q = 0
        else:
            if q < 9:
                # R2
                q = q + 1
            else:
                # R3
                q = 0

        # Output visible same cycle after posedge settles.
        out.append({"q": q & 0xF})

    return out
