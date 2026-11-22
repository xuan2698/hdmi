def reference(vectors):
    # Contract rules:
    # hold_when_a_high: on posedge, if a==1 and initialized, q holds.
    # increment_when_a_low: on posedge, if a==0 and initialized, q increments.
    # First posedge: q loads 4 regardless of a (initialization).
    # q is x before first posedge.
    # Mid changes occur after sampling, carried to next row.
    q = None  # x before first posedge
    initialized = False
    out = []
    for row in vectors:
        a = row.get('a', 0)
        # posedge sampling: apply state update
        if not initialized:
            # First posedge: load 4 regardless of a
            q = 4
            initialized = True
        else:
            if a == 1:
                # hold_when_a_high
                pass
            else:
                # increment_when_a_low
                q = (q + 1) & 0x7
        out.append({'q': q})
    return out
