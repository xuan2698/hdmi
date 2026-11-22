def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore FSM.
    # States: S0 (no 1 seen yet), S1 (a 1 has been seen).
    # Outputs are combinational from (state, x), except reset forces z=0.
    # Reset is asynchronous, active high, forces state to S0 and z=0.

    out = []
    state = "S0"  # power-up state (unspecified in spec; use S0)

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R5: asynchronous reset asserted -> state S0, z=0 immediately.
        if areset == 1:
            state = "S0"
            z = 0
            out.append({"z": z & 1})
            # R3/R4: state updates on posedge; during reset, update_during_reset=false,
            # so state stays S0. Mid changes carried to next row.
            continue

        # R1: In S0, z = x (pass through).
        # R2: In S1, z = NOT x (complement).
        if state == "S0":
            z = x & 1  # R1
        else:
            z = (~x) & 1  # R2

        out.append({"z": z & 1})

        # R3: On posedge, if x=1 -> next state S1; if x=0 stays S0.
        # R4: Once in S1, stays S1 regardless of x.
        if state == "S0":
            if x == 1:
                state = "S1"  # R3
            else:
                state = "S0"  # R3
        else:
            state = "S1"  # R4

    return out
