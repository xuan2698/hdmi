def reference(vectors):
    # Contract implementation for a synchronous active-high-reset decade counter.
    # State: count (0..9). Output q = count.
    # R1: reset == 1 at posedge -> q = 0 (priority 1)
    # R2: reset == 0 && q == 9 at posedge -> q = 0 (priority 2)
    # R3: reset == 0 && q != 9 at posedge -> q = q + 1 (priority 3)
    # Mid changes occur AFTER sampling, before next edge, carried to next row.

    count = 0  # power-up state (concrete)
    results = []

    for row in vectors:
        # Sample inputs at the posedge (values driven before the edge)
        reset = row.get("reset", 0) & 1

        # Compute next state per priority rules
        if reset == 1:
            # R1: synchronous active-high reset
            next_count = 0
        elif count == 9:
            # R2: wrap from 9 to 0
            next_count = 0
        else:
            # R3: increment
            next_count = count + 1

        # Output visible same cycle (registered output equals new state after edge)
        q = next_count & 0xF
        results.append({"q": q})

        # Update state for next row
        count = next_count

        # Mid changes: applied after sampling, carried to next row.
        # They affect the next row's inputs, which are read from the next row dict,
        # so nothing extra needed here (mid changes are represented in next row).

    return results
