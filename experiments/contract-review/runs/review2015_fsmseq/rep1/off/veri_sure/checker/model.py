def reference(vectors):
    # State encoding: 0=S0, 1=S1, 2=S2, 3=S3, 4=S4
    state = 0
    start_shifting = 0
    out = []
    for row in vectors:
        # Apply inputs driven before the sampled posedge
        reset = row.get('reset', 0)
        data = row.get('data', 0)
        # Synchronous reset / state update on posedge
        if reset:
            state = 0
            start_shifting = 0
        else:
            if state == 0:
                state = 1 if data else 0
            elif state == 1:
                state = 2 if data else 0
            elif state == 2:
                state = 3 if not data else 2
            elif state == 3:
                state = 4 if data else 0
            elif state == 4:
                state = 4
            if state == 4:
                start_shifting = 1
        out.append({'start_shifting': start_shifting})
    return out
