def reference(vectors):
    # Contract rules:
    # R1: a == 1 on posedge -> q holds (priority 1)
    # R2: a == 0 on posedge -> q increments by 1 (mod 8) (priority 2)
    # State: count = 3-bit counter stored in q
    # Reset: none; power-up unspecified -> start at 0
    # Mid changes occur AFTER sampling, carried to next row.
    q = 0  # initial state (unspecified, choose 0)
    out = []
    for vec in vectors:
        a = vec.get('a', 0)
        # sample at posedge: apply rule based on a
        if a == 1:
            # R1: hold
            pass
        else:
            # R2: increment mod 8
            q = (q + 1) & 0x7
        out.append({'q': q})
    return out
