def reference(vectors):
    # State: Q register, reset value 0x34 (52)
    Q = 0x34  # R3_reset_value: power-up/reset value 0x34

    out = []
    for row in vectors:
        d = row['d'] & 0xFF
        reset = row['reset'] & 0x1

        # R1_sync_reset (candidate interpretation): reset does not override d;
        # d is captured and reset only affects next cycle.
        # R2_dff_capture: on negedge, capture d when reset==0.
        # R3_reset_value: on negedge with reset==1, Q becomes 0x34.
        # Sampling occurs at negedge; visible same cycle.
        if reset == 1:
            # R1_sync_reset / R3_reset_value: reset to 0x34 at negedge
            Q = 0x34
        else:
            # R2_dff_capture: capture d at negedge
            Q = d

        out.append({'q': Q & 0xFF})

    return out
