def reference(vectors):
    # D flip-flop with active-high synchronous reset.
    # Each row: inputs d, r; clock clk; output q sampled after posedge.
    # Mid changes occur after sampling and carry to next row.
    # Power-up q is unspecified; first sampled edge defines it.
    q = None
    results = []
    for row in vectors:
        d = row.get('d', 0) & 1
        r = row.get('r', 0) & 1
        # Synchronous rule at sampled positive edge
        if r == 1:
            q = 0
        else:
            q = d
        results.append({'q': q & 1})
        # Apply mid changes after sampling for next row
        mid = row.get('mid', None)
        if mid:
            # mid changes carry into next row's starting inputs
            # (handled by next row's own d/r if provided; here we
            #  just note that no state change to q occurs)
            pass
    return results
