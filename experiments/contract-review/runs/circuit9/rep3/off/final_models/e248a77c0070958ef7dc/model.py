def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds (priority 1)
    # increment_when_a_low: on posedge, if a==0, q increments mod 8 (priority 1)
    # reset: none; power-up unspecified -> start at 0
    # mid changes occur AFTER sampling, carried to next row
    q = 0  # power-up unspecified; concrete choice
    out = []
    for row in vectors:
        a = row.get('a', 0)
        # posedge sampling: apply rule based on a
        if a == 1:
            # hold_when_a_high
            pass
        else:
            # increment_when_a_low
            q = (q + 1) & 0x7
        out.append({'q': q})
        # mid changes after sampling: carried to next row (already reflected since we read a per row)
    return out
