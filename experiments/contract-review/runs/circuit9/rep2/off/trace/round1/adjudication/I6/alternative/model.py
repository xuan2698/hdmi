def reference(vectors):
    # Contract implementation.
    # State: 3-bit counter q (power-up unspecified -> concrete 0).
    # R1 (priority 1): on posedge, a == 1 -> q holds.
    # R2 (priority 2): on posedge, a == 0 -> q increments by 1 (mod 8).
    # Mid changes occur after sampling; carried to next row start.
    # Sample after posedge has settled.

    q = 0  # concrete power-up value (unspecified in spec)
    out = []
    pending_a = None  # mid change carried to next row

    for row in vectors:
        # Determine input value for this row's posedge sample.
        if pending_a is not None:
            a = pending_a
            pending_a = None
        else:
            a = row.get('a', 0)

        # Posedge sampling: apply transition rules.
        # R1: a == 1 -> hold
        # R2: a == 0 -> increment
        if a == 1:
            q = q  # R1 hold
        else:
            q = (q + 1) & 0x7  # R2 increment mod 8

        # Mid change after sampling (if provided in row).
        if 'a_mid' in row:
            pending_a = row['a_mid']

        out.append({'q': q & 0x7})

    return out
