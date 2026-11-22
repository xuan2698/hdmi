def reference(vectors):
    # Contract rules:
    # R1: reset == 1 on posedge -> q = 0 (sync, active high)
    # R2: reset == 0 && q < 9 on posedge -> q = q + 1
    # R3: reset == 0 && q == 9 on posedge -> q = 0
    # Mid changes occur AFTER sampling, before next edge, carried to next row.
    # Power-up state: q = 0 (concrete unsigned value required).

    q = 0  # named state: COUNT (4-bit counter value)
    out = []

    for row in vectors:
        reset = row.get("reset", 0)
        # Sample at posedge: apply synchronous update based on current inputs
        if reset == 1:
            # R1: synchronous active-high reset
            q = 0
        else:
            if q < 9:
                # R2: increment while below 9
                q = q + 1
            else:
                # R3: wrap from 9 to 0
                q = 0
        # Output visible same cycle after posedge settles
        out.append({"q": q & 0xF})

        # Mid changes (if any) occur AFTER sampling; they only affect
        # the next row's inputs, which are already read from the next vector.
        # No state mutation needed here for mid inputs.

    return out
