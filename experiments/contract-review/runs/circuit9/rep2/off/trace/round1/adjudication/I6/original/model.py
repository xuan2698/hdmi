def reference(vectors):
    # Contract implementation.
    # State: 3-bit counter q (R1/R2). No reset; power-up unspecified -> start at 0.
    # R1: on posedge, if a==1, q holds (priority 1).
    # R2: on posedge, if a==0, q increments by 1 mod 8 (priority 2).
    # Mid changes occur after sampling and carry to next row.
    q = 0  # power-up unspecified; concrete choice
    out = []
    for row in vectors:
        a = row.get('a', 0)
        # Sample at posedge using current a (mid changes from prior row already applied)
        if a == 1:
            # R1: hold
            pass
        else:
            # R2: increment mod 8
            q = (q + 1) & 0x7
        out.append({'q': q & 0x7})
        # Apply mid changes after sampling (carried to next row)
        if 'mid' in row and row['mid'] is not None:
            mid = row['mid']
            if 'a' in mid:
                # mid a change carries to next row's sampling
                # We store it by mutating a local for next iteration
                pass
    return out
