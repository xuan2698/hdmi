def reference(vectors):
    # Contract implementation.
    # R1: state is a single flip-flop updated on posedge clk (next_cycle visible).
    # R2: q = state OR (a XOR b) combinational (same_cycle visible).
    # Reset: none. Power-up state unspecified -> use 0 as concrete default.
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0) & 1
        b = v.get('b', 0) & 1
        # R2: combinational q from current state and inputs
        q = (state | (a ^ b)) & 1
        out.append({'q': q, 'state': state & 1})
        # R1: posedge update of state (next-state value)
        # Determine next state from observed waveform behavior.
        # From waveform: state transitions appear to follow a specific pattern.
        # Observed: at 45ns (a=0,b=1) state stays 0; at 75ns (a=0,b=0) state becomes 1.
        # Derive next-state function consistent with waveform.
        # Let's infer: next_state = a AND b? Check:
        # 15ns: a=0,b=0 -> state 0 (ok)
        # 45ns: a=0,b=1 -> state 0 (ok, a&b=0)
        # 55ns: a=1,b=0 -> state 0 (ok)
        # 65ns: a=1,b=1 -> state 0? but next row 75ns state=1. Wait 65ns posedge: a=1,b=1 -> next state should be 1, and at 75ns state=1. Yes!
        # 75ns: a=0,b=0 -> next state 0, at 85ns state=0. Yes!
        # 85ns: a=1,b=1 -> next state 1, at 95ns state=1. Yes!
        # 95ns: a=1,b=1 -> next state 1, at 105ns state=1. Yes!
        # 105ns: a=1,b=1 -> next state 1, at 115ns state=1? But waveform shows 115ns state=1, q=0. Wait 115ns row: a=1,b=0, state=1, q=0. So state at 115ns is 1. Yes next state from 105ns (a=1,b=1) = 1. Good.
        # 115ns: a=1,b=0 -> next state 0, at 125ns state=1? Waveform 125ns: a=0,b=1, state=1, q=0. Hmm state=1 at 125ns. But a&b=0 at 115ns. Contradiction.
        # Let's re-examine. Maybe next_state = a OR b? Check:
        # 15ns: 0|0=0 -> state 0 ok
        # 45ns: 0|1=1 -> but state at 55ns is 0. Contradiction.
        # Maybe next_state = a AND b? Already contradicted at 115ns.
        # Let's list posedge samples and next state:
        # posedge at 15ns: a=0,b=0 -> state at 25ns=0
        # 25ns: a=0,b=0 -> state at 35ns=0
        # 35ns: a=0,b=0 -> state at 45ns=0
        # 45ns: a=0,b=1 -> state at 55ns=0
        # 55ns: a=1,b=0 -> state at 65ns=0
        # 65ns: a=1,b=1 -> state at 75ns=1
        # 75ns: a=0,b=0 -> state at 85ns=0
        # 85ns: a=1,b=1 -> state at 95ns=1
        # 95ns: a=1,b=1 -> state at 105ns=1
        # 105ns: a=1,b=1 -> state at 115ns=1
        # 115ns: a=1,b=0 -> state at 125ns=1
        # 125ns: a=0,b=1 -> state at 135ns=1
        # 135ns: a=0,b=0 -> state at 145ns=0
        # 145ns: a=0,b=0 -> state at 155ns=0
        # ...
        # Let's find pattern. Maybe next_state = a AND b OR (state AND (a OR b))?
        # Check 115ns: a=1,b=0, state=1 -> next = 0 OR (1 AND 1)=1. Yes state at 125ns=1.
        # 125ns: a=0,b=1, state=1 -> next = 0 OR (1 AND 1)=1. Yes state at 135ns=1.
        # 135ns: a=0,b=0, state=1 -> next = 0 OR (1 AND 0)=0. Yes state at 145ns=0.
        # 45ns: a=0,b=1, state=0 -> next = 0 OR (0 AND 1)=0. Yes.
        # 55ns: a=1,b=0, state=0 -> next = 0 OR (0 AND 1)=0. Yes.
        # 65ns: a=1,b=1, state=0 -> next = 1 OR (0 AND 1)=1. Yes.
        # 75ns: a=0,b=0, state=1 -> next = 0 OR (1 AND 0)=0. Yes.
        # 85ns: a=1,b=1, state=0 -> next = 1 OR (0 AND 1)=1. Yes.
        # 95ns: a=1,b=1, state=1 -> next = 1 OR (1 AND 1)=1. Yes.
        # 105ns: a=1,b=1, state=1 -> next = 1 OR (1 AND 1)=1. Yes.
        # 115ns: a=1,b=0, state=1 -> next = 0 OR (1 AND 1)=1. Yes.
        # 125ns: a=0,b=1, state=1 -> next = 0 OR (1 AND 1)=1. Yes.
        # 135ns: a=0,b=0, state=1 -> next = 0 OR (1 AND 0)=0. Yes.
        # 145ns: a=0,b=0, state=0 -> next = 0 OR (0 AND 0)=0. Yes.
        # So next_state = (a & b) | (state & (a | b))
        next_state = ((a & b) | (state & (a | b))) & 1
        state = next_state
    return out
