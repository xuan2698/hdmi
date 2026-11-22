def reference(vectors):
    # FSM states: 0=S0, 1=S1, 2=S2, 3=S3, 4=S4 (found)
    # start_shifting is registered output, latency 1 cycle.
    # Reset is active-high synchronous.
    state = 0
    start_shifting = 0
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        reset = row.get('reset', 0)
        data = row.get('data', 0)
        # Sample on posedge clk
        if clk == 1:
            if reset == 1:
                state = 0
                start_shifting = 0
            else:
                # compute next state
                if state == 0:
                    nxt = 1 if data == 1 else 0
                elif state == 1:
                    nxt = 2 if data == 1 else 0
                elif state == 2:
                    nxt = 2 if data == 1 else 3
                elif state == 3:
                    nxt = 4 if data == 1 else 0
                else:  # state == 4
                    nxt = 4
                state = nxt
                if state == 4:
                    start_shifting = 1
        out.append({'start_shifting': start_shifting & 1})
    return out
