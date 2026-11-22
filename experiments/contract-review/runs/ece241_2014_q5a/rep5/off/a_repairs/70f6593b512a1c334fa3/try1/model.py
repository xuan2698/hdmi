def reference(vectors):
    # State machine implementation for 2's complementer Moore machine.
    # Contract rules implemented as comments.
    state = 'S0'  # initial state (power-up unspecified but we choose S0)
    out = []
    for row in vectors:
        areset = row.get('areset', 0)
        x = row.get('x', 0)
        # R5: Asynchronous reset asserted forces state S0 and z=0 immediately.
        if areset == 1:
            state = 'S0'
            z = 0
        else:
            # Combinational output based on current state (Moore: output depends on state only,
            # but here output also depends on x per R1/R2, so it's actually Mealy-like in spec;
            # however contract says Moore but rules R1/R2 are combinational with x).
            # R1: In state S0, z = x.
            # R2: In state S1, z = NOT x.
            if state == 'S0':
                z = x & 1
            else:  # S1
                z = (~x) & 1
        out.append({'z': z})
        # State update on posedge (sampled after edge settles).
        # R3: On posedge, if x=1 then next state S1; if x=0 stay S0 (from S0).
        # R4: Once in S1, state remains S1 regardless of x.
        if areset == 0:
            if state == 'S0':
                if x == 1:
                    state = 'S1'
                # else stay S0
            # else S1 stays S1
        # If areset==1, state already forced to S0 (async), no posedge update needed.
    return out
