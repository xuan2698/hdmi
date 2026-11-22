def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds (priority 1)
    # increment_when_a_low: on posedge, if a==0, q increments by 1 (mod 8)
    # reset: none; power-up unspecified -> use 0 as concrete initial value
    # mid: input changes after sampling carry to next row (handled by using
    #      each row's 'a' as the value driven before that row's posedge)
    q = 0  # power-up unspecified; concrete initial value
    out = []
    for row in vectors:
        a = row.get('a', 0)
        # posedge sampling: apply transition based on a
        if a == 1:
            # hold_when_a_high
            q = q & 0x7
        else:
            # increment_when_a_low
            q = (q + 1) & 0x7
        out.append({'q': q})
    return out
