def reference(vectors):
    # rule reset_to_A: synchronous active high reset; reset has priority at posedge.
    # rule out_A: state == A -> out 0 (combinational, same_cycle)
    # rule out_B: state == B -> out 0 (combinational, same_cycle)
    # rule out_C: state == C -> out 0 (combinational, same_cycle)
    # rule out_D: state == D -> out 1 (combinational, same_cycle)
    state = "A"  # concrete initial state for unspecified power-up
    result = []
    for row in vectors:
        inp = row.get("in", 0)
        reset = row.get("reset", 0)

        # posedge update: synchronous reset and state transitions
        if reset == 1:
            state = "A"  # rule reset_to_A
        else:
            if state == "A":
                state = "A" if inp == 0 else "B"  # out_A transition
            elif state == "B":
                state = "C" if inp == 0 else "B"  # out_B transition
            elif state == "C":
                state = "A" if inp == 0 else "D"  # out_C transition
            elif state == "D":
                state = "C" if inp == 0 else "B"  # out_D transition

        # Moore output visible same_cycle after the sampled posedge settles
        if state == "A":
            out = 0  # rule out_A
        elif state == "B":
            out = 0  # rule out_B
        elif state == "C":
            out = 0  # rule out_C
        else:  # state == "D"
            out = 1  # rule out_D

        result.append({"out": out})
    return result
