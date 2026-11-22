def reference(vectors):
    # Moore 2's complementer, LSB-first.
    # State: 0 = Copy (output 0), 1 = Complement (output 1).
    # On posedge: if areset -> state=Copy, z=0.
    # else: update state from x (Copy: x=0->Copy, x=1->Complement; Complement stays),
    #       then z = state's output.
    state = 0
    out = []
    for row in vectors:
        areset = row.get('areset', 0) & 1
        x = row.get('x', 0) & 1
        if areset:
            state = 0
            z = 0
        else:
            if state == 0:
                if x == 1:
                    state = 1
            # else state stays 1
            z = state
        out.append({'z': z})
    return out
