def reference(vectors):
    # State encoding: START=0, INV0=1, INV1=2
    START = 0
    INV0 = 1
    INV1 = 2
    state = START
    z = 0
    current = {}
    results = []

    for row in vectors:
        # R_CONVERT: Apply row's driven input values before the sampled edge
        for key, val in row.items():
            if key != 'mid':
                current[key] = val

        areset = current.get('areset', 0)
        x = current.get('x', 0)

        # R_RESET: asynchronous reset has priority
        if areset == 1:
            state = START
            z = 0
        else:
            # R_CONVERT: posedge clk transition when reset deasserted
            if state == START:
                if x == 0:
                    state = START
                else:
                    state = INV1
            elif state == INV0:
                if x == 0:
                    state = INV1
                else:
                    state = INV0
            else:  # INV1
                if x == 0:
                    state = INV1
                else:
                    state = INV0

            # Moore output from new state
            if state == START:
                z = 0
            elif state == INV0:
                z = 0
            else:  # INV1
                z = 1

        # Record post-posedge same-cycle Moore output
        results.append({'z': z})

        # Process mid changes after sampling, before next edge
        if 'mid' in row:
            mid = row['mid']
            for key, val in mid.items():
                current[key] = val
            # R_RESET: asynchronous reset can be asserted in mid
            if mid.get('areset', 0) == 1:
                state = START
                z = 0

    return results
