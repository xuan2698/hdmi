def reference(vectors):
    # State encoding: 0=A, 1=B, 2=C, 3=D
    state = 0  # concrete initial state for unspecified power-up
    cur_in = 0
    cur_reset = 0
    result = []
    for row in vectors:
        # Drive row values before the sampled edge
        if "in" in row:
            cur_in = row["in"]
        if "reset" in row:
            cur_reset = row["reset"]

        # Sample after active edge (negedge per global interpretation)
        # reset_to_A: synchronous active high reset resets FSM to state A
        if cur_reset == 1:
            next_state = 0
        else:
            # Explicit transitions from the state transition table
            if state == 0:  # A
                if cur_in == 0:
                    next_state = 0  # A
                else:
                    next_state = 1  # B
            elif state == 1:  # B
                if cur_in == 0:
                    next_state = 2  # C
                else:
                    next_state = 1  # B
            elif state == 2:  # C
                if cur_in == 0:
                    next_state = 0  # A
                else:
                    next_state = 3  # D
            else:  # state == 3, D
                if cur_in == 0:
                    next_state = 2  # C
                else:
                    next_state = 1  # B

        state = next_state

        # Moore outputs based on the new state after the edge
        # out_A: state A -> out 0
        # out_B: state B -> out 0
        # out_C: state C -> out 0
        # out_D: state D -> out 1
        if state == 3:
            out_val = 1
        else:
            out_val = 0

        result.append({"out": out_val})

        # Optional mid input changes occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row.
        if "mid" in row:
            mid = row["mid"]
            if "in" in mid:
                cur_in = mid["in"]
            if "reset" in mid:
                cur_reset = mid["reset"]

    return result
