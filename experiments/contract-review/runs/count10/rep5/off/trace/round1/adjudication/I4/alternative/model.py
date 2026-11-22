def reference(vectors):
    # Contract implementation.
    # State: q (4-bit counter), initialized to 0 (power-up unspecified; we pick 0).
    # R1: reset == 1 on posedge -> q = 0 (sync, active high, priority 1).
    # R2: reset == 0 && q < 9 on posedge -> q = q + 1 (priority 2).
    # R3: reset == 0 && q == 9 on posedge -> q = 0 (priority 3).
    # Mid changes occur AFTER sampling, before next edge, carried to next row start.
    # Each row: values driven before sampled edge; we sample on posedge.
    # We model: for each row, apply mid changes from previous row first (already
    # applied at end of previous iteration), then sample posedge with current inputs,
    # then apply this row's mid changes (if any) for next row.
    q = 0  # initial state (power-up unspecified; choose 0)
    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        # Sample on posedge with current inputs (R1/R2/R3)
        if reset == 1:
            # R1: sync reset to 0
            q = 0
        else:
            if q < 9:
                # R2: increment
                q = q + 1
            else:
                # R3: wrap from 9 to 0
                q = 0
        out.append({'q': q & 0xF})
        # Mid changes occur AFTER sampling, before other edge, carried to next row.
        # Since inputs are given per-row and mid changes are optional/unspecified,
        # we treat the row's reset as the value at sampling time. Any mid change
        # would be reflected in the next row's reset value already.
    return out
