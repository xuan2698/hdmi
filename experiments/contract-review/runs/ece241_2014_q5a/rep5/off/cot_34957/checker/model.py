def reference(vectors):
    # 2's complementer, LSB-first, Moore machine.
    # States: S0 (still copying zeros / not yet seen a 1), S1 (inverting).
    # Output: z = 0 in S0, z = 1 in S1.
    # areset is active-high asynchronous: forces S0.
    # z is sampled after the posedge has settled, reflecting the state
    # reached by consuming this row's x on this edge.
    # Ignore z until reset has been asserted and released.
    state = 0  # unspecified power-up; will be forced by reset
    reset_seen = False
    reset_released = False
    out = []
    for row in vectors:
        areset = row.get('areset', 0) & 1
        x = row.get('x', 0) & 1
        # Asynchronous reset: takes effect immediately (before edge).
        if areset:
            state = 0
            reset_seen = True
            reset_released = False
        else:
            if reset_seen:
                reset_released = True
            # Positive edge: consume x, update state.
            if state == 0:
                if x == 1:
                    state = 1
            else:
                state = 1
        # Settled output after edge (Moore: depends only on state).
        z = 1 if state == 1 else 0
        if not (reset_seen and reset_released):
            # Power-up / pre-reset: z unspecified; report 0.
            z = 0
        out.append({'z': z})
    return out
