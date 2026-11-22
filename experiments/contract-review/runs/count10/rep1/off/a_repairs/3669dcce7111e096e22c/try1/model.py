def reference(vectors):
    # Contract implementation.
    # State: COUNT (current decade count 0..9), updated on posedge.
    # Output q reflects COUNT after the sampled posedge.
    #
    # R1_SYNC_RESET: reset == 1 at posedge -> q becomes 0 (same_cycle visible).
    # R2_COUNT_INC: reset == 0 and q != 9 -> q increments.
    # R3_WRAP: reset == 0 and q == 9 -> q wraps to 0.
    #
    # The contract's "remaining_uncertain_fields" note for R1 says reset takes
    # effect at the posedge but q updates only on the following posedge, so q
    # remains previous value during the reset cycle. The example A failure
    # (cycle 3 expected 0, actual 1) indicates the intended behavior is that
    # reset is visible same_cycle (q=0 on the reset posedge). We implement
    # same_cycle reset per R1's "visible":"same_cycle" and the example vectors.

    count = 0  # power-up unspecified; start at 0
    out = []

    for row in vectors:
        reset = row.get("reset", 0)

        # R1_SYNC_RESET: synchronous active-high reset, visible same cycle.
        if reset == 1:
            count = 0
        else:
            # R2_COUNT_INC / R3_WRAP: increment modulo 10.
            if count == 9:
                count = 0
            else:
                count = count + 1

        out.append({"q": count & 0xF})

    return out
