def reference(vectors):
    # Contract implementation for a synchronous active-high-reset decade counter.
    # State: COUNT (current decade count 0..9). Initial value unspecified;
    # first posedge with reset==1 establishes q=0.
    # R1: reset==1 on posedge -> q=0 (same_cycle, priority 1)
    # R2: reset==0 && q<9 on posedge -> q=q+1 (same_cycle, priority 2)
    # R3: reset==0 && q==9 on posedge -> q=0 (same_cycle, priority 2)
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.

    q = 0  # initial state (unspecified; will be established by first reset)
    out = []

    for row in vectors:
        # Sample inputs driven before the posedge
        reset = row.get("reset", 0)

        # R1: synchronous active-high reset has priority
        if reset == 1:
            q = 0
        # R2: count up while below 9
        elif q < 9:
            q = q + 1
        # R3: wrap from 9 to 0
        else:
            q = 0

        # Output visible same cycle as the posedge
        out.append({"q": q & 0xF})

        # Mid changes occur AFTER sampling; carried to next row.
        # (No mid inputs affect this design's state directly.)

    return out
