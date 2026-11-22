def reference(vectors):
    # Contract implementation.
    # State: COUNT (current decade count 0..9), updated on posedge.
    # Output q reflects COUNT after the sampled posedge.
    # reset is active-high synchronous: on posedge with reset==1, COUNT -> 0.
    # Otherwise COUNT -> (COUNT + 1) % 10.
    # Mid input changes occur AFTER sampling, before the other edge,
    # and are carried to the start of the next row.

    count = 0  # power-up unspecified; use 0 as concrete value
    out = []

    for row in vectors:
        reset = row.get("reset", 0)

        # R1_SYNC_RESET: reset == 1 on posedge -> q = 0
        # R2_COUNT_INC: reset == 0 on posedge -> q = (q + 1) % 10
        # R3_WRAP: included in modulo-10 increment
        if reset == 1:
            count = 0
        else:
            count = (count + 1) % 10

        # Output visible same cycle after posedge settles
        out.append({"q": count & 0xF})

    return out
