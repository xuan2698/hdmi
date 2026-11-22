def reference(vectors):
    # Contract implementation.
    # State: COUNT (current decade count 0..9), updated on posedge.
    # Output q reflects COUNT after the sampled posedge.
    # reset is active-high synchronous: on posedge with reset==1, COUNT <- 0.
    # Otherwise COUNT <- (COUNT + 1) mod 10.
    # Mid input changes occur AFTER sampling and are carried to next row.

    count = 0  # power-up state; unspecified but we choose 0
    out = []

    for row in vectors:
        # Determine reset value for this row's sampled edge.
        # Mid changes from previous row are already applied to 'row' by caller.
        reset = row.get("reset", 0)

        # R1_SYNC_RESET: reset == 1 on posedge -> q = 0
        # R2_COUNT_INC: reset == 0 -> increment
        # R3_WRAP: q == 9 -> wrap to 0
        if reset == 1:
            count = 0
        else:
            count = (count + 1) % 10

        out.append({"q": count & 0xF})

    return out
