def reference(vectors):
    # Contract rules:
    # R1: on posedge, if a == 1, q holds (priority 1)
    # R2: on posedge, if a == 0, q increments by 1 mod 8 (priority 2)
    # State: count (3-bit), power-up unspecified -> use 0 as concrete value
    # Mid changes occur AFTER sampling, carried to next row.
    q = 0  # concrete power-up value (unspecified in spec)
    out = []
    for row in vectors:
        a = row.get('a', 0)
        # sample at posedge: apply transition based on current a
        if a == 1:
            # R1: hold
            pass
        else:
            # R2: increment mod 8
            q = (q + 1) % 8
        out.append({'q': q & 0x7})
    return out
