def reference(vectors):
    # Contract rules:
    # R1: a == 1 on posedge -> q holds (priority 1)
    # R2: a == 0 on posedge -> q increments by 1 mod 8 (priority 2)
    # State: count (3-bit), power-up unspecified -> use 4 as concrete initial
    # Mid changes occur after sampling, carried to next row.
    q = 4  # concrete power-up value (unspecified in spec)
    out = []
    for row in vectors:
        a = row.get('a', 0)
        # posedge sampling: apply transition based on a
        if a == 1:
            # R1: hold
            pass
        else:
            # R2: increment mod 8
            q = (q + 1) % 8
        out.append({'q': q & 0x7})
    return out
