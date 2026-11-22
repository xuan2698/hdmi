def reference(vectors):
    # FSM states: 0=no prefix, 1="1", 2="11", 3="110", 4=found (sticky)
    # start_shifting is registered; synchronous active-high reset has priority.
    state = 0
    start_shifting = 0
    out = []
    for row in vectors:
        # Values driven before the sampled posedge
        reset = row['reset'] & 1
        data = row['data'] & 1
        # Sample at posedge: compute next state and registered output
        if reset:
            state = 0
            start_shifting = 0
        else:
            if state == 4:
                state = 4
            elif state == 0:
                state = 1 if data == 1 else 0
            elif state == 1:
                state = 2 if data == 1 else 0
            elif state == 2:
                state = 3 if data == 0 else 2
            elif state == 3:
                if data == 1:
                    state = 4
                else:
                    state = 0
            if state == 4:
                start_shifting = 1
        out.append({'start_shifting': start_shifting})
        # Mid-cycle data changes occur after sampling; they do not affect
        # the registered output for this row and are carried to next row.
    return out
