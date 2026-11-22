def reference(vectors):
    # Contract implementation.
    # State: COUNT (current decade count 0..9), updated at posedge clk.
    # Power-on: choose q = 0 (one of the allowed uncertain interpretations).
    q = 0
    out = []
    for row in vectors:
        # Inputs are driven before the sampled posedge.
        reset = row.get("reset", 0)
        # R1: reset == 1 at posedge -> q becomes 0 (sync, active high).
        # R2: reset == 0 && q < 9 -> q advances by 1.
        # R3: reset == 0 && q == 9 -> q wraps to 0.
        if reset == 1:
            q = 0  # R1
        else:
            if q < 9:
                q = q + 1  # R2
            else:
                q = 0  # R3
        # Output visible same cycle after posedge settles.
        out.append({"q": q & 0xF})
        # Mid changes occur AFTER sampling; they are carried to next row
        # via the next row's own input values, so nothing to do here.
    return out
