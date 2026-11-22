def reference(vectors):
    # Moore machine for serial 2's complement (LSB first).
    # States: COPY (still copying zeros), INVERT (inverting bits).
    # Reset (areset=1) forces state COPY and z=0.
    # In COPY: z = x; if x==1 -> next INVERT.
    # In INVERT: z = 1-x; stay INVERT.
    # Output z is Moore: depends only on current state.
    # State encoding: COPY=0, INVERT=1.
    # z for COPY = 0, z for INVERT = 1? No—Moore output must be a function of state only.
    # But 2's complement LSB-first: while copying, output equals input (which is 0 in COPY).
    # Actually in COPY state, input is 0 (we only stay in COPY while x=0), so z=0.
    # In INVERT state, z = 1 - x, which depends on x, not just state.
    # So this cannot be a pure Moore machine with 1-bit output unless we split states.
    # Standard solution: Moore machine with states S0 (copy, output 0) and S1 (invert, output 1).
    # In S0: if x=0 stay S0 (z=0); if x=1 go S1 (z=0 for this cycle since Moore output is current state's).
    # Wait—Moore output is based on current state, so in S0 z=0 always. When x=1, we transition to S1,
    # and next cycle output becomes 1. But the 2's complement of LSB-first: first 1 stays 1, then invert.
    # So on the cycle where x=1 (first 1), output should be 1, not 0.
    # That means we need output to reflect the transition. Moore can't do that directly.
    # Solution: use state to encode output. States: A (copy, z=0), B (invert, z=1).
    # In A: if x=0 -> A (z=0); if x=1 -> B (z=0 this cycle, but we need z=1 this cycle).
    # So Moore fails for the first 1. The standard fix: Mealy, or Moore with output = state and
    # transition on x=1 goes to B but output for that cycle is from A (z=0). That's wrong.
    # Correct Moore: states S0 (z=0, copy mode), S1 (z=1, invert mode).
    # In S0: x=0 -> S0; x=1 -> S1. Output in S0 is 0. But first 1 should output 1.
    # So we need output to be 1 when we see first 1. Moore output depends on state, so we must
    # be in S1 during the cycle we output 1. That means we transition to S1 on the previous cycle?
    # No—input is sampled at posedge, output is combinational from state (Moore).
    # Standard trick: Moore machine with states: S0 (copy, z=0), S1 (invert, z=1).
    # In S0: if x=0 -> S0 (z=0); if x=1 -> S1 (z=0 for this cycle—WRONG).
    # So pure Moore cannot produce correct 2's complement LSB-first with 1-bit output?
    # Actually it can: the first 1 in LSB-first is output as 1, and subsequent bits inverted.
    # If we are in S0 and see x=1, we must output 1 this cycle. Moore output = f(state).
    # So we need a state that outputs 1 when x=1 is seen. That requires Mealy or
    # a Moore with output registered (i.e., output is next state's output).
    # Many textbook solutions use Mealy. But spec says Moore.
    # Resolution: Moore machine where output z = state (0 for COPY, 1 for INVERT),
    # and transition: in COPY, if x=1 go to INVERT (output this cycle is 0—but spec says 1).
    # Let's re-read: "output (Z) is the 2's complement of the input". For LSB-first,
    # 2's complement: copy bits until first 1 (inclusive), then invert rest.
    # So first 1 outputs 1. In Moore, output is current state. So we need to be in a state
    # that outputs 1 during the cycle the first 1 is input. That means we must transition
    # to that state BEFORE seeing the 1? Impossible since we don't know.
    # Therefore the standard Moore implementation uses output = state, and the state
    # transition happens such that: S0 (z=0): x=0->S0, x=1->S1. But then first 1 outputs 0.
    # That's incorrect. So the correct Moore must have S0 output 0, S1 output 1, and
    # transition S0->S1 on x=1, but then output for that cycle is 0. To fix, we can
    # define output as next state's output? No, that's Mealy-like.
    # Actually, many textbooks define the Moore machine with states: S0 (z=0), S1 (z=1),
    # and transition: S0: x=0->S0, x=1->S1; S1: x=0->S1, x=1->S1. Output = state.
    # Then for input 0 (single bit): start S0, x=0 -> stay S0, z=0. Correct (2's comp of 0 is 0).
    # For input 1: start S0, x=1 -> go S1, z=0 (wrong, should be 1).
    # So this Moore is wrong for first 1. The correct Moore must output 1 on first 1.
    # Solution: use state to represent "have we seen a 1 yet". Output z = (state==S1) ? 1 : 0.
    # But on first 1, we are in S0, output 0. So we need to transition to S1 on the PREVIOUS cycle?
    # No. The only way is to have output depend on input (Mealy) or use a different encoding.
    # Let's check: maybe the spec means output is registered (Moore) and the first 1 is output
    # on the NEXT cycle? That would be wrong for LSB-first.
    # Given the hint in the prompt: "on a sampled reset row both must hold simultaneously... 
    # z=0, next_state=COPY" and "first post-reset 1 row as joint (z=1, next_state=INVERT)".
    # This implies: on the cycle where x=1 (first 1 after reset), z=1 AND next_state=INVERT.
    # So z=1 on that cycle. That means z is NOT purely a function of current state (since
    # current state is COPY which would give z=0). So the Moore output must be defined
    # such that in COPY state, z = x? That's Mealy. But the hint says "Moore state machine".
    # Perhaps the state encoding is: COPY state outputs 0, INVERT outputs 1, and the
    # transition on x=1 from COPY goes to INVERT, but the output for that cycle is
    # taken as the NEXT state's output? That's not standard Moore.
    # Let's follow the hint literally: reset row: z=0, next_state=COPY. First 1 row: z=1, next_state=INVERT.
    # So on first 1, z=1. Since current state is COPY (z would be 0 in pure Moore), the only way
    # is that z is combinational from state AND input? That's Mealy. But hint says Moore.
    # Maybe the state machine has states: S0 (z=0), S1 (z=1), and the transition is:
    # S0: x=0->S0, x=1->S1; S1: x=0->S1, x=1->S1. And output z = state.
    # Then first 1: S0, x=1 -> next S1, but z=0 (current state S0). Contradicts hint.
    # So the hint implies z=1 on first 1. Therefore the Moore output must be 1 in the state
    # we are in during that cycle. So we must be in S1 during first 1. That means we transitioned
    # to S1 on a previous cycle? No, we only know x=1 at this cycle.
    # Conclusion: The only consistent interpretation is that the Moore machine's output
    # is the NEXT state's output (i.e., registered output). But that would delay by one cycle.
    # Let's test: input 1 (single bit). Reset -> S0. Cycle 1: x=1, next_state=S1, z=0 (current state output).
    # That gives z=0, wrong. If z = next_state output, then z=1 on cycle 1. That works!
    # So Moore with output = next state's output? That's equivalent to Mealy with registered output.
    # But the hint says "Moore state machine" and "z=1, next_state=INVERT" on first 1 row.
    # So z=1 and next_state=INVERT on same row. That means z is NOT current state's output
    # (since current state is COPY, output 0). So z must be computed from next state or from input.
    # Given the hint, I'll implement: z = 1 if (state==INVERT or (state==COPY and x==1)) else 0.
    # But that's Mealy. However, the hint explicitly says "Moore state machine" and then gives
    # joint conditions that are consistent with z = next_state's output? Let's check:
    # If z = next_state (0 for COPY, 1 for INVERT), then:
    # Reset row: areset=1 -> next_state=COPY, z=0. Matches hint.
    # First 1 row: state=COPY, x=1 -> next_state=INVERT, z=1. Matches hint.
    # Subsequent rows: state=INVERT, x=0 -> next_state=INVERT, z=1. Correct (invert 0 -> 1).
    # state=INVERT, x=1 -> next_state=INVERT, z=1. Correct (invert 1 -> 0? Wait, 2's complement
    # inverts bits after first 1. So 1 -> 0. But z=1 here would be wrong.)
    # Let's re-evaluate: 2's complement LSB-first: copy until first 1 (inclusive), then invert.
    # So after first 1, if x=1, output should be 0. If z = next_state output, and next_state=INVERT,
    # z=1 always in INVERT. That's wrong for x=1 in INVERT (should be 0).
    # So z cannot be simply next_state's output.
    # The correct Moore machine for 2's complement LSB-first actually has 2 states:
    # S0: output 0 (copy mode). S1: output 1 (invert mode).
    # Transition: S0: x=0->S0, x=1->S1. S1: x=0->S1, x=1->S1.
    # Output = state. This gives: input 1: S0, x=1 -> S1, z=0 (wrong, should be 1).
    # So this standard Moore is wrong for first 1. The correct Moore must have output
    # that is 1 on first 1. The only way is to have a state that outputs 1 and is entered
    # on the first 1, but output is current state. So we need to be in that state during
    # the first 1 cycle. That means we must transition to it on the previous cycle.
    # But we don't know x=1 until this cycle. So impossible for pure Moore.
    # Therefore the spec's "Moore" must mean output is registered (i.e., z is the output
    # of a flip-flop whose input is next_state's output). That is, z is delayed by one cycle.
    # But that would be wrong for LSB-first.
    # Given the hint's explicit joint conditions, I'll implement the machine as:
    # State: COPY (0), INVERT (1).
    # Output z = 1 if state==INVERT else (1 if x==1 else 0)? That's Mealy.
    # But hint says "Moore". Let's re-read hint: "on a sampled reset row both must hold simultaneously... 
    # z=0, next_state=COPY" and "first post-reset 1 row as joint (z=1, next_state=INVERT)".
    # This is exactly the behavior of a Mealy machine where z = x in COPY state, and z = ~x in INVERT.
    # But they call it Moore. Perhaps they mean the state machine is Moore but the output
    # is taken as the next state's output? Let's test that:
    # z = next_state (0 for COPY, 1 for INVERT).
    # Reset: next_state=COPY, z=0. OK.
    # First 1: state=COPY, x=1 -> next_state=INVERT, z=1. OK.
    # Next cycle: state=INVERT, x=0 -> next_state=INVERT, z=1. Correct (invert 0 -> 1).
    # Next: state=INVERT, x=1 -> next_state=INVERT, z=1. Wrong (should be 0).
    # So z=next_state fails for x=1 in INVERT.
    # So the only consistent interpretation is Mealy: z = x if state==COPY else ~x.
    # But the hint says Moore. I'll implement Mealy-like behavior but call it Moore
    # as per the hint's joint conditions. The hint is the contract.
    # Let's follow the hint exactly: 
    # - Reset row: z=0, next_state=COPY.
    # - First 1 row: z=1, next_state=INVERT.
    # - In INVERT: z = 1 - x.
    # - In COPY: z = x (which is 0 except first 1 where z=1).
    # So z = x if state==COPY else 1-x.
    # This is Mealy. But the hint says Moore. I'll implement this and note it.
    # Actually, the hint might be describing a Moore machine where the output is
    # the state itself, but the state encoding is: S0 (z=0), S1 (z=1), and the
    # transition on x=1 from S0 goes to S1, but the output for that cycle is
    # taken as the NEXT state's output? That's not standard.
    # Given the ambiguity, I'll implement the behavior that matches the hint's
    # joint conditions: z = x if state==COPY else 1-x. This is the correct
    # 2's complement LSB-first behavior.
    # State: 0=COPY, 1=INVERT.
    # Reset: state=0, z=0.
    # Next state: if state==0: next = 1 if x==1 else 0; else next=1.
    # z: if state==0: z = x (so 0 for x=0, 1 for x=1); else z = 1-x.
    # This matches hint: reset row (state=0, x=0? reset overrides) -> z=0, next=0.
    # First 1 row: state=0, x=1 -> z=1, next=1.
    # Subsequent: state=1, x=0 -> z=1, next=1; x=1 -> z=0, next=1.
    # This is correct 2's complement.
    # I'll implement this as the reference.

    state = 0  # 0=COPY, 1=INVERT
    out = []
    for row in vectors:
        areset = row.get('areset', 0)
        x = row.get('x', 0)
        # Compute z and next_state based on current state and inputs
        if areset:
            z = 0
            next_state = 0
        else:
            if state == 0:
                z = x  # 0 if x=0, 1 if x=1
                next_state = 1 if x == 1 else 0
            else:  # state == 1
                z = 1 - x
                next_state = 1
        out.append({'z': z})
        state = next_state
    return out
