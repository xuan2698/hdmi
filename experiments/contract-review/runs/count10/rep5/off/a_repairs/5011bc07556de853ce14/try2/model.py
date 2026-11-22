def reference(vectors):
    # Contract implementation.
    # State: COUNT (4-bit counter value q).
    # R1: reset == 1 on posedge -> q = 0 (sync, active high, priority 1).
    # R2: reset == 0 && q < 9 on posedge -> q = q + 1 (priority 2).
    # R3: reset == 0 && q == 9 on posedge -> q = 0 (priority 3).
    # Mid input changes occur AFTER sampling, before the other edge,
    # and are carried to the start of the next row.
    #
    # Power-up: q is unspecified; we start at 0. The first row's values
    # are driven before the sampled edge, so the first sample reflects
    # the transition from the initial state.

    q = 0  # initial COUNT state (power-up unspecified; choose 0)
    out = []
    for row in vectors:
        # Apply any mid changes carried from previous row are already in row.
        reset = row.get('reset', 0)
        # Sample at posedge clk: compute next state per rules.
        if reset == 1:
            # R1: sync active-high reset -> q = 0
            q = 0
        else:
            if q < 9:
                # R2: count up
                q = q + 1
            else:
                # R3: wrap from 9 to 0
                q = 0
        out.append({'q': q & 0xF})
    return out
