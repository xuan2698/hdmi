def reference(vectors):
    # Decade counter: 4-bit state, synchronous active-high reset to 0.
    # Counts 0..9 inclusive, wraps mod 10.
    # Each row: starting inputs (reset) drive the sampled posedge.
    # Mid-row changes occur AFTER sampling and carry to next row's start.
    # Power-up state is unspecified; first row with reset=0 is unconstrained.
    # Protocol seed 20261120: seed initial state deterministically.
    # Seed-derived initial state: use seed to pick a starting count in 0..9.
    seed = 20261120
    state = seed % 10  # deterministic power-up per protocol seed

    results = []
    for row in vectors:
        # Determine starting reset for this row.
        # If row provides 'reset', use it; otherwise carry from previous mid.
        if 'reset' in row:
            reset = row['reset']
        else:
            reset = carried_reset if 'carried_reset' in dir() else 0

        # Sample at posedge: compute next state from current state and starting reset.
        if reset:
            next_state = 0
        else:
            next_state = (state + 1) % 10

        # Settled output after edge.
        q = next_state
        results.append({'q': q & 0xF})

        # Adopt settled state.
        state = next_state

        # Process mid-row changes AFTER sampling; carry to next row.
        if 'mid' in row and row['mid'] is not None:
            mid = row['mid']
            if 'reset' in mid:
                carried_reset = mid['reset']
            else:
                carried_reset = reset
        else:
            carried_reset = reset

    return results
