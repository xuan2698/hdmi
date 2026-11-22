def reference(vectors):
    # Rule sync_reset: synchronous active high reset resets FSM to state A.
    # Rule transition_and_moore_output: posedge state transition and Moore output.
    state = 0  # A
    cur_reset = 0
    cur_in = 0
    result = []

    for row in vectors:
        # Inputs are driven before the sampled posedge.
        r = row.get("reset", cur_reset)
        v = row.get("in", cur_in)
        cur_reset = r
        cur_in = v

        # Rule sync_reset: reset has priority over in.
        if cur_reset == 1:
            state = 0
        else:
            # Rule transition_and_moore_output: explicit state transitions.
            if state == 0:          # A
                if cur_in == 0:
                    state = 0       # A
                else:
                    state = 1       # B
            elif state == 1:        # B
                if cur_in == 0:
                    state = 2       # C
                else:
                    state = 1       # B
            elif state == 2:        # C
                if cur_in == 0:
                    state = 0       # A
                else:
                    state = 3       # D
            else:                   # D
                if cur_in == 0:
                    state = 2       # C
                else:
                    state = 1       # B

        # Rule transition_and_moore_output: Moore output after the edge.
        if state == 3:              # D
            out = 1
        else:                       # A, B, C
            out = 0

        result.append({"out": out})

        # Mid changes occur after sampling and are carried to the next row.
        mid = row.get("mid", None)
        if mid is not None:
            try:
                cur_reset = mid.get("reset", cur_reset)
                cur_in = mid.get("in", cur_in)
            except:
                for change in mid:
                    cur_reset = change.get("reset", cur_reset)
                    cur_in = change.get("in", cur_in)

    return result
