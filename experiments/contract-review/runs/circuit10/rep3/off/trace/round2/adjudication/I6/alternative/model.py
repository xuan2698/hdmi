def reference(vectors):
    # Contract implementation.
    # R1: state updates on posedge clk (next_cycle). Initial state unspecified -> use 0.
    # R2 (candidate interpretation): q = state XOR (a XOR b), combinational same_cycle.
    # Mid changes occur after sampling; carried to next row. We process each row's
    # inputs as the values present at the sampled posedge.
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0) & 1
        b = v.get('b', 0) & 1
        # R2: combinational output using current state
        q = (state ^ (a ^ b)) & 1
        out.append({'q': q, 'state': state & 1})
        # R1: next state on posedge. Determine next-state function from waveform.
        # Observed transitions (state -> next) given (a,b):
        #  (0,0,0)->0 ; (0,0,1)->1 ; (0,1,0)->1 ; (0,1,1)->0
        #  (1,0,0)->1 ; (1,0,1)->0 ; (1,1,0)->0 ; (1,1,1)->1
        # This is next = state XOR a XOR b? Check:
        #  state=0,a=0,b=1 -> 1 yes; state=0,a=1,b=0 -> 1 yes; state=0,a=1,b=1 -> 0 yes
        #  state=1,a=0,b=0 -> 1 yes; state=1,a=0,b=1 -> 0 yes; state=1,a=1,b=0 -> 0 yes; state=1,a=1,b=1 -> 1 yes
        # So next_state = state XOR a XOR b.
        state = (state ^ a ^ b) & 1
    return out
