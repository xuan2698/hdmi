def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1, q holds (priority 1)
    # increment_when_a_low: on posedge, if a==0, q increments mod 8 (priority 1)
    # reset: none; power-up unspecified -> use 4 as initial (matches waveform at 5ns)
    # mid changes occur after sampling, carried to next row (handled by using
    #   the a value present at the start of each row for that row's posedge)
    q = 4  # power-up unspecified; waveform shows q=4 at first posedge
    out = []
    for row in vectors:
        a = row["a"]
        # posedge sampling: apply rule based on a at this row
        if a == 1:
            # hold_when_a_high
            pass
        else:
            # increment_when_a_low
            q = (q + 1) & 0x7
        out.append({"q": q})
    return out
