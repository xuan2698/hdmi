def reference(vectors):
    # Contract implementation.
    # State: COUNT (4-bit counter value q), updated on posedge clk.
    # R1: reset == 1 on posedge -> q = 0 (sync, active high, priority 1)
    # R2: reset == 0 && q < 9 on posedge -> q = q + 1 (priority 2)
    # R3: reset == 0 && q == 9 on posedge -> q = 0 (priority 3)
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    q = 0  # power-up state (concrete)
    out = []
    for row in vectors:
        # Sample: apply current inputs at posedge
        reset = row.get('reset', 0)
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
        out.append({'q': q & 0xF})
        # Mid changes: apply after sampling, before next edge
        # (mid values carried to start of next row; here we just note them)
        # No mid handling needed beyond carrying inputs forward, which is
        # implicit since next row provides its own inputs.
    return out
