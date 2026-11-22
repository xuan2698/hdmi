def reference(vectors):
    # state update: state_next = majority(a, b, state) = (a&b) | (a&state) | (b&state)
    # q = a ^ b ^ state
    # state shown in row is state BEFORE posedge (for clk=1 rows)
    # for clk=0 rows, state is unchanged from previous row
    # x treated as 0
    
    results = []
    state = 0  # initial power-up state (unspecified, using 0)
    
    for row in vectors:
        clk = row.get('clk', 0)
        a = row.get('a', 0)
        b = row.get('b', 0)
        # treat x as 0
        if a is None or a == 'x': a = 0
        if b is None or b == 'x': b = 0
        if clk is None or clk == 'x': clk = 0
        
        # state shown in this row is current state (before posedge)
        q = (a ^ b ^ state) & 1
        
        results.append({'q': q, 'state': state})
        
        # update state at posedge
        if clk == 1:
            state = ((a & b) | (a & state) | (b & state)) & 1
    
    return results
