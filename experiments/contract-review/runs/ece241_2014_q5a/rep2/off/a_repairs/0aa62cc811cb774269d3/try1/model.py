def reference(vectors):
    # State machine: S0 (no 1 seen yet), S1 (1 seen, complementing)
    # R4: async reset -> S0, z=0
    # R1: S0 -> z = x
    # R2: S1 -> z = NOT x
    # R3: posedge: S0->S1 if x=1, S0->S0 if x=0, S1->S1 always
    # Mid changes occur after sampling, carried to next row.

    state = "S0"
    out = []

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R4: asynchronous reset asserted -> state S0, z=0 (same cycle)
        if areset == 1:
            state = "S0"
            z = 0
            out.append({"z": z})
            # mid changes after sampling: apply to state for next row
            mid = row.get("mid")
            if mid:
                if "areset" in mid and mid["areset"] == 1:
                    state = "S0"
                if "x" in mid:
                    # x mid change doesn't affect state until next posedge
                    pass
            continue

        # Combinational output based on current state (R1/R2)
        if state == "S0":
            z = x  # R1
        else:
            z = 1 - x  # R2

        out.append({"z": z})

        # R3: posedge transition (takes effect after current cycle's output)
        if state == "S0":
            if x == 1:
                state = "S1"
            # else stay S0
        # S1 stays S1

        # Mid changes after sampling, carried to next row
        mid = row.get("mid")
        if mid:
            if "areset" in mid and mid["areset"] == 1:
                state = "S0"
            if "x" in mid:
                # x mid change: state transition already computed from sampled x
                # but per contract, mid changes are carried to start of next row,
                # meaning they don't affect this row's posedge transition.
                pass

    return out
