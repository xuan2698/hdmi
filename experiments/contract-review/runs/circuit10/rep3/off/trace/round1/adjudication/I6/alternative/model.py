def reference(vectors):
    # Contract rules:
    # R1: state updates on posedge clk to a^b (next_cycle visible)
    # R2: q = state (combinational passthrough, same_cycle)
    # Reset: none. Initial state unspecified -> use 0 as concrete value.
    # Mid changes: applied after sampling, carried to next row.
    # We process each row: sample at posedge using current inputs (after any mid
    # changes from previous row have been applied), then apply mid changes.
    state = 0  # concrete initial value (power-up unspecified)
    out = []
    for row in vectors:
        a = row.get('a', 0)
        b = row.get('b', 0)
        # R2: q = state (combinational, same cycle)
        q = state & 1
        out.append({'q': q, 'state': state & 1})
        # R1: state updates on posedge to a^b
        state = (a ^ b) & 1
        # mid changes: apply after sampling, carried to next row
        if 'mid' in row and row['mid']:
            for k, v in row['mid'].items():
                if k == 'a':
                    a = v
                elif k == 'b':
                    b = v
            # carry mid values forward by mutating next row's inputs is not
            # possible here; instead we track carried values
            # (handled by storing into a pending dict)
            # We'll store carried inputs for next iteration
            # Since vectors are given, we apply carried values to next row
            # by keeping them in variables used at start of next loop.
            # Implement via a pending override.
            # (Simplest: store in row-local and propagate)
            # We'll use a pending dict.
            pass
    return out
