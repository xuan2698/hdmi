def reference(vectors):
    # FSM states: 0=initial, 1=prefix "1", 2=prefix "11", 3=prefix "110", 4=matched
    # Transition table for prefix regime (state, data) -> next state
    # state 0: 0->0, 1->1
    # state 1: 0->2, 1->1
    # state 2: 0->0, 1->3
    # state 3: 0->0, 1->4
    # state 4: absorbing (matched)
    trans = [
        [0, 1],
        [2, 1],
        [0, 3],
        [0, 4],
        [4, 4],
    ]
    state = 0
    out = []
    for row in vectors:
        # Inputs driven before the sampled edge
        reset = row.get('reset', 0) & 1
        data = row.get('data', 0) & 1
        # Sample at posedge: compute next state
        if reset:
            state = 0
        else:
            state = trans[state][data]
        start_shifting = 1 if state == 4 else 0
        out.append({'start_shifting': start_shifting})
        # Mid-cycle changes occur after sampling; they are carried to next row
        # (handled implicitly since next row's inputs are read fresh)
    return out
