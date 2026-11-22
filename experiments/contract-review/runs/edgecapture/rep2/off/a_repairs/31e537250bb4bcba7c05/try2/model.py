def reference(vectors):
    # Contract implementation.
    # State: out_reg (32-bit sticky), prev_in (32-bit previous input).
    # Initial prev_in is unspecified; choose 0 at time 0 (one of the candidates).
    out_reg = 0
    prev_in = 0

    results = []
    for row in vectors:
        reset = row["reset"] & 1
        inp = row["in"] & 0xFFFFFFFF

        # R1_reset_clear: synchronous reset clears out_reg at posedge.
        # R2_capture_falling: set bits where prev_in=1 and in=0.
        # R3_hold: otherwise hold.
        if reset == 1:
            # R1_reset_clear
            out_reg = 0
        else:
            # R2_capture_falling
            falling = prev_in & (~inp & 0xFFFFFFFF)
            out_reg = (out_reg | falling) & 0xFFFFFFFF
            # R3_hold is implicit: bits not in falling remain unchanged.

        # Output visible after posedge (same cycle for reset, next cycle for capture).
        results.append({"out": out_reg & 0xFFFFFFFF})

        # Update prev_in for next cycle. Mid changes occur after sampling,
        # carried to start of next row; here we simply latch current input.
        prev_in = inp

    return results
