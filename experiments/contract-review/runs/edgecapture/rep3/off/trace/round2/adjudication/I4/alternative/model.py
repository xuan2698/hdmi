def reference(vectors):
    # Contract implementation.
    # State: out_reg (32-bit), prev_in (32-bit), initialized to 0.
    # Clock: posedge clk. Sample after posedge settled.
    # reset: active high synchronous.
    # R1_reset_clear: reset==1 -> out <= 0 (same cycle visible).
    # R2_capture_falling: reset==0 && (prev_in & ~in)!=0 -> out <= out | (prev_in & ~in).
    # R3_hold: reset==0 && no falling -> out <= out.
    # Global interpretation: on first posedge with reset==0, if prev_in&~in nonzero,
    #   capture falling edge rather than clearing to 0. (prev_in starts at 0, so
    #   prev_in&~in is 0 on first cycle anyway; but we honor the rule explicitly.)
    # mid: optional mid input changes occur AFTER sampling, before other edge,
    #   carried to start of next row. We process mid after computing outputs.

    out_reg = 0
    prev_in = 0
    first_released = True  # tracks first posedge with reset==0

    results = []
    for row in vectors:
        reset = row.get("reset", 0)
        in_val = row.get("in", 0)
        # Mask to 32 bits
        reset = reset & 1
        in_val = in_val & 0xFFFFFFFF

        # Compute falling edges based on prev_in and current in
        fall = prev_in & (~in_val & 0xFFFFFFFF)

        if reset == 1:
            # R1_reset_clear
            out_reg = 0
            first_released = True
        else:
            if first_released:
                # Global interpretation: on first posedge with reset==0,
                # capture falling edge if nonzero rather than clearing.
                if fall != 0:
                    out_reg = out_reg | fall
                # else out_reg stays (which is 0 from reset)
                first_released = False
            else:
                if fall != 0:
                    # R2_capture_falling
                    out_reg = out_reg | fall
                else:
                    # R3_hold
                    out_reg = out_reg

        # Output visible same cycle for reset, next cycle for capture/hold.
        # Per contract, out is the register value after this posedge.
        results.append({"out": out_reg & 0xFFFFFFFF})

        # Update prev_in for next cycle
        prev_in = in_val

        # mid: optional mid input changes occur AFTER sampling, before other edge,
        # carried to start of next row. Apply mid if present.
        mid = row.get("mid")
        if mid is not None:
            if "in" in mid:
                prev_in = mid["in"] & 0xFFFFFFFF
            if "reset" in mid:
                # mid reset change carried to next row's reset input
                # We store it as an override for next row's reset
                # Since next row provides reset, mid reset would override.
                # We'll track via a pending override.
                pass

    return results
