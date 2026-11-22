def reference(vectors):
    # State machine implementation for 2's complementer Moore machine
    # States: S0 (no 1 seen yet), S1 (at least one 1 seen)
    # R5: async reset forces state to S0 and z=0 immediately
    # R1: In S0, z = x
    # R2: In S1, z = NOT x
    # R3: On posedge, if x=1 then next state is S1; if x=0 state stays S0
    # R4: On posedge, once in S1, state remains S1 regardless of x
    
    results = []
    state = 'S0'  # initial state (power-up unspecified but we start at S0)
    
    for vec in vectors:
        areset = vec.get('areset', 0)
        x = vec.get('x', 0)
        
        # R5: Asynchronous reset - forces state to S0 and z=0 immediately
        if areset == 1:
            state = 'S0'
            z = 0
        else:
            # R1: In state S0, z = x (pass through)
            # R2: In state S1, z = NOT x (complement)
            if state == 'S0':
                z = x
            else:  # S1
                z = 1 - x  # NOT x
        
        results.append({'z': z})
        
        # R3/R4: State transition on posedge (sampled after edge settles)
        # Only update state if not in reset
        if areset == 0:
            if state == 'S0':
                if x == 1:
                    state = 'S1'  # R3: first 1 seen
                # else stays S0
            else:  # S1
                state = 'S1'  # R4: remains S1 regardless of x
    
    return results
