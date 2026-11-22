def reference(vectors):
    # Contract implementation.
    # R1: a == 1 at posedge -> q holds (next_cycle).
    # R2: a == 0 at posedge -> q increments by 1 mod 8 (next_cycle).
    # global: q initializes to 0 at time 0.
    q = 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        # posedge sampling: apply transition based on current a
        if a == 1:
            # R1: hold
            pass
        else:
            # R2: increment mod 8
            q = (q + 1) % 8
        out.append({'q': q})
    return out
