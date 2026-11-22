def reference(vectors):
    # Contract implementation.
    # State: out_reg (32-bit), prev_in (32-bit), prev_in_valid (bool)
    # Timing: sample at posedge clk; mid changes applied after sampling.
    out_reg = 0
    prev_in = 0
    prev_in_valid = False
    results = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        inp = row.get('in', 0) & 0xFFFFFFFF

        # R1_reset_clear: sync reset clears out_reg (priority 1)
        if reset == 1:
            out_reg = 0
            prev_in_valid = False
            prev_in = inp
        else:
            # R2_capture_falling: capture 1->0 transitions (priority 2)
            if prev_in_valid:
                falling = prev_in & (~inp & 0xFFFFFFFF)
                if falling != 0:
                    out_reg = (out_reg | falling) & 0xFFFFFFFF
                # R3_hold: otherwise out_reg unchanged
            else:
                # first released cycle: no capture, out stays cleared
                pass
            prev_in = inp
            prev_in_valid = True

        results.append({'out': out_reg & 0xFFFFFFFF})

    return results
